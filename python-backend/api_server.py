# api_server.py
import asyncio
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crawler import WebCrawler
from parser import WebParser
from extractor import ContentExtractor
from generator import MarkdownSpecGenerator
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://render-recorn.vercel.app"], # Your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic logger setup
logger = logging.getLogger("webagent_api")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

class GenerateRequest(BaseModel):
    target_url: str


class GenerateResponse(BaseModel):
    structure_md: str
    design_md: str
    usecase_md: str
    status: str


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
async def generate_docs(req: GenerateRequest):
    logger.info(f"[generate] Incoming request for URL: {req.target_url}")

    # Basic validation
    if not req.target_url.startswith(("http://", "https://")):
        logger.warning(f"[generate] Invalid URL format: {req.target_url}")
        raise HTTPException(status_code=400, detail="Invalid URL. Must start with http:// or https://")

    try:
        # Crawl
        logger.info(f"[generate] Starting crawler for: {req.target_url}")
        crawler = WebCrawler(start_url=req.target_url, max_pages=6)
        pages_data = await crawler.crawl()

        if not pages_data:
            logger.warning(f"[generate] No pages_data returned for: {req.target_url}")
            raise HTTPException(
                status_code=502,
                detail="Crawler could not fetch any content from the target URL. "
                       "The site may be blocking automated access or is unreachable."
            )

        # Process telemetry and content
        logger.info("[generate] Extracting telemetry and content corpus")
        telemetry = WebParser.extract_telemetry(pages_data)
        copy_corpus = ContentExtractor.extract_copy_block(pages_data)

        # Generate docs in memory
        logger.info("[generate] Invoking MarkdownSpecGenerator")
        generator = MarkdownSpecGenerator()
        docs = await generator.generate_documents_in_memory(req.target_url, telemetry, copy_corpus)

        structure_md = docs.get("structure_md", "")
        design_md = docs.get("design_md", "")
        usecase_md = docs.get("usecase_md", "")

        if not (structure_md and design_md and usecase_md):
            logger.error("[generate] One or more markdown docs empty after generation")
            raise HTTPException(
                status_code=500,
                detail="AI generation returned empty outputs. Please try again or contact support."
            )

        logger.info("[generate] Successfully generated all markdown specs")
        return GenerateResponse(
            structure_md=structure_md,
            design_md=design_md,
            usecase_md=usecase_md,
            status="success",
        )

    except HTTPException as http_exc:
        # Already structured; FastAPI will send JSON {detail: ...}
        logger.error(f"[generate] HTTPException: {http_exc.detail}")
        raise

    except Exception as e:
        logger.exception(f"[generate] Unexpected server error for URL {req.target_url}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal error while processing the target URL. Please try again later."
        )