import base64
import html
import os
from datetime import date

import requests
import streamlit as st

from dotenv import load_dotenv


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# =========================================================
# PAGE
# =========================================================

st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .hero {

        padding: 1.5rem;

        border-radius: 15px;

        background:
        linear-gradient(
            135deg,
            #111827,
            #1f2937
        );

        color: white;

        margin-bottom: 1.5rem;

    }

    .hero h1 {

        margin-bottom: 0.2rem;

    }

    .hero p {

        color: #d1d5db;

    }

    .preview {

        background: #111827;

        color: #f3f4f6;

        border-radius: 12px;

        padding: 1.5rem;

        min-height: 400px;

        max-height: 650px;

        overflow-y: auto;

        font-family: Georgia, serif;

        line-height: 1.7;

        white-space: normal;

    }

    .disclaimer {

        font-size: 0.85rem;

        color: #6b7280;

        padding-top: 1.5rem;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">

        <h1>⚖️ LegalEase</h1>

        <p>
        AI-powered legal document drafting,
        editing and export.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "document" not in st.session_state:

    st.session_state.document = ""


if "terms" not in st.session_state:

    st.session_state.terms = []


if "doc_type" not in st.session_state:

    st.session_state.doc_type = (
        "Freelance Work Contract"
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header(
        "Document Details"
    )

    # ---------------------------------
    # DOCUMENT TYPE
    # ---------------------------------

    doc_type = st.text_input(

        "Document Type",

        value=st.session_state.doc_type,

        placeholder=(
            "Example: NDA"
        )
    )

    # ---------------------------------
    # PARTIES
    # ---------------------------------

    parties = st.text_area(

        "Parties Involved",

        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),

        height=120
    )

    # ---------------------------------
    # TERMS
    # ---------------------------------

    terms_text = st.text_area(

        "Terms & Conditions",

        placeholder=(
            "Payment within 30 days; "
            "Confidentiality must be maintained; "
            "Either party may terminate with "
            "15 days notice"
        ),

        height=180,

        help=(
            "Separate individual clauses "
            "with semicolons."
        )
    )

    # ---------------------------------
    # DATE
    # ---------------------------------

    effective_date = st.date_input(

        "Effective Date",

        value=date.today()
    )

    # ---------------------------------
    # EXTRA INSTRUCTIONS
    # ---------------------------------

    instructions = st.text_area(

        "Additional Instructions",

        placeholder=(
            "Use clear professional language. "
            "Include an IP ownership clause."
        ),

        height=120
    )

    # ---------------------------------
    # LOGO
    # ---------------------------------

    logo = st.file_uploader(

        "Optional Logo",

        type=[
            "png",
            "jpg",
            "jpeg"
        ],

        help=(
            "The logo will be included "
            "in DOCX and PDF exports."
        )
    )

    # ---------------------------------
    # GENERATE
    # ---------------------------------

    generate = st.button(

        "✨ Generate Document",

        type="primary",

        use_container_width=True
    )


# =========================================================
# GENERATION
# =========================================================

if generate:

    if not parties.strip():

        st.error(
            "Please enter the parties."
        )

    elif not terms_text.strip():

        st.error(
            "Please enter at least one term."
        )

    else:

        payload = {

            "document_type":
                doc_type.strip(),

            "parties":
                parties.strip(),

            "terms":
                terms_text.strip(),

            "effective_date":
                effective_date.isoformat(),

            "additional_instructions":
                instructions.strip()
        }

        with st.spinner(
            "Generating your document..."
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                st.session_state.document = (
                    result["text"]
                )

                st.session_state.terms = [

                    item.strip()

                    for item in (
                        terms_text
                        .replace("\n", ";")
                        .split(";")
                    )

                    if item.strip()
                ]

                st.session_state.doc_type = (
                    doc_type.strip()
                )

                st.success(
                    "Document generated successfully."
                )

            except requests.RequestException as exc:

                st.error(
                    "Could not connect to the "
                    "FastAPI backend."
                )

                st.info(
                    "Make sure the backend is running:"
                )

                st.code(
                    "uvicorn backend.main:app --reload"
                )

                st.caption(
                    str(exc)
                )


# =========================================================
# MAIN LAYOUT
# =========================================================

left, right = st.columns(
    [1.35, 1]
)


# =========================================================
# PREVIEW
# =========================================================

with left:

    st.subheader(
        "📄 Document Preview"
    )

    if st.session_state.document:

        safe_document = html.escape(

            st.session_state.document
        )

        safe_document = (
            safe_document
            .replace(
                "\n",
                "<br>"
            )
        )

        st.markdown(

            f"""
            <div class="preview">
                {safe_document}
            </div>
            """,

            unsafe_allow_html=True
        )

    else:

        st.info(
            "Generate a document and "
            "the preview will appear here."
        )


# =========================================================
# EDITOR
# =========================================================

with right:

    st.subheader(
        "✏️ Edit & Export"
    )

    edited_document = st.text_area(

        "Editable Document",

        value=st.session_state.document,

        height=520,

        label_visibility="collapsed"
    )

    if (
        edited_document
        != st.session_state.document
    ):

        st.session_state.document = (
            edited_document
        )


    # ---------------------------------
    # LOGO ENCODING
    # ---------------------------------

    logo_base64 = None

    if logo is not None:

        logo_base64 = base64.b64encode(

            logo.getvalue()

        ).decode(
            "ascii"
        )


    # =====================================================
    # EXPORT FUNCTION
    # =====================================================

    def export_document(format_name):

        if not st.session_state.document.strip():

            st.warning(
                "Generate a document first."
            )

            return None

        payload = {

            "text":
                st.session_state.document,

            "document_type":
                st.session_state.doc_type
                or doc_type,

            "format":
                format_name,

            "terms":
                st.session_state.terms,

            "logo_base64":
                logo_base64
        }

        response = requests.post(

            f"{BACKEND_URL}/export",

            json=payload,

            timeout=60
        )

        response.raise_for_status()

        return response


    # =====================================================
    # TXT
    # =====================================================

    try:

        if st.button(
            "Download TXT",
            use_container_width=True
        ):

            response = export_document(
                "txt"
            )

            if response:

                st.download_button(

                    "⬇ Save TXT File",

                    data=response.content,

                    file_name=(
                        "legalease_document.txt"
                    ),

                    mime="text/plain",

                    use_container_width=True
                )


        # =================================================
        # DOCX
        # =================================================

        if st.button(
            "Download DOCX",
            use_container_width=True
        ):

            response = export_document(
                "docx"
            )

            if response:

                st.download_button(

                    "⬇ Save DOCX File",

                    data=response.content,

                    file_name=(
                        "legalease_document.docx"
                    ),

                    mime=(
                        "application/"
                        "vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),

                    use_container_width=True
                )


        # =================================================
        # PDF
        # =================================================

        if st.button(
            "Download PDF",
            use_container_width=True
        ):

            response = export_document(
                "pdf"
            )

            if response:

                st.download_button(

                    "⬇ Save PDF File",

                    data=response.content,

                    file_name=(
                        "legalease_document.pdf"
                    ),

                    mime="application/pdf",

                    use_container_width=True
                )

    except requests.RequestException as exc:

        st.error(
            f"Export failed: {exc}"
        )


# =========================================================
# DISCLAIMER
# =========================================================

st.markdown(
    """
    <div class="disclaimer">

    ⚠️ LegalEase creates AI-assisted drafts for
    informational and document-preparation purposes.

    Generated content should be reviewed by a
    qualified legal professional and adapted to
    the applicable jurisdiction before signing
    or relying on it.

    </div>
    """,
    unsafe_allow_html=True
)