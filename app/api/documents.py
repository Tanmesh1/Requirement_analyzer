from fastapi import APIRouter, Depends , UploadFile , File
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app import models
from app.schemas import DocumentResponse
from app.utils.files import validate_file, extract_text
from app.models import DocumentText
from app.utils.text import normalize_text

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

    content = await extract_text(file)

    document = models.Document(
        filename = file.filename,
        user_id = current_user.id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    normalized = normalize_text(content)

    document_text = DocumentText(
        text = normalized,
        document_id = document.id
    )

    db.add(document_text)
    db.commit()

    return document

