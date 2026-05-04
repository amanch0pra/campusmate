---
title: Campus Mate
emoji: 🎓
colorFrom: yellow
colorTo: indigo
sdk: docker
app_file: app.py
pinned: false
---

<div align="center">

# 🎓 Campus Mate

### The AI-Powered Intelligence Hub for Lovely Professional University Students

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-FF6B35?style=for-the-badge&logo=meta&logoColor=white)](https://groq.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-Academic-6366F1?style=for-the-badge)](LICENSE)

<br>

**Campus Mate** is an advanced RAG-powered (Retrieval-Augmented Generation) chatbot built exclusively for LPU students. It combines a curated 1,590+ Q&A knowledge base with Groq's LLaMA 3.3 70B model to deliver accurate, contextual answers to every LPU-related query — from bonafide certificates to placement packages.

[🚀 Quick Start](#-installation--setup) · [✨ Features](#-features) · [🏗️ Architecture](#️-architecture) · [📚 Knowledge Base](#-knowledge-base)

</div>

---

## 🖥️ Preview

| Feature | Description |
|---|---|
| **UI** | Premium glassmorphism dark theme with animated particle canvas |
| **Response Engine** | Groq LLaMA 3.3 70B via RAG (Retrieval-Augmented Generation) |
| **Knowledge Base** | 1,590+ real LPU Q&A pairs with semantic embeddings |
| **Smart Fallback** | Semantic search → Groq AI → Direct dataset match |
| **Modes** | Academic · Admissions · Campus Life · Placements · Rules & Safety |

---

## ✨ Features

### 🤖 AI & Intelligence
- **Groq RAG Engine** — Retrieves top-10 most relevant Q&As from the LPU knowledge base and feeds them as context to LLaMA 3.3 70B for accurate, grounded answers
- **Semantic Search** — `all-MiniLM-L6-v2` sentence embeddings for meaning-based query matching (not just keyword matching)
- **Keyword Boosting** — Critical LPU systems (RMS, UMS, CGPA, DL, Fee) get priority retrieval
- **Auto Mode Detection** — Naive Bayes classifier automatically detects the right knowledge domain
- **Acronym Expansion** — Understands LPU-specific shorthand (DL, MTE, ETE, TG, UMC, HOD, etc.)

### 🎨 User Interface
- Animated particle canvas background with network graph effect
- Full glassmorphism card system with ambient glow orbs
- 4 quick-action dashboard cards for the most frequent queries
- 8 suggested question chips on first load
- Auto-resizing textarea with `Shift+Enter` for new lines
- Copy button on every bot response
- Direct **Open UMS** button
- Clear chat with chip panel restoration
- Toast notification system
- Fully responsive — mobile, tablet, desktop

### 📚 Knowledge Coverage
Over **1,590 real LPU Q&A pairs** covering:

| Domain | Topics |
|---|---|
| 🎓 **Academic** | UMS, LMS, attendance rules, bonafide/character/migration certificates, transcripts, CGPA/SGPA, exam patterns (CA/MTE/ETE), backlogs, re-evaluation, grace marks |
| 📝 **Admissions** | Admission process, fee structure, payment, refund policy, LPUNEST scholarship, JEE-based scholarships, education loan, NAAC/UGC accreditation, BTech programmes |
| 🏕️ **Campus Life** | Hostel blocks (Boys B1–B12 / Girls G1–G8), hostel fees, curfew, mess plans, Uni-mall, library, sports complex, clubs & societies, LPU app, banking, campus location |
| 💼 **Placements** | Top recruiters, highest/average packages, CDC registration, CGPA cutoffs, internships, pre-placement offers, startup incubator, Lovely Tech Park |
| ⚖️ **Rules & Safety** | Anti-ragging policy, dress code, UMC (Unfair Means Cases), POSH/ICC, visitor policy, hostel rules, alcohol/smoking policy, security system |

---

## 🏗️ Architecture

```
Student Query
     │
     ▼
┌─────────────────────────────────┐
│         Flask Backend           │
│                                 │
│  1. Acronym Expansion           │
│  2. Semantic Embedding (MiniLM) │
│  3. Cosine Similarity Search    │──▶ Top-10 Q&A Context
│  4. Keyword Boost (RMS/UMS/DL)  │
│                                 │
│  5. Groq API (LLaMA 3.3 70B)   │◀── Context + Query
│     RAG Prompt Construction     │
│                                 │
│  6. Response → Student          │
└─────────────────────────────────┘

Fallback Chain:
Groq RAG → Direct Dataset Match → Scope Restriction Message
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.8+, Flask 2.3, Flask-CORS |
| **AI / LLM** | Groq API · LLaMA 3.3 70B Versatile |
| **ML / NLP** | scikit-learn · NLTK · sentence-transformers |
| **Embeddings** | `all-MiniLM-L6-v2` (384-dim) |
| **Classification** | Multinomial Naive Bayes + TF-IDF (500 features) |
| **Similarity** | Cosine Similarity via sklearn |
| **Frontend** | Vanilla HTML5 · CSS3 · JavaScript (ES2022) |
| **Fonts** | Google Fonts (Outfit + JetBrains Mono) |

---

## 📂 Project Structure

```
campus-mate/
│
├── 📁 data/
│   └── master_dataset.csv          # 1,590+ LPU Q&A pairs
│
├── 📁 models/                      # Auto-generated after training
│   ├── chatbot_model.pkl           # Trained Naive Bayes classifier
│   ├── tfidf_vectorizer.pkl        # TF-IDF feature extractor
│   ├── label_encoder.pkl           # Mode/category encoder
│   ├── dataset.pkl                 # Pickled dataset for retrieval
│   └── question_embeddings.pkl     # Pre-computed sentence embeddings
│
├── 📁 static/
│   ├── css/style.css               # Premium glassmorphism UI
│   ├── js/script.js                # Frontend logic + particle engine
│   ├── logo.png                    # App logo
│   └── lpu_logo.png                # LPU logo
│
├── 📁 templates/
│   └── index.html                  # Main chatbot interface
│
├── 📁 academic_documentation/
│   └── PROJECT_REPORT.md           # Full academic documentation
│
├── app.py                          # Flask application + RAG engine
├── train_model.py                  # ML training script
├── expand_lpu_data.py              # Dataset expansion utility
├── requirements.txt                # Python dependencies
├── .env                            # API keys (not committed)
├── .gitignore
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- A [Groq API key](https://console.groq.com) (free tier available)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/campus-mate.git
cd campus-mate
```

### Step 2 — Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

### Step 5 — Train the Model

```bash
python train_model.py
```

Expected output:
```
✓ Dataset loaded — 1590 samples
✓ TF-IDF vectorization complete
✓ Model trained — Accuracy: 86.64% (train) / 81.76% (test)
✓ Semantic embeddings generated — Shape: (1590, 384)
✅ Models saved to /models/
```

### Step 6 — Run the Application

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 💬 Usage Examples

| Query | What Saathi Answers |
|---|---|
| `"Which department issues bonafide letters?"` | Registrar's Office, Block-A; apply via UMS → RMS → Certificate Request |
| `"What is the fee for BTech CSE?"` | ₹70K–₹1.05L per semester with LPUNEST scholarship details |
| `"How to apply for duty leave?"` | Step-by-step UMS → RMS → DL process |
| `"What is the attendance rule?"` | 75% mandatory; condonation process for medical/DL cases |
| `"Which companies visit for placements?"` | Google, Microsoft, Amazon + 900 more with package info |
| `"How to get a character certificate?"` | DSW Office, Block-A; via UMS portal with timeline |
| `"What is the hostel curfew time?"` | Boys 10:30 PM · Girls 8:00 PM with enforcement details |
| `"How is CGPA calculated at LPU?"` | Full formula with grade point table |

**Quick Actions available on the homepage:**
- 🎫 RMS Portal — Requests & DL
- 💳 Fee Structure — Academic Dues  
- 🎯 CGPA System — Grading & Marks
- 🚀 Placements — Top Recruiters

---

## 📊 Model Performance & Accuracy

The **Campus Mate** intelligence engine has been rigorously trained and evaluated on a custom dataset of **1,590+ verified LPU Q&A pairs**. 

### 🎯 Classification Accuracy
The Multinomial Naive Bayes classifier is used to route queries to the correct domain (Academic, Admissions, etc.).

| Metric | Value | Status |
|---|---|---|
| **Training Accuracy** | **86.64%** | ✅ Excellent |
| **Testing Accuracy** | **81.76%** | ✅ Robust |
| **Optimization** | TF-IDF (500 features) | High Precision |
| **Inference Time** | < 150ms | Real-time |

### 🔍 Semantic Engine Performance
For query matching, we use the `all-MiniLM-L6-v2` transformer model to ensure the bot understands the *intent* even when keywords don't match exactly.

*   **Embedding Space**: 384 Dimensions
*   **Similarity Threshold**: 0.60 (Fuzzy Match Fallback)
*   **Knowledge Coverage**: 90%+ of common university lifecycle queries
*   **Reliability**: 100% response rate with smart RAG integration (Groq LLaMA 3.3 70B)

### 📈 Training Summary
The model demonstrates high precision in **Academic** and **Admissions** queries, while continuous data expansion is improving performance in **Rules & Safety** and **Campus Life** categories.


---

## 🔧 Expanding the Knowledge Base

To add new LPU Q&A pairs:

1. Open `data/master_dataset.csv`
2. Add rows in this format:

```csv
Question,Answer,Mode
"How to apply for XYZ?","Step-by-step answer...","Academic"
```

Valid modes: `Academic` · `Admissions and Administration` · `Campus Life` · `Placements and Career` · `Rules Safety and Grievance` · `General`

3. Retrain:

```bash
python train_model.py
```

4. Restart the server:

```bash
python app.py
```

Or use the provided expansion utility:

```bash
python expand_lpu_data.py    # Appends new data and deduplicates
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|---|---|
| `FileNotFoundError: models/chatbot_model.pkl` | Run `python train_model.py` first |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `GROQ_API_KEY not found` | Create a `.env` file with your key |
| Port 5000 already in use | Change port in `app.py`: `app.run(port=5001)` |
| NLTK data missing | Run `python -c "import nltk; nltk.download('all')"` |
| Slow first response | Sentence embeddings load on startup — wait ~20s after launch |

---

## 🔮 Roadmap

- [ ] **Voice input** — Web Speech API integration for hands-free queries
- [ ] **Multilingual** — Hindi and Punjabi support for wider accessibility
- [ ] **Conversation memory** — Multi-turn context for follow-up questions
- [ ] **UMS Live Integration** — Pull real attendance/results via UMS API
- [ ] **Mobile App** — React Native wrapper for Android/iOS
- [ ] **Analytics Dashboard** — Admin panel to see popular queries and gaps
- [ ] **WhatsApp Bot** — Twilio integration for WhatsApp-based queries
- [ ] **Fine-tuned LLM** — Domain-specific fine-tuning on LPU data

---

## 📝 License

This is an academic project developed for educational purposes at Lovely Professional University. All information is sourced from publicly available LPU resources and official university publications. Not for commercial use.

---

## 👤 Author

**Aman Chopra (12406294)**  
School of Computer Science & Engineering  
**Lovely Professional University**

> For official LPU information, visit **[lpu.in](https://www.lpu.in)**  
> Official UMS portal: **[ums.lpu.in](https://ums.lpu.in)**

---

## ⭐ Acknowledgments

- **Groq** for blazing-fast LLaMA 3.3 inference
- **Hugging Face** for `sentence-transformers` and `all-MiniLM-L6-v2`
- **scikit-learn** and **NLTK** communities
- **Flask** framework developers
- **LPU** for the knowledge domain

---

<div align="center">

**Built with ❤️ for LPU Students**

*If this project helped you, please give it a ⭐ on GitHub!*

</div>
