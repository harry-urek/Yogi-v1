from fastapi import FastAPI, File, HTTPException, Depends, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .schemas import DetailBase, PlantBase, UserCreate, UserOut
from PIL import Image
from .models import Plants, Details, User
from sqlalchemy.orm import Session
from .db import get_db
from fastapi_sqlalchemy import DBSessionMiddleware
from datetime import datetime
import io
import os

from .helper import predict
load_dotenv(".env")



app = FastAPI()
# app.add_middleware(DBSessionMiddleware, db_url = os.environment["DATABASE_URL"])


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/plants/{plant_id}")
async def read_plant(plant_id: int, db: Session = Depends(get_db)):
    if (
        result := db.query(Plants)
        .filter(Plants.id == plant_id)
        .first()
    ):
        return result
    else:
        raise HTTPException(status_code=404, detail='Plants is not found')




@app.get("/details/(plant_id)")
async def read_detail(plant_id: int, db: Session = Depends(get_db)):
    if (
        result := db.query(Details)
        .filter(Details.plant_id == plant_id)
        .first()
    ):
        return result
    else:

        raise HTTPException(status_code=404, detail='Details not found')

@app.post("/plants/")
async def create(plant: PlantBase, db: Session = Depends(get_db)):
    db_plant = Plants(plant_text = plant.plant_text)
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    for choice in plant.choices:
        db_choice = Details(plant_family=choice.plant_family, plant_bio=choice.plant_bio, plant_descr=choice.plant_descr, plant_url= choice.plant_url, plant_id=db_plant.id)
        db.add(db_choice)
    db.commit()



@app.post("/plants")
async def create_plant(plant_text: PlantBase, db: Session = Depends(get_db)):
    db_plant = Plants(**plant_text.dict())

    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return {"plant_text": plant_text}



@app.post("/plants_details")
async def create_plant_details(plant: DetailBase, db: Session = Depends(get_db)):
    db_plant = Details(**plant.dict())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)

    return db_plant


@app.post("/predict_plant")
async def predict_plant(img_file: UploadFile ):
    # image = await file.read()
    image_bytes = img_file.file.read()
    
    return predict(image_bytes)

@app.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
