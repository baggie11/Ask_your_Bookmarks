# Bookmark AI — Smarter Search for Your Saved Links

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)](https://fastapi.tiangolo.com/)
[![FAISS](https://img.shields.io/badge/FAISS-VectorDB-orange.svg)](https://github.com/facebookresearch/faiss)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-purple.svg)](https://www.langchain.com/)

Author: [Bagavati Narayanan](https://github.com/baggie11)

A semantic search engine for your Chrome bookmarks — powered by **AI embeddings**, **FAISS**, and **FastAPI**.  
Stop scrolling through endless bookmark lists — just ask what you remember, and Bookmark AI finds it instantly.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How-It-Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Screenshots](#screenshots)
- [Setup Instructions](#setup-instructions)

---

## Overview

**Bookmark AI** allows you to search your Chrome bookmarks using *natural language* rather than titles or keywords.  
It understands the *context* behind your saved pages by embedding the actual content and performing **semantic search**.

**Key Highlights:**
- Semantic retrieval over real bookmark content  
- Chrome Extension + FastAPI backend  
- Google Gemini embeddings + FAISS for similarity search  
- Works seamlessly across all bookmark folders  
- Blazing-fast query responses through local vector database

---

## Features

- **One-click semantic search** over saved bookmarks  
- **AI-powered understanding** of what you meant, not just what you typed  
- **Content-based indexing** — extracts page text, not only titles  
- **Full-folder coverage** — searches across your entire Chrome tree  
- **Lightweight and fast** — stores embeddings locally via FAISS  
- **Frontend + Backend integration** for real-time search

---

## How It Works

1. **Fetch Bookmarks**  
   - Uses Chrome’s Bookmark API to retrieve all saved links.  

2. **Extract Content**  
   - Scrapes title + body text of each URL using `BeautifulSoup`.  

3. **Generate Embeddings**  
   - Transforms page text into vector representations using  
     `GoogleGenerativeAIEmbeddings` (via LangChain).  

4. **Store in FAISS**  
   - Builds a local FAISS vector database for fast similarity queries.  

5. **Semantic Query**  
   - User enters a natural question → system retrieves the most relevant saved bookmarks, even if titles don’t match exactly.

---

## Tech Stack

| **Component** | **Technology** |
|----------------|----------------|
| **Frontend (Chrome Extension)** | |
| Language | JavaScript |
| APIs | Chrome Bookmark API |
| UI Library | Semantic UI |
| Rendering | DOM manipulation & dynamic rendering |
| **Backend** | |
| Framework | Python + FastAPI |
| HTTP Requests | [`httpx`](https://www.python-httpx.org/) |
| Web Scraping | [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/) |
| LLM Orchestration | [`LangChain`](https://www.langchain.com/) |
| Vector Database | [`FAISS`](https://github.com/facebookresearch/faiss) |
| Embeddings | [`GoogleGenerativeAIEmbeddings`](https://python.langchain.com/docs/integrations/text_embedding/google_generative_ai/) |

---



## Screenshots

![image](https://github.com/user-attachments/assets/20d678ac-9ef4-4897-9329-cc5a7eeb7093)

![image](https://github.com/user-attachments/assets/9a782657-1101-4f48-97af-5e0c16acfed0)

---

## Setup Instructions

### 🔌 Backend

```bash
# Clone the repo
git clone https://github.com/your-username/bookmark-ai.git
cd bookmark-ai/backend

# Install dependencies
pip install -r requirements.txt

Note: Use your Gemini API key by pasting it in app.py:

# Run the FastAPI server
uvicorn app:app --reload
