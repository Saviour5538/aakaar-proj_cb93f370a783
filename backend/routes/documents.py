from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database.models import Document
from database.config import get_db
from backend.services.auth import get_current_user, get_current_user_id

router = APIRouter(prefix="/documents")


class DocumentResponse(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    filename: str
    status: str
    chunk_count: Optional[int] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True


@router.post("/upload", operation_id="upload_document", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_id),
):
    try:
        # Simulated service logic for uploading a document
        document = Document(
            user_id=current_user,
            filename=file.filename,
            status="uploaded",
            chunk_count=0,
            created_at=datetime.utcnow()
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", operation_id="list_documents", response_model=List[DocumentResponse])
async def list_documents(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_id),
):
    try:
        # Simulated service logic for listing documents
        documents = db.query(Document).filter(Document.user_id == current_user).all()
        return documents
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{id}", operation_id="delete_document", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_id),
):
    try:
        # Simulated service logic for deleting a document
        document = db.query(Document).filter(Document.id == id, Document.user_id == current_user).first()
        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        db.delete(document)
        db.commit()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))