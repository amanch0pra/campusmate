"""
Campus Mate - Advanced ML Model Training Script
This script trains models for the advanced chatbot including:
- Multinomial Naive Bayes for mode classification
- Sentence embeddings for semantic search
- Category classification
"""

import pandas as pd
import numpy as np
import pickle
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sentence_transformers import SentenceTransformer
import warnings
import os
warnings.filterwarnings('ignore')

# Download required NLTK data
print("Downloading NLTK data...")
try:
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except Exception as e:
    print(f"Note: NLTK download had issues: {e}")
    print("Continuing anyway...")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ============= STEP 1: LOAD DATASET =============
print("\n" + "="*60)
print("STEP 1: Loading Dataset")
print("="*60)

df = pd.read_csv('data/master_dataset.csv')
print(f"✓ Dataset loaded successfully")
print(f"  Total samples: {len(df)}")
print(f"  Modes: {df['Mode'].unique()}")
print(f"\nMode distribution:")
print(df['Mode'].value_counts())

# ============= STEP 2: TEXT PREPROCESSING =============
print("\n" + "="*60)
print("STEP 2: Text Preprocessing")
print("="*60)

# LPU Specific Acronyms for Training
LPU_ACRONYMS = {
    "ums": "university management system",
    "lms": "learning management system blackboard",
    "rms": "request management system",
    "dl": "duty leave",
    "ml": "medical leave",
    "lpunest": "lpu national entrance scholarship test",
    "mte": "mid term exam examination",
    "ete": "end term exam examination",
    "ca": "continuous assessment",
    "cgpa": "cumulative grade point average",
    "sgpa": "semester grade point average",
    "tg": "teacher guardian",
    "hod": "head of department",
    "umc": "unfair means case",
    "erp": "enterprise resource planning parent portal",
    "naac": "national assessment accreditation council",
    "ugc": "university grants commission",
    "lpu": "lovely professional university"
}

def expand_acronyms(text):
    """
    Expand common LPU acronyms in text
    """
    words = text.lower().split()
    expanded_words = [LPU_ACRONYMS.get(word, word) for word in words]
    return ' '.join(expanded_words)

def preprocess_text(text):
    """
    Preprocess text using NLP techniques:
    - Lowercasing
    - Expanding Acronyms
    - Removing special characters and digits
    - Tokenization
    - Stopword removal
    """
    # Convert to lowercase
    text = str(text).lower()
    
    # 1. Expand Acronyms
    text = expand_acronyms(text)
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    
    # Join tokens back
    if not tokens:
        return text
    return ' '.join(tokens)

# Apply preprocessing to questions
print("Preprocessing questions...")
df['processed_question'] = df['Question'].apply(preprocess_text)
print(f"✓ Preprocessing completed")
print(f"  Example:")
print(f"    Original: {df['Question'].iloc[0]}")
print(f"    Processed: {df['processed_question'].iloc[0]}")

# ============= STEP 3: FEATURE EXTRACTION =============
print("\n" + "="*60)
print("STEP 3: Feature Extraction using TF-IDF")
print("="*60)

# Initialize TF-IDF Vectorizer
tfidf = TfidfVectorizer(max_features=500, ngram_range=(1, 2))

# Fit and transform the text data
X = tfidf.fit_transform(df['processed_question'])
print(f"✓ TF-IDF vectorization completed")
print(f"  Feature matrix shape: {X.shape}")
print(f"  Vocabulary size: {len(tfidf.vocabulary_)}")

# Encode labels (modes)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['Mode'])
print(f"✓ Label encoding completed")
print(f"  Classes: {label_encoder.classes_}")

# ============= STEP 4: TRAIN-TEST SPLIT =============
print("\n" + "="*60)
print("STEP 4: Splitting Dataset")
print("="*60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"✓ Dataset split completed")
print(f"  Training samples: {X_train.shape[0]}")
print(f"  Testing samples: {X_test.shape[0]}")

