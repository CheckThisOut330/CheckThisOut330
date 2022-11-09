import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from modules.database import Database
from modules.model import RoomCount

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.post("/api/")
async def api(item: RoomCount):
    Database().set_count(item.room, item.count)
    return {"status": "ok", "room": item.room, "count": item.count}

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,
                                                    "title": "CheckThisOut330"})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4, log_level="info")