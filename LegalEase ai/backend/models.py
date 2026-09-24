from typing import Literal

from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=1)
    parties: str = Field(min_length=1)
    terms: str = Field(min_length=1)
    effective_date: str
    additional_instructions: str = ""


class ExportRequest(BaseModel):
    text: str = Field(min_length=1)
    document_type: str = "Legal Document"
    format: Literal["txt", "docx", "pdf"]
    terms: list[str] = Field(default_factory=list)
    logo_base64: str | None = None