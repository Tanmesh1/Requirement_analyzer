from fastapi import APIRouter, Depends , UploadFile , File , HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app import models
from app.schemas import DocumentResponse
from app.utils.files import validate_file, extract_text
from app.models import DocumentText
from app.utils.text import normalize_text
from app.utils.pdf import extract_text_from_pdf
from app.models import ProcessingStatus

router = APIRouter(
    prefix="/documents",
    tags= ["Documents"]
)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    validate_file(file)
    file_bytes = await file.read()

    #content = await extract_text(file)

    document = models.Document(
        filename = file.filename,
        user_id = current_user.id,
        status = ProcessingStatus.uploaded
    )
   
    db.add(document)
    db.commit()
    db.refresh(document)

    try:
       
        document.status = ProcessingStatus.processing
        db.commit()

        if file.filename.lower().endswith(".pdf"):
            raw_text = extract_text_from_pdf(file_bytes)
        else:
            raw_text = file_bytes.decode("utf-8")
        

        if not raw_text.strip():
            raise ValueError("No extractable text found")
        
        normalized = normalize_text(raw_text)
        document_text = DocumentText(
            text = normalized,
            document_id = document.id
        )

        db.add(document_text)
        document.status = ProcessingStatus.processed
        db.commit()
        



    except Exception as e:
        print("🔥 REAL ERROR:", repr(e))
        document.status = ProcessingStatus.failed
        document.error_message = str(e)
        db.commit()

        raise HTTPException(
            status_code = 400,
            detail = "Document Processing Failed"
        )

    return document

