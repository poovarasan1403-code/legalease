from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from backend.config import (
    get_settings
)

from backend.routes import (
    router
)


settings = get_settings()


app = FastAPI(

    title=settings.app_name,

    version="1.0.0",

    description=(
        "AI-assisted legal document "
        "drafting and export API."
    )
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=settings.origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# ROUTES
# =========================================================

app.include_router(
    router
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def root():

    return {

        "service": "LegalEase",

        "status": "running",

        "docs": "/docs",

        "health": "/health"
    }