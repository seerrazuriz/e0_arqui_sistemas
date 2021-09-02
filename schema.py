from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    nickname: str
    email: str
    password: str

    class Config:
        orm_mode = True

class Stock(BaseModel):
    name: str
    sell_price: int
    buy_price: int

    class Config:
        orm_mode = True

class Transaction(BaseModel):
    stockType_id: int
    owner_id: int
    quantity: float

    class Config:
        orm_mode = True