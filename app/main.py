from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.exceptions import TokenExpiredException, TokenNoFoundException
from app.users.router import router as users_router
from app.chat.router import router as chat_router
from app.users.dependencies import get_current_user
from app.users.models import User
from fastapi.responses import HTMLResponse
from fastapi import FastAPI

app = FastAPI()
templates = Jinja2Templates(directory='app/templates')

app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.mount('/uploads', StaticFiles(directory='uploads'), name='uploads')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(chat_router)


@app.get("/")
async def landing_page(request: Request):
    # Пытаемся получить текущего пользователя
    try:
        user = await get_current_user(request)
        if user:
            return RedirectResponse(url="/chat")
    except:
        pass
    # Если пользователь не авторизован — показываем лендинг
    return templates.TemplateResponse("landing.html", {"request": request})


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")

@app.get("/google3926764af44d929c.html", response_class=HTMLResponse)
async def verify_google():
    # Укажите правильный путь к вашему файлу
    file_path = "google3926764af44d929c.html"
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)


#@app.get("/init-db")
#async def init_db():
#    from app.database import engine, Base
#    async with engine.begin() as conn:
#        await conn.run_sync(Base.metadata.create_all)
#    return {"message": "✅ Таблицы успешно созданы!"}

@app.get("/yandex_f0d033a5ab75c5a6.html", response_class=HTMLResponse)
async def verify_yandex():
    file_path = "app/static/yandex_f0d033a5ab75c5a6.html"
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)