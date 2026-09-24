from fastapi import APIRouter, HTTPException

from fastapi.responses import Response

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator
)

from backend.models import (
    DocumentRequest,
    ExportRequest
)

from backend.services.document_service import (
    make_docx,
    make_pdf,
    make_txt
)


router = APIRouter(
    tags=["LegalEase"]
)


generator = GeminiDocumentGenerator()


# =========================================================
# HEALTH
# =========================================================

@router.get("/health")
def health():

    return {
        "status": "ok",
        "service": "LegalEase"
    }


# =========================================================
# GENERATE DOCUMENT
# =========================================================

@router.post("/generate")
def generate_document(
    request: DocumentRequest
):

    try:

        text = generator.generate_document(

            request.document_type,

            request.parties,

            request.terms,

            request.effective_date,

            request.additional_instructions
        )

        return {

            "success": True,

            "document_type":
                request.document_type,

            "text":
                text
        }

    except Exception as exc:

        raise HTTPException(

            status_code=502,

            detail=str(exc)

        ) from exc


# =========================================================
# EXPORT DOCUMENT
# =========================================================

@router.post("/export")
def export_document(
    request: ExportRequest
):

    try:

        # ---------------------------------
        # TXT
        # ---------------------------------

        if request.format == "txt":

            data = make_txt(
                request.text
            )

            media = "text/plain"

            filename = (
                "legalease_document.txt"
            )

        # ---------------------------------
        # DOCX
        # ---------------------------------

        elif request.format == "docx":

            data = make_docx(

                request.text,

                request.document_type,

                request.terms,

                request.logo_base64
            )

            media = (
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )

            filename = (
                "legalease_document.docx"
            )

        # ---------------------------------
        # PDF
        # ---------------------------------

        else:

            data = make_pdf(

                request.text,

                request.document_type,

                request.terms,

                request.logo_base64
            )

            media = (
                "application/pdf"
            )

            filename = (
                "legalease_document.pdf"
            )

        return Response(

            content=data,

            media_type=media,

            headers={
                "Content-Disposition":
                    f'attachment; filename="{filename}"'
            }
        )

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=f"Export failed: {exc}"

        ) from exc