# Bookmark AI — Smarter Search for Your Saved Links

Tired of saving hundreds of bookmarks and forgetting why you saved them in the first place?  
**Bookmark AI** lets you semantically search through your Chrome bookmarks using natural language — not just keywords or page titles!

---

## Features

- **One-click semantic search** over your saved bookmarks  
- Powered by **Google Gemini embeddings** and **FAISS vector search**
- Extracts **real content** from bookmarked pages (not just titles)
- Understands your questions even if you forgot the exact wording
- Works across **all folders** in your Chrome bookmarks
- FastAPI backend with Chrome Extension frontend

---

## How It Works

1. **Fetches** your saved Chrome bookmarks
2. **Scrapes** the content + titles of each URL using `BeautifulSoup`
3. **Embeds** that text using `GoogleGenerativeAIEmbeddings`
4. **Stores** them in a local FAISS vector database
5. You can now **ask natural questions**, and get relevant bookmark links — even if the title doesn't match exactly!

---

## Tech Stack

| **Component**                | **Technology**                                                                 |
|-----------------------------|---------------------------------------------------------------------------------|
| **Frontend (Chrome Extension)** |                                                                                 |
| Language                    | JavaScript                                                                     |
| APIs                        | Chrome Bookmark API                                                             |
| UI Library                  | Semantic UI                                                                     |
| Rendering                   | DOM manipulation/rendering                                                      |
| **Backend**              |                                                                                 |
| Framework                   | Python + FastAPI                                                                |
| Web Requests                | [`httpx`](https://www.python-httpx.org/)                                       |
| Web Scraping                | [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/)              |
| LLM Orchestration           | [`langchain`](https://www.langchain.com/)                                      |
| Vector DB                   | [`FAISS`](https://github.com/facebookresearch/faiss)                           |
| Embeddings                  | [`GoogleGenerativeAIEmbeddings`](https://python.langchain.com/docs/integrations/text_embedding/google_generative_ai/) |


---

## Screenshots

![image](https://github.com/user-attachments/assets/20d678ac-9ef4-4897-9329-cc5a7eeb7093)

![image](https://github.com/user-attachments/assets/9a782657-1101-4f48-97af-5e0c16acfed0)


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
