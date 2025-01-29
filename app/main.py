from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .auth.auth_routes import router as auth_router
from .notes.notes_routes import router as notes_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(notes_router, prefix="/notes", tags=["Notes"])


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("multiform.html", {"request": request})
