from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import Base, engine
from .deps import get_optional_user
from .routers import auth, records

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Simple Web App", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.include_router(auth.router)
app.include_router(records.router)


@app.get("/", response_class=HTMLResponse)
def root(current_user=Depends(get_optional_user)):
    return RedirectResponse(url="/insert" if current_user else "/login")


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, current_user=Depends(get_optional_user)):
    if current_user:
        return RedirectResponse(url="/insert")
    return templates.TemplateResponse(request, "login.html")


@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request, current_user=Depends(get_optional_user)):
    if current_user:
        return RedirectResponse(url="/insert")
    return templates.TemplateResponse(request, "signup.html")


@app.get("/insert", response_class=HTMLResponse)
def insert_page(request: Request, current_user=Depends(get_optional_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(
        request, "insert.html", {"username": current_user.username, "active_page": "insert"}
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request, current_user=Depends(get_optional_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(
        request, "dashboard.html", {"username": current_user.username, "active_page": "dashboard"}
    )


@app.get("/health")
def health():
    return {"status": "ok"}
