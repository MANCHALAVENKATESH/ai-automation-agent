# 🤖 AI Browser Automation Agent

A powerful **local AI-powered browser automation agent** that understands natural language, executes browser tasks automatically, and improves over time using **RAG (Retrieval-Augmented Generation)** and **Fine-tuning**.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Ollama](https://img.shields.io/badge/Ollama-Llama3-green)
![Playwright](https://img.shields.io/badge/Playwright-Browser-orange)
![LangChain](https://img.shields.io/badge/LangChain-LLM-red)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Overview

This project is an **AI-powered autonomous agent** that can:

- Understand plain English tasks  
- Convert them into executable browser steps  
- Perform actions using a real browser  
- Learn from past executions using memory (RAG)  
- Improve performance using fine-tuning  

---

## 💡 Example

**Input:**
Open Amazon and search for mobiles and take a screenshot

**What happens:**
- Opens browser  
- Navigates to Amazon  
- Searches for mobiles  
- Takes screenshot  
- Saves memory for future tasks  

---

## 🧠 How It Works

User Input → Agent → RAG Memory → Step Generation → Execution → Logging

---

## ✨ Features

- 🧠 LLM Powered (Llama3 via Ollama)
- 🌐 Browser Automation (Playwright)
- 💾 Memory System (ChromaDB)
- 📚 RAG Pipeline
- 📝 Task Logging (TinyDB)
- 🔧 Fine-Tuning Support
- 🌍 Runs Locally (No Cloud)
- 🚀 API Support (Flask)
- 📸 Screenshot Capture

---

## 🛠️ Tech Stack

Python | Ollama | Llama3 | LangChain | ChromaDB | Playwright | TinyDB | Flask

---

## 📁 Project Structure

ai-automation-agent/
├── main.py
├── run_fine_tuning.py
├── requirements.txt
├── data/
├── screenshots/
└── app/

---

## ⚙️ Installation

git clone https://github.com/MANCHALAVENKATESH/ai-automation-agent.git
cd ai-automation-agent

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium

ollama pull llama3

---

## ▶️ Usage

ollama serve  
python main.py  

---

## 🧠 Fine-Tuning

python run_fine_tuning.py

---

## 🌐 API

Start server:
python app/api/routes.py

POST /run  
GET /history  
GET /stats  

---

## 📄 License

MIT License © 2026 Venkatesh Manchala
