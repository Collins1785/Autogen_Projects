# 📘 **Autogen Interview Intelligence**  
### *A Multi‑Agent AI Interviewer, Coach & Evaluator System*

Autogen Interview Intelligence is an interactive, multi‑agent interview simulation system built using **Autogen**, **OpenAI models**, and **Streamlit**. It creates a realistic interview experience by generating role‑specific questions, evaluating user answers, providing structured feedback, and scoring responses — all in real time.

This project demonstrates how coordinated AI agents can work together to deliver a complete interview practice workflow, making preparation smarter, adaptive, and personalised.

---

## 🚀 **Features**

### 🔹 **Multi‑Agent Architecture**
The system uses three specialised agents:
- **Interviewer Agent** — Generates unique, role‑specific interview questions  
- **Coach Agent** — Provides concise, actionable feedback  
- **Evaluator Agent** — Scores answers on a 1–10 scale with justification  

### 🔹 **Role‑Aware Questioning**
Users select the job role in the sidebar, and the interviewer generates **non‑repeating questions** tailored to that role.

### 🔹 **Configurable Interview Length**
Choose between **1 to 5 questions** using a sidebar slider.

### 🔹 **Interactive Streamlit UI**
- Clean, responsive interface  
- Sidebar controls  
- Blue high‑contrast theme  
- Step‑by‑step interview flow  

### 🔹 **Final Summary Report**
At the end of the interview, users receive:
- All questions asked  
- Their answers  
- Feedback from the coach  
- Scores from the evaluator  
- An overall average score  

---

## 🧠 **How It Works**

### 1️⃣ User selects:
- Job role  
- Number of questions  

### 2️⃣ Interviewer Agent generates a **unique** question  
The system tracks previously asked questions to avoid repetition.

### 3️⃣ User submits an answer  
The Coach and Evaluator agents analyse it.

### 4️⃣ Feedback & Score displayed  
The user can move to the next question.

### 5️⃣ Final summary generated  
A complete breakdown of performance is shown.

---

## 🏗️ **Tech Stack**

| Component | Technology |
|----------|------------|
| UI | Streamlit |
| Agents | Autogen (AssistantAgent) |
| Model | OpenAI GPT‑4o‑mini |
| Environment | Python 3.10+ |
| Config | `.streamlit/config.toml` for theming |

---

## 📂 **Project Structure**

```
AUTOGEN/
│
├── autogen_AIinterviewer.py     # Main Streamlit app
├── .env                         # API keys
├── .streamlit/
│     └── config.toml            # Theme configuration
├── env/                         # Virtual environment (optional)
└── README.md                    # Project documentation
```

---

## ⚙️ **Setup Instructions**

### 1️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 2️⃣ Add your OpenAI API key  
Create a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

### 3️⃣ Run the Streamlit app
```
streamlit run autogen_AIinterviewer.py
```

---

## 🎨 **Theme Configuration**

Located in `.streamlit/config.toml`:

```
[theme]
primaryColor="#0D47A1"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#E3F2FD"
textColor="#000000"
font="sans serif"
```

This provides a clean, high‑contrast professional look.

---

## 🧪 **Why This Project Matters**

This project is a practical demonstration of:
- Multi‑agent reasoning  
- Tool‑free agent collaboration  
- Real‑time evaluation loops  
- Role‑adaptive content generation  
- Streamlit‑based AI UI design  

It’s ideal for:
- Interview preparation  
- AI‑powered learning tools  
- Demonstrating Autogen capabilities  
- Portfolio and community showcases  

---

## 📌 **Future Enhancements**

- Voice‑based interview mode  
- Difficulty levels (junior/mid/senior)  
- PDF export of interview summary  
- Multi‑round interview simulation  
- Behavioural + technical question modes  

---

## 🙌 **Credits**

Built by **Collins**  
Powered by **Autogen**, **OpenAI**, and **Streamlit**

