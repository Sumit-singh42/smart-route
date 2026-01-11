from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from app.services.providers import provider_service, STATS
import traceback
import io
import pypdf

router = APIRouter()

@router.post("/api/parse-document")
async def parse_document(file: UploadFile = File(...)):
    """
    Parses an uploaded document (PDF or Text) and returns the extracted text.
    """
    try:
        contents = await file.read()
        filename = file.filename.lower()
        extracted_text = ""

        if filename.endswith(".pdf"):
            try:
                pdf_file = io.BytesIO(contents)
                reader = pypdf.PdfReader(pdf_file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            except Exception as e:
                print(f"Error parsing PDF: {e}")
                raise HTTPException(status_code=400, detail=f"Invalid PDF file: {str(e)}")
        
        else:
            # Assume text/code file
            try:
                extracted_text = contents.decode("utf-8")
            except UnicodeDecodeError:
                # Try latin-1 fallback
                extracted_text = contents.decode("latin-1")
        
        if not extracted_text.strip():
             return {"text": f"[No text extracted from {file.filename}]"}

        return {"text": extracted_text}

    except Exception as e:
        print(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@router.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
        messages = body.get("messages", [])
        
        if not messages:
            raise HTTPException(status_code=400, detail="Messages required")

        response = await provider_service.route_request(messages)
        return response

    except Exception as e:
        print(f"Error processing request: {e}")
        traceback.print_exc()
        # INCLUDE TRACEBACK IN RESPONSE SO VERIFY SCRIPT SEES IT
        full_error = f"{str(e)}\n\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=full_error)

@router.get("/api/stats")
async def get_stats():
    """
    Returns the real-time stats for the dashboard.
    """
    total = STATS["cache_hits"] + STATS["cache_misses"]
    hit_rate = round((STATS["cache_hits"] / total) * 100, 1) if total > 0 else 0
    
    return {
        "requests": STATS["total_requests"],
        "savings": round(STATS["total_savings"], 4),
        "hit_rate": hit_rate,
        "provider_groq": STATS.get("provider_groq", 0),
        "provider_local": STATS.get("provider_local", 0),
        "latest_request": STATS.get("latest_request", {
            "type": "Waiting...",
            "provider": "Waiting...",
            "timestamp": 0
        })
    }

@router.get("/health")
async def health():
    return {"status": "ok"}
