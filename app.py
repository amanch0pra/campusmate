from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import warnings
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

warnings.filterwarnings('ignore')

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# ============= LOAD NEURAL ARCHITECTURE =============
print("🧠 Initializing Campus Mate...")

try:
    with open('models/chatbot_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✓ Synaptic Weights Loaded")
    
    with open('models/tfidf_vectorizer.pkl', 'rb') as f:
        tfidf = pickle.load(f)
    print("✓ Vectorizer Synchronized")
    
    with open('models/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    print("✓ Class Labels Indexed")
    
    with open('models/dataset.pkl', 'rb') as f:
        df = pickle.load(f)
    print("✓ Multi-dimensional Knowledge Base Online")
    
    print(f"📊 Processing {len(df)} High-Fidelity Data Points")
    
except Exception as e:
    print(f"\n❌ System Failure: {e}")
    exit(1)

# Load Sentence Transformer
print("\n🔄 Booting Semantic Intelligence...")
try:
    # Use the same model as training
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
    with open('models/question_embeddings.pkl', 'rb') as f:
        question_embeddings = pickle.load(f)
    print("✓ Neural Embeddings Online")
except Exception as e:
    print(f"⚠️ Warning: Semantic Intelligence degraded: {e}")
    sentence_model = None
    question_embeddings = None

# ============= COGNITIVE FALLBACKS =============

CATEGORY_SYNOPSIS = {
    'Academic': """The **Academic Framework** at LPU operates on a 10-point CGPA system with mandatory 75% attendance benchmarks. Evaluation tiers include CA (20%), MTE (20%), and ETE (60%). For deep-level queries, access the UMS portal or visit Academic Affairs in Block-A.""",
    'Admissions and Administration': """Our **Admission Protocols** are merit-based, leveraging LPUNEST scores for scholarship determination. Application cycles are continuous. Scholarships range from merit-based offsets to sports-related excellence grants.""",
    'Campus Life': """The **Lifestyle Ecosystem** features a 600-acre infrastructure with 24/7 security, biotic-monitored hostels, and multi-cuisine hubs. We maintain a high-decibel campus experience with 100+ active societies and international-standard sports facilities.""",
    'Placements and Career': """The **Career Trajectory** at LPU is supported by 900+ recruitment agencies. Tier-1 outliers include Google, Microsoft, and Amazon with international packages peaking at ₹1.05 Cr. Training begins in the 5th semester.""",
    'Rules Safety and Grievance': """Our **Governance Protocols** enforce a strictly disciplined environment. This includes anti-ragging mandates, formal dress codes, and biometric surveillance. Grievances are routed through the RMS portal with a 7-day resolution window."""
}

# ============= NEURAL HELPER FUNCTIONS =============

def expand_acronyms(text):
    ACRONYMS = {
        "dl": "duty leave", "ml": "medical leave", "ums": "university management system",
        "mte": "mid term exam", "ete": "end term exam", "ca": "continuous assessment",
        "cgpa": "cumulative grade point average", "sgpa": "semester grade point average",
        "hod": "head of department", "lpunest": "lpu entrance test", "tg": "teacher guardian"
    }
    words = text.lower().split()
    return ' '.join([ACRONYMS.get(w, w) for w in words])

def get_semantic_match(question, mode=None, top_k=1):
    if sentence_model is None or question_embeddings is None: return []
    
    # Mode filtering
    if mode and mode not in ['auto', 'General']:
        indices = [i for i, m in enumerate(df['Mode']) if m == mode]
        if not indices: return []
        target_embeddings = question_embeddings[indices]
        target_df = df.iloc[indices]
    else:
        target_embeddings = question_embeddings
        target_df = df
        indices = range(len(df))

    query_embedding = sentence_model.encode([question])[0]
    similarities = cosine_similarity([query_embedding], target_embeddings)[0]
    
    best_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in best_indices:
        results.append({
            'answer': target_df.iloc[idx]['Answer'],
            'question': target_df.iloc[idx]['Question'],
            'mode': target_df.iloc[idx]['Mode'],
            'similarity': float(similarities[idx])
        })
    return results

def synthesize_response(question, selected_mode):
    """
    Cognitive synthesis using Groq RAG (Retrieval-Augmented Generation)
    """
    original_question = question
    question = expand_acronyms(question)
    
    # Retrieve relevant context from the official dataset
    # We increase top_k to 10 to maximize context coverage for Groq
    matches = get_semantic_match(question, mode=selected_mode, top_k=10)
    
    # Keyword-Based Boosting for Critical Protocols
    # This ensures that if a student asks about a specific university system, 
    # we find the exact protocol even if semantic similarity is slightly lower.
    CRITICAL_KEYWORDS = {'rms': 'Request Management System', 'dl': 'Duty Leave', 'cgpa': 'CGPA', 'fee': 'Fee', 'scholarship': 'Scholarship'}
    matched_contexts = []
    
    # 1. Add Semantic Matches
    for m in matches:
        matched_contexts.append(m)
        
    # 2. Hard Keyword Match (Fail-safe for critical LPU systems)
    query_lower = question.lower()
    for kw, full_name in CRITICAL_KEYWORDS.items():
        if kw in query_lower or full_name.lower() in query_lower:
            # Find rows containing this keyword in the Question
            # We take more matches here to ensure we don't miss the detailed protocols
            kw_matches = df[df['Question'].str.contains(kw, case=False, na=False) | 
                            df['Question'].str.contains(full_name, case=False, na=False)]
            
            # Prioritize "How to" OR "Process" questions for these keywords
            # We also look for "S-Block", "Uni-Mall", "Block 34" for navigation
            how_to_matches = kw_matches[kw_matches['Question'].str.contains('How to|Process|Sequence|Steps|Where is', case=False, na=False)]
            
            # Combine prioritized and regular matches
            final_kw_list = pd.concat([how_to_matches, kw_matches.head(5)]).drop_duplicates().head(7)
            
            for _, row in final_kw_list.iterrows():
                # Add to context if not already there
                if not any(ctx['question'] == row['Question'] for ctx in matched_contexts):
                    matched_contexts.append({
                        'question': row['Question'],
                        'answer': row['Answer'],
                        'mode': row['Mode'],
                        'similarity': 0.8 # High Boost for Critical Keywords
                    })
    
    # Sort by similarity (keep the most relevant ones first)
    matched_contexts = sorted(matched_contexts, key=lambda x: x['similarity'], reverse=True)[:10]

    # If it's a critical query, we allow a lower similarity threshold
    is_critical = any(kw in query_lower for kw in CRITICAL_KEYWORDS)
    threshold = 0.20 if is_critical else 0.25
    
    if not matched_contexts or matched_contexts[0]['similarity'] < threshold:
        return {
            'answer': "I'm sorry, I don't have specific information about that in my LPU dataset. For accuracy, please consult the University Management System (UMS) or visit the relevant department block.",
            'mode': 'system',
            'confidence': 0.0,
            'method': 'restricted_scope'
        }

    # Construct the context-grounded prompt for Groq
    context_data = "\n\n".join([f"Source Question: {m['question']}\nSource Answer: {m['answer']}" for m in matched_contexts])
    
    system_prompt = """You are Campus Mate, the ELITE Lovely Professional University (LPU) student assistant. 
Your goal is to provide high-fidelity, accurate, and actionable information strictly based on the provided context.

Formatting Protocol:
1. Use **bold** for portal names, block numbers, and key steps.
2. Use bullet points for sequences (e.g., UMS -> RMS -> DL).
3. If the user asks for a 'guide' or 'how to', provide a clear Step 1, Step 2 format.

If the information is not present in the context, politely inform the user that you don't have that specific data. 
Never hallucinate or use external general knowledge. Always speak as a premium LPU assistant."""
    
    user_prompt = f"""Use the following context from our official database to answer the student's query.

---
DATABASE CONTEXT:
{context_data}
---

STUDENT QUERY: {original_question}

INSTRUCTIONS:
- provide a natural, conversational response.
- use Markdown formatting (bolding, lists) for readability.
- ONLY use facts from the DATABASE CONTEXT.
- If the query is just a greeting, respond normally as Campus Mate.
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=800
        )
        
        reply = completion.choices[0].message.content
        
        return {
            'answer': reply,
            'mode': matches[0]['mode'],
            'confidence': matches[0]['similarity'],
            'method': 'groq_braintrust'
        }
        
    except Exception as e:
        print(f"⚠️ Neural Link Error (Groq): {e}")
        # High-fidelity fallback to direct dataset match
        return {
            'answer': matches[0]['answer'],
            'mode': matches[0]['mode'],
            'confidence': matches[0]['similarity'],
            'method': 'semantic_fallback'
        }

# ============= ROUTES =============

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        selected_mode = data.get('mode', 'auto')
        
        if not user_message:
            return jsonify({'response': 'Awaiting input sequence...', 'mode': 'system', 'confidence': 1.0})
        
        result = synthesize_response(user_message, selected_mode)
        
        return jsonify({
            'response': result['answer'],
            'mode': result['mode'],
            'confidence': result['confidence'],
            'method': result['method']
        })
    
    except Exception as e:
        print(f"🔥 Core Error: {e}")
        return jsonify({
            'response': "⚠️ **System Overload**: An internal exception occurred. Re-synchronizing neural link...",
            'mode': 'error',
            'confidence': 0.0
        })

if __name__ == '__main__':
    # Standard Hugging Face Space port is 7860
    port = int(os.environ.get("PORT", 7860))
    app.run(debug=False, host='0.0.0.0', port=port)
