#import fastapi framework to create backend server
from fastapi import FastAPI
#import middleware for enabling cross-origin resource sharing
from fastapi.middleware.cors import CORSMiddleware
#pydantic BaseModel to define the data structure of request body
from pydantic import BaseModel
#typing tools for clearer type hints
from typing import List
#async tools to handle parallel tasks like scraping multiple links
import asyncio
#HTTP client for asynchronous web requests(to fetch bookmark pages)
import httpx
#library to parse HTML contant and extract title/text
from bs4 import BeautifulSoup
#OS module to interact with the file system
import os
#to validate urls using standard url parsin
from urllib.parse import urlparse
from langchain_community.vectorstores import FAISS
#document odel to structure the text content before converting to vectors
from langchain_core.documents import Document
#google gemini embeddings model
from langchain_google_genai import GoogleGenerativeAIEmbeddings

#configure the embedding model
GEMINI_API_KEY = "GEMINI_API_KEY"

embedding_model = GoogleGenerativeAIEmbeddings(
    model = "models/embedding-001",
    google_api_key=GEMINI_API_KEY
)

'''This line sets up a connection to Google Gemini's text embedding model, allowing you to convert natural language text into numerical vectors for advanced AI use cases like search or retrieval.'''

#initialize the fastapi app and cors
app = FastAPI()
#allow frontend to interact with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], #allow all origins
    allow_credentials = True,
    allow_methods = ["*"], #allow all HTTP methods
    allow_headers = ["*"],
)

#define request models
class AskRequest(BaseModel):
    question : str

class BookmarkRefreshRequests(BaseModel):
    bookmarks : List[str]

#check if a url is valid
def is_valid_url(url:str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.scheme.startswith("http") and
        parsed.hostname is not None and
        parsed.hostname not in ("localhost", "127.0.0.1") and
        parsed.scheme != "chrome-extension"
    )

#extract text and title from a webpage
async def extract_text_and_title_from_url(url:str) -> dict:
    try:
        #async HTTP request to fetch the page content
        async with httpx.AsyncClient(timeout = 10) as client:
            resp = await client.get(url)
            soup = BeautifulSoup(resp.text,"html.parser")

            #remove unnecessary elements
            for tag in soup(["script", "style", "header", "footer", "nav", "noscript"]):
                tag.extract()
            
            #get the page title or fallback to untitled page
            title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled Page"

            #extract visible text(limit to 2000 chars for speed)
            content = soup.get_text(separator = " ",strip = True)[:2000]

            return {"url" : url,"title" :title,"content":content}
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return {"url": url, "title": "ERROR", "content": ""}


#refresh the FAISS index from bookmarks
@app.post("/refresh_index")
async def refresh_index(data : BookmarkRefreshRequests):
    #filter out only valid URLs
    urls = [url for url in data.bookmarks if is_valid_url(url)]
    #create a list of scraping tasks(run parallel)
    # Run all extract_text_and_title_from_url(url) coroutines concurrently and collect their results in order

    tasks = [extract_text_and_title_from_url(url) for url in urls]
    results = await asyncio.gather(*tasks)

    #convert each page into a langchain document
    docs = [
        Document(
            page_content=f"{item['title']}\n\n{item['content']}",
            metadata = {"source": item["url"], "title": item["title"]}
        )
        for item in results if item["content"]
    ]

    if not docs:
        return {"status": "❌ No valid content extracted."}
    
    #create a FAISS index from the documents and save locally
    os.makedirs("faiss_index",exist_ok=True)
    vectordb = FAISS.from_documents(docs, embeddings=embedding_model)
    vectordb.save_local("faiss_index")
    # Make sure the folder exists
# Build a FAISS index from documents using the embedding model
# Save the FAISS index and metadata to the "faiss_index" directory

    return {"status": "✅ Index refreshed."}

@app.post("/ask")
async def ask_question(data : AskRequest):
    #If no index exists,return empty
    if not os.path.exists("faiss_index"):
        return {"matching_urls" : []}
    
    #load existing faiss index
    vectordb = FAISS.load_local(
        "faiss_index",
        embeddings=embedding_model,
        allow_dangerous_deserialization=True  # Allow loading saved vector data
    )

    #search with similarity score, returns the top 10 matches
    results_with_scores = vectordb.similarity_search_with_score(data.question,k = 10)

    #sort results by score (lower = more similar) and extract URLs
    sorted_urls = [
        doc.metadata["source"]
        for doc,score in sorted(results_with_scores,key = lambda x :x[1])
        if "source" in doc.metadata
    ]

    return {"matching_urls" : sorted_urls}








