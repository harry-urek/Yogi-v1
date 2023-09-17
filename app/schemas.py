from pydantic import BaseModel
from typing import List




class DetailBase(BaseModel):
    plant_family: str
    plant_bio: str
    plant_descr: str
    plant_url: str
    
    class config:
        orm_mode = True

class PlantBase(BaseModel):
    plant_text:str
    choices: List[DetailBase]
    
    class Config:
        orm_mode = True
        
class UserOut(BaseModel):
    id: int
    email: str
    

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    