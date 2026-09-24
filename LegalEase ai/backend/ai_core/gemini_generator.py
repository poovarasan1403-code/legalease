from datetime import date

from backend.config import get_settings


class GeminiDocumentGenerator:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        additional_instructions: str,
    ) -> str:
        if self.settings.mock_ai:
            return self._mock_document(
                document_type,
                parties,
                terms,
                effective_date,
                additional_instructions,
            )

        if not self.settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        from google import genai

        client = genai.Client(api_key=self.settings.gemini_api_key)
        prompt = (
            "Draft a clear professional legal document. "
            f"Document type: {document_type}\n"
            f"Parties: {parties}\n"
            f"Terms: {terms}\n"
            f"Effective date: {effective_date}\n"
            f"Additional instructions: {additional_instructions}\n"
            "Include appropriate headings and complete clauses."
        )
        response = client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
        )
        if not response.text:
            raise RuntimeError("The AI returned an empty document")
        return response.text

    @staticmethod
    def _mock_document(
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        additional_instructions: str,
    ) -> str:
        instructions = additional_instructions or "None"
        return (
            f"{document_type.upper()}\n\n"
            f"Effective date: {effective_date or date.today().isoformat()}\n\n"
            f"PARTIES\n{parties}\n\n"
            f"TERMS\n{terms}\n\n"
            f"ADDITIONAL INSTRUCTIONS\n{instructions}\n\n"
            "This mock document is for local testing only and is not legal advice."
        )