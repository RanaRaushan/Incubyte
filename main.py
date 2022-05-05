from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from db.database import create_db_and_tables
from word_app import add_word_exception_handlers
from word_app.routes import router as word_app_routers
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

# Adding word app router to include in the main app API
app.include_router(word_app_routers)

# Adding exception handler from word app
add_word_exception_handlers(app)


@app.on_event("startup")
async def startup():
    # create db tables
    await create_db_and_tables()


@app.get("/")
def main():
    return RedirectResponse(url="/word")

