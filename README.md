# Personalized Finance Agent  
*A multi-agent financial assistant built using Google Agent Developer Kit (ADK), Gemini 2.5, and Streamlit.*

This project implements a **stateful multi-agent system** for financial intelligence - capable of answering finance questions, retrieving real-time stock data, monitoring stock dips, performing mortgage calculations, extracting financial facts from the web, and maintaining contextual memory - all inside a clean and modern **Streamlit Chat UI**.

---

## Features

### 🔹 1. Multi-Agent Architecture (6 Specialized Agents)

This system uses a modular **master-router-executor** architecture:

#### **1️. RouterAgent**
Classifies user queries into categories:
- `STOCK`
- `MORTGAGE`
- `STOCK_MONITOR`
- `STOCK_STOCKMONITOR`
- `GENERIC_FINANCE`
- `ASK_CLARIFY`
- `OUT_OF_DOMAIN`

#### **2️. FinanceBrain (Master Controller)**
Orchestrates:
- workflow selection  
- multi-turn clarifications  
- parallel routing (e.g., stock + monitor)  
- dip threshold logic (calls calculator)

FinanceBrain **never answers directly** - it only coordinates.

#### **3️. StockAgent**
Retrieves:
- real-time stock prices  
- historical data  
- sector context  

Uses `get_stock_yahoo()` and safe insights - *no personal financial advice*.

#### **4️. MortgageAgent**
Handles:
- mortgage interest rate lookup  
- mortgage payment calculations  
- missing-rate fallback logic  

Uses Python code executor + interest extraction agent.

#### **5️. StockMonitoringAgent**
Controls:
- adding alerts  
- ensuring scheduler runs  
- checking existing alerts  

Strictly limited to tool calls only.

#### **6️. ToneAgent**
Final output refinement:
- clean formatting  
- friendly tone  
- does not alter numbers or facts  

---

## 🔹 2. Finance Information Extraction (Search-Based)

A specialized `FinanceInfoAgent` uses `google_search` to extract:
- mortgage rates  
- CPI, unemployment, GDP  
- interest rates  
- bank rates  
- bond yields  
- capital gains rules
- tax rates  

Always returns factual, web-extracted data.

---

## 🔹 3. Calculator Agent (Python Execution)

Handles all arithmetic:
- mortgage payment formulas  
- percentage dip → threshold calculations  
- financial math that must be computed in code  

Outputs ONLY Python code that is executed via ADK.

---

## 🔹 4. Stateful Memory via ADK Sessions

- Supports full multi-turn context  
- Preserves conversation history  
- Maintains stock alert logic consistently  

---

## 🔹 5. Streamlit Chat UI

A modern interactive UI:
- instant user message display  
- dynamic "🤖 Thinking…" loader  
- auto-update with agent response  
- clean light theme  
- scrollable message history  
- smooth ChatGPT-style interface  

---

##  Tech Stack

| Component | Technology |
|----------|------------|
| AI Engine | **Gemini 2.5 Flash Lite** |
| Agent Framework | **Google ADK** |
| Frontend | **Streamlit** |
| Backend | Python 3.10+ |
| State | ADK InMemorySessionService |

---


---

## Running the App

### **1. Install dependencies**

```bash
pip install -r requirements.txt
```
### **2. Add your API key**
Create .env and add Gemini API Key inside:

```bash
GENAI_API_KEY = "your-key-here"
```

### **3. Run the Streamlit chatbot**

```bash
streamlit run app.py
```

### **4. CLI version (for debugging)**

```bash
python MainAgent.py
```
## Example Interactions

### **Stock Price**

User: What is the current price of NVDA?


### **Mortgage**

User: Calculate my payment for a $500k home, 20% down, 5%, 25 years.


### **Stock Dip Alerts**

User: Alert me when TSLA drops by 12%.


### **General Finance**

User: What is the Bank of Canada prime rate right now?


---

## Why This System Is Standout

-> Fully modular multi-agent architecture  
-> Real-time stock retrieval  
-> Search-driven financial fact extraction  
-> Python-executed financial math  
-> Natural multi-turn conversation  
-> Clean Streamlit chatbot UI  
-> ADK-based workflow routing  
-> Production-ready structure  

---

## Future Enhancements

- Persistent DB for alerts  
- UI themes / dark mode toggle  
- User authentication  
- Portfolio simulation tools  
- Graphs & charts for stock history  

---

## Contributions

Open to pull requests, improvements, and new ideas.

---

## License

MIT License — feel free to use & modify.