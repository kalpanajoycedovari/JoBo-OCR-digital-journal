# 🌼 JoBo — OCR Digital Journal

> *A cozy, AI-powered journaling app that brings your handwritten notes to life.*

![Python](https://img.shields.io/badge/Python-3.10+-3a7a40?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55-66bb6a?style=for-the-badge&logo=streamlit&logoColor=white)
![Tesseract](https://img.shields.io/badge/Tesseract_OCR-5.0-a5d6a7?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-dcedc8?style=for-the-badge)

---

## ✨ What is JoBo?

JoBo is a digital journaling application that uses **Optical Character Recognition (OCR)** and **AI-powered sentiment analysis** to transform your handwritten or printed notes into searchable, organised digital entries — all wrapped in a soft, cozy pastel green UI with floating daisies. 🌿

---

🖼️ Features

| Feature | Description |

| 📷 **Image Upload** | Upload photos or scans of handwritten notes |
| 🔍 **OCR Extraction** | Automatically extract text using Tesseract OCR |
| 🧹 **Image Preprocessing** | OpenCV pipeline for denoising, thresholding & deskewing |
| 💾 **Secure Storage** | Save entries to a local SQLite database |
| 🔎 **Keyword Search** | Find any entry instantly by keyword |
| 😊 **Mood Analysis** | AI sentiment analysis on every journal entry |
| 🌸 **Mood Overview** | See your emotional trends across all entries |
| ✏️ **Edit Before Saving** | Review and correct OCR output before saving |
| 🗑️ **Delete Entries** | Remove entries you no longer need |
| ☁️ **Cloud Deployed** | Fully deployed and accessible from anywhere |

---

## Tech Stack

- **Python 3.10+**
- **Streamlit** — web UI framework
- **Tesseract OCR** — text extraction engine
- **OpenCV** — image preprocessing
- **TextBlob / NLTK** — sentiment analysis
- **SQLite** — local database storage
- **Pillow** — image handling
- **NumPy** — numerical processing

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed on your system

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/kalpanajoycedovari/JoBo-OCR-digital-journal.git
cd JoBo-OCR-digital-journal
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

**4. Configure Tesseract path (Windows only)**

In `jobo/ocr_engine.py`, make sure this line points to your Tesseract install:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

**5. Run the app**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` and start journaling! 🌼

---

## 📁 Project Structure

```
JoBo-OCR-digital-journal/
│
├── jobo/
│   ├── __init__.py
│   ├── preprocessor.py     # OpenCV image preprocessing pipeline
│   ├── ocr_engine.py       # Tesseract OCR text extraction
│   ├── database.py         # SQLite database operations
│   ├── models.py           # JournalEntry data model
│   ├── search.py           # Keyword & date search
│   └── sentiment.py        # TextBlob sentiment analysis
│
├── uploads/                # Uploaded images (gitignored)
├── outputs/                # Exported text files (gitignored)
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
│
├── app.py                  # Main Streamlit application
├── packages.txt            # System packages for Streamlit Cloud
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🔄 How It Works

```
📸 Upload Image
      ↓
🧹 Preprocess (grayscale → denoise → threshold → deskew)
      ↓
🔍 OCR Extraction (Tesseract)
      ↓
😊 Sentiment Analysis (TextBlob)
      ↓
💾 Save to Database (SQLite)
      ↓
🌸 View, Search & Explore
```

---

## ☁️ Deployment

JoBo is deployed on **Streamlit Cloud**.

To deploy your own instance:

1. Push this repository to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **New app** and connect your repository
4. Set **Main file path** to `app.py`
5. Click **Deploy** — Streamlit Cloud handles the rest!

> Tesseract is automatically installed on the server via `packages.txt`.

---

## 🗺️ Roadmap

- [x] Core OCR pipeline
- [x] Image preprocessing
- [x] SQLite storage
- [x] Keyword search
- [x] Sentiment analysis
- [x] Cozy diary UI with animations
- [x] Cloud deployment
- [ ] Filter entries by date
- [ ] Export journal as PDF
- [ ] Multi-language OCR support
- [ ] User authentication
- [ ] Mood trend chart over time

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

Made with 🌿 and lots of ☕ Joyce

> *"Every thought deserves to be remembered."*

---

<div align="center">
  <img src="https://img.shields.io/badge/Made%20with-Streamlit-66bb6a?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Powered%20by-Tesseract_OCR-a5d6a7?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Vibes-Cozy%20%F0%9F%8C%BC-dcedc8?style=for-the-badge"/>
</div>
