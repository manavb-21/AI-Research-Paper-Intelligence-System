import logging
from typing import Any

from fastapi import FastAPI, HTTPException

from src.engine import EngineError, initialize_system, process_query

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
def startup_event() -> None:
    """Initialize backend resources when the FastAPI application starts."""
    logger.info('FastAPI startup started')
    try:
        initialize_system()
    except EngineError:
        logger.exception('Engine initialization failed during startup')
        raise
    except Exception:
        logger.exception('Unexpected startup failure')
        raise
    logger.info('FastAPI startup complete')


@app.get("/api/search")
def search(query: str, k: int = 3) -> dict[str, Any]:
    """Search research papers and return a generative summary with top paper metadata."""
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty")

    logger.info('Search request received: query=%s, k=%d', query, k)

    try:
        return process_query(query, k=k)
    except EngineError as exc:
        logger.exception('Search request failed: %s', exc.message)
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except Exception as exc:
        logger.exception('Unexpected search request failure')
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing query",
        ) from exc


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "healthy"}
