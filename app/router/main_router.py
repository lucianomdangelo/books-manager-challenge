from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.router import books, comments


router = APIRouter(prefix="")

# Add all rotuers
router.include_router(books.router)
router.include_router(comments.router)

@router.get("/")
def root():
    return RedirectResponse(url=("/docs"))