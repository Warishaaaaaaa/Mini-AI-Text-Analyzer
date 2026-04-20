# 🧠 Mini AI Text Analyzer

> ⚠️ **Disclaimer:** This project is built purely for **learning purposes** as a beginner NLP project. It may not be perfect, may have limitations, and is not intended for production use. Feedback and suggestions are always welcome!

---

## 📌 What is this?

Mini AI Text Analyzer is a beginner-friendly desktop application built with **Python** and **Tkinter**. It takes any text input and performs three basic NLP (Natural Language Processing) tasks:

- ✅ **Spell Correction** — fixes common spelling mistakes
- ✅ **Text Processing** — removes stopwords and punctuation, keeps only meaningful words
- ✅ **Sentiment Analysis** — tells you if the text is Positive 😊, Neutral 😐, or Negative 😡

Results are displayed in a clean, professional GUI and automatically saved to a `report.txt` file.

---

## 🖥️ GUI Preview

The app features a modern light-themed desktop interface with:
- Header bar with status indicator
- Input text box with character counter
- Analyze / Clear / Exit buttons
- Output panel showing Original, Corrected, and Processed text
- Sidebar with Word Count, Unique Word Count, and Sentiment Meter

---
---

## 📸 Screenshots

### 🖥️ GUI Interface
![GUI](screenshots/gui.png)

### 📊 Analysis Output
![Output](screenshots/output.png)

### 📈 Result View
![Result](screenshots/report.png)

---
## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.14.2 | Core programming language |
| Tkinter | GUI (desktop window) |
| NLTK | Tokenization & stopword removal |
| TextBlob | Spell correction & sentiment analysis |
| Threading | Keeps GUI responsive during processing |

---

## 📦 Requirements

Make sure you have Python installed, then install the required libraries:

```bash
pip install nltk textblob
```

On first run, the app will automatically download required NLTK data:
- `punkt` — tokenizer
- `punkt_tab` — tokenizer tables
- `stopwords` — common English stopwords

---

## 🚀 How to Run

1. Clone this repository:
```bash
git clone https://github.com/Warishaaaaaaa/Mini-AI-Text-Analyzer
```

2. Navigate into the project folder:
```bash
cd Mini-AI-Text-Analyzer
```

3. (Optional but recommended) Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Mac/Linux
```

4. Install dependencies:
```bash
pip install nltk textblob
```

5. Run the app:
```bash
python main.py
```

---

## 🧪 Example Inputs to Test

| Type | Example Text |
|---|---|
| Negative | "This product is terrible. It broke after one day and customer support was useless." |
| Spelling errors | "She wass verry hapy abut her excelent performanse in the competision." |
| Mixed | "The weather was cold but the children played joyfully outside, laughing without a care." |

---

## 📁 Project Structure

Mini-AI-Text-Analyzer/
│
├── main.py
├── report.txt
├── README.md
└── screenshots/

---

## ⚙️ Features

- 🔤 **Spell Correction** using TextBlob
- 🧹 **Text Processing** — lowercasing, punctuation removal, stopword filtering
- 💬 **Sentiment Analysis** with polarity score and visual bar
- 📊 **Word Count** and **Unique Word Count**
- 💾 **Auto-saves** every analysis to `report.txt`
- 🎨 **Clean light-themed GUI** built entirely with Tkinter

---

## ⚠️ Known Limitations

- TextBlob's spell correction can be **slow** on longer texts (this is normal — please wait)
- Spell correction is not always 100% accurate — it is a simple statistical model
- Sentiment analysis works best on **English text** only
- This is a **learning project** — edge cases may not be handled perfectly
- The app window is fixed size and not responsive

---

## 🤝 Contributing

This is a personal learning project but if you have suggestions or spot a bug, feel free to open an issue or pull request. All feedback is appreciated!

---


## 👤 Author

Warisha Amjad

