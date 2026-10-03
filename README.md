# AI Resume Match Analyzer

A Streamlit-based resume and job-description matching application using Groq and Pydantic.
Helps user to know how fit he is for the role he applying for.

## Live Demo

https://resumeevaluator-9cezgnjfstcvz4bwpkjwpc.streamlit.app/

## Features

- Upload PDF/DOCX resume directly from UI
- Paste job description directly in UI
- Structured resume parsing
- Structured job-description parsing
- Resume-to-job matching
- Match percentage
- Matching skills
- Missing important skills
- Experience requirement status
- Verdict and summary
- Custom Streamlit CSS dashboard
- Modular VS Code-friendly architecture

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=your_key
GROQ_MODEL=openai/gpt-oss-120b
```

Run:

```bash
streamlit run app.py
```
