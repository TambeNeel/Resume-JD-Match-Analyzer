# 🌟 Resume and Job Description Match Analyzer

This project is a multi-agent resume-job match analysis tool built with Streamlit and powered by:

* OpenAI (GPT-3.5)
* Anthropic Claude (Haiku)

It compares a candidate's resume to a job description, scores it across key areas and suggests improvements.

---

## 🔧 Features

* Upload resume and job description (PDF, DOCX, TXT)
* Analyze match using both OpenAI and Claude
* Score comparison table: Skills, Experience, Education, Overall
* Side-by-side improvement suggestions
* One-click resume comparison output

---

## 📂 Folder Structure

```bash
/
├── app.py                  # Main Streamlit application
├── .env                    # API keys
├── requirements.txt        # Python dependencies
├── README.md               # This file
```

---

## 📊 Example Output

* Match score comparison table with OpenAI and Claude
* Side-by-side improvement suggestions
* Side-by-side Resume and JD Detailed Explanation

---

## 📅 Requirements

* Python 3.8+
* OpenAI API Key
* Anthropic API Key

---

## 🔎 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Resume-JD-Match-Analyzer.git
cd Resume-JD-Match-Analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

---

## 🚫 .gitignore Suggestions

```bash
.env
__pycache__/
*.pyc
*.DS_Store
```

---

## 📑 requirements.txt

```txt
streamlit
python-dotenv
PyPDF2
python-docx
openai
anthropic
```

---

## 🚀 Future Ideas

* Add Gemini/Google API support
* Export results as PDF/CSV
* Resume strength visualization

---

## 💼 License

This project is for educational and demo purposes.

---

## 🙌 Credits

Built by Neel Tambe using OpenAI, Anthropic Claude and Streamlit.
