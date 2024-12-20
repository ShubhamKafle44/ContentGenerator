from fastapi import FastAPI, Request, Depends

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import engine, get_db

import crud, models, database, utility, schemas

from starlette.concurrency import run_in_threadpool #This is for multithreading



app = FastAPI()


templates = Jinja2Templates(directory="templates")



@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate/")
async def generate_content(payLoad: schemas.GeneratePayload, db: Session = Depends(get_db)):
    generated_text = await run_in_threadpool(utility.generate_content, db, payLoad.topic)
    return{"generated_text": generated_text}

@app.post("/analyze/")
async def analyze_content(payLoad: schemas.AnalyzePayload, db: Session = Depends(get_db)):
    readability, sentiment = await run_in_threadpool(utility.analyze_content, db, payLoad.topic)
    return{"readability": readability, "sentiment": sentiment}

