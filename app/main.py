from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import contact, events, gallery, members
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API de la vitrine de la Clique de Doissin.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"name": settings.app_name, "docs": "/docs"}


@app.get("/api/v1/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(members.router, prefix="/api/v1/members", tags=["members"])
app.include_router(gallery.router, prefix="/api/v1/gallery", tags=["gallery"])
app.include_router(contact.router, prefix="/api/v1/contact", tags=["contact"])
