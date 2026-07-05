from fastapi import FastAPI, HTTPException
from src.engine import initialize_system, process_query

app = FastAPI()


@app.on_event("startup")
def startup_event():
    initialize_system()


@app.get("/api/search")
def search(query: str, k: int = 3):
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty")

    try:
        summary = process_query(query, k=k)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error while processing query")

    return {"query": query, "generative_summary": summary}


@app.get("/health")
def health():
    return {"status": "healthy"}
