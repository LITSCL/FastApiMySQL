from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routes.usuario_route import rutas_usuario

app: object = FastAPI(
    title = "API REST",
    description = "Es una simple API REST de prueba creada con el framework FastAPI",
    version = "1.0.0"
)

plantillas: object = Jinja2Templates(directory = "templates")

@app.get("/", response_class = HTMLResponse, tags = ["index"])
async def index(request: Request) -> object:
    return plantillas.TemplateResponse("index.html", {"request": request})

app.include_router(rutas_usuario)