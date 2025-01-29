from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .auth.auth_routes import router as auth_router
from .notes.notes_routes import router as notes_router
from .notes.notes_service import router as notes_service_router

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
app.include_router(notes_router, prefix="/notes", tags=["Notes"])
app.include_router(notes_service_router, prefix="/notes_service", tags=["Notes Service"])



@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("multiform.html", {"request": request})