# ============= STEP 5: MODEL TRAINING =============
print("\n" + "="*60)
print("STEP 5: Training Multinomial Naive Bayes Model")
print("="*60)

# Initialize and train the model
model = MultinomialNB(alpha=1.0)
model.fit(X_train, y_train)
print(f"✓ Model training completed")

# ============= STEP 6: MODEL EVALUATION =============
print("\n" + "="*60)
print("STEP 6: Model Evaluation")
print("="*60)

# Predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Calculate accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"✓ Training Accuracy: {train_accuracy*100:.2f}%")
print(f"✓ Testing Accuracy: {test_accuracy*100:.2f}%")

print(f"\n📊 Classification Report (Test Set):")
print("="*60)
print(classification_report(y_test, y_test_pred))

print(f"\n📊 Confusion Matrix:")
print("="*60)
cm = confusion_matrix(y_test, y_test_pred)
print(cm)

# ============= STEP 7: SEMANTIC EMBEDDINGS =============
print("\n" + "="*60)
print("STEP 7: Generating Semantic Embeddings")
print("="*60)

print("Loading Sentence Transformer model...")
try:
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Sentence Transformer loaded")
    
    print("\nGenerating embeddings for all questions...")
    print("(This may take 1-2 minutes for the first time)")
    
    # CRITICAL: Use expanded questions for embeddings to match runtime behavior
    print("Expanding acronyms for embeddings...")
    expanded_questions = df['Question'].apply(expand_acronyms).tolist()
    
    question_embeddings = sentence_model.encode(
        expanded_questions, 
        show_progress_bar=True,
        batch_size=32
    )
    print(f"✓ Embeddings generated")
    print(f"  Shape: {question_embeddings.shape}")
    
    semantic_model_available = True
except Exception as e:
    print(f"⚠️ Warning: Could not generate semantic embeddings: {e}")
    print("The chatbot will work with TF-IDF only")
    question_embeddings = None
    semantic_model_available = False

# ============= STEP 8: SAVE TRAINED MODELS =============
print("\n" + "="*60)
print("STEP 8: Saving Trained Models")
print("="*60)

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Save the trained model
with open('models/chatbot_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✓ Model saved: models/chatbot_model.pkl")

# Save the TF-IDF vectorizer
with open('models/tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)
print("✓ TF-IDF Vectorizer saved: models/tfidf_vectorizer.pkl")

# Save the label encoder
with open('models/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
print("✓ Label Encoder saved: models/label_encoder.pkl")

# Save the original dataset for response matching
with open('models/dataset.pkl', 'wb') as f:
    pickle.dump(df, f)
print("✓ Dataset saved: models/dataset.pkl")

# Save semantic embeddings if available
if semantic_model_available and question_embeddings is not None:
    with open('models/question_embeddings.pkl', 'wb') as f:
        pickle.dump(question_embeddings, f)
    print("✓ Semantic embeddings saved: models/question_embeddings.pkl")

print("\n" + "="*60)
print("✅ ADVANCED MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"\n📈 Summary:")
print(f"  - Training Accuracy: {train_accuracy*100:.2f}%")
print(f"  - Testing Accuracy: {test_accuracy*100:.2f}%")
print(f"  - Total Samples: {len(df)}")
print(f"  - Number of Modes: {len(label_encoder.classes_)}")
print(f"  - Model: Multinomial Naive Bayes")
print(f"  - Feature Extraction: TF-IDF (500 features)")
print(f"  - Semantic Search: {'✓ Enabled' if semantic_model_available else '✗ Disabled'}")
print(f"\n✨ Advanced Features:")
print(f"  • Semantic understanding with sentence transformers")
print(f"  • Multi-tier fallback system")
print(f"  • Fuzzy matching for typo tolerance")
print(f"  • Category-based intelligent responses")
print(f"  • 100% response rate (no 'sorry' messages)")
print(f"\n🎯 Ready to deploy in Flask application!")
print("="*60 + "\n")
