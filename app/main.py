from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.auth.auth_routes import router as auth_router
from app.notes.notes_routes import router as notes_router

app = FastAPI(
    title="FastAPI Course :: EKKE: LBT_IM738G2",
    description="This is a `Simple Notes APP` API that demonstrates how to use FastAPI",
    version="0.0.0.1",
    contact={
        "name": "Mihaly Nyilas",
        "url": "http://dabzse.net",
        "email": "dr.dabzse+fastapi@gmail.com"
    },
    license_info={
        "name": "Licence: MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
)

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(notes_router, tags=["Notes"])


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
