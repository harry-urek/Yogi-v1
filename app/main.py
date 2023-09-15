from fastapi import FastAPI, HTTPException, Depends, Response, status
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

from .models import Plants , Details, User
from sqlalchemy.orm import Session
from .db import  get_db
from fastapi_sqlalchemy import DBSessionMiddleware
from datetime import datetime
import os
load_dotenv(".env")
app = FastAPI()
# app.add_middleware(DBSessionMiddleware, db_url = os.environment["DATABASE_URL"])

class DetailBase(BaseModel):
    plant_family: str
    plant_bio: str
    plant_descr: str
    plant_url: str
    
    class config:
        orm_mode = True

class PlantBase(BaseModel):
    plant_text: str
    choices: List[DetailBase]
    
    class config:
        orm_mode = True
        
class Plant(BaseModel):
    plant_text:str
    
    class config:
        orm_mode =True
        
class UserOut(BaseModel):
    id: int
    email: str
    

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    


@app.get("/plants/{plant_id}")
async def read_plant(plant_id: int, db: Session = Depends(get_db)):
    if (
        result := db.query(Plants)
        .filter(Plants.id == plant_id)
        .first()
    ):
        return result
    else:
        raise HTTPException(status_code=404, detail='Questions is not found')

@app.get("/details/(plant_id)")
async def read_detail(plant_id:int, db: Session = Depends(get_db)):
    if (
        result := db.query(Details)
        .filter(Details.plant_id == plant_id)
        .first()
    ):
        return result
    else:
        raise HTTPException(status_code=404, detail='Questions is not found')

@app.post("/plants", status_code=status.HTTP_201_CREATED, responses=Plant)
async def create_plant(plant_text:Plant, db: Session = Depends(get_db)):
    db_plant = Plants(plant_text)
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return plant_text


@app.post("/plants_details")
async def create_plant_details(plant: PlantBase, db: Session = Depends(get_db)):
    db_plant = Plants(**plant.dict())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    for choice in plant.choices:
        db_choice = Details(plant_family=choice.plant_family, plant_bio=choice.plant_bio, plant_descr=choice.plant_descr, plant_url= choice.plant_url, plant_id=db_plant.id)
        db.add(db_choice)
    db.commit()
    
@app.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user