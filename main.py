import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import Stock, User, Transaction

from schema import Stock as SchemaStock, User as SchemaUser, Transaction as SchemaTransaction
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get("/")
async def index():
    return {"message": "Hola amigue"}

@app.post("/add_stock", response_model=SchemaStock)
async def add_stock(stock:SchemaStock):
    db_stock = Stock(name=stock.name, sell_price=stock.sell_price, buy_price=stock.buy_price)
    db.session.add(db_stock)
    db.session.commit()
    return db_stock

@app.get("/stocks")
async def get_stocks():
    stocks = db.session.query(Stock).all()

    return stocks

@app.get("/my_stocks/{user_id}")
async def get_user_stocks(user_id):
    transactions = db.session.query(Transaction).filter(Transaction.owner_id == user_id).all()
    stocks = db.session.query(Stock).all()
    stocks_names = {}
    for stock in stocks:
        stocks_names[stock.id] = [stock.name, 0]
    
    for transaction in transactions:
        if transaction.transaction_type == 'buy':
            stocks_names[transaction.stockType_id][1] += float(transaction.quantity) 
        else:
            stocks_names[transaction.stockType_id][1] -= float(transaction.quantity)

    return dict(stocks_names.values())

@app.get("/users")
async def get_users():
    users = db.session.query(User).all()

    return users

@app.post("/sign_up", response_model=SchemaUser)
async def add_user(user:SchemaUser):
    db_user = User(nickname=user.nickname, email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user

@app.delete("/delete_user/{user_id}")
async def delete_user(user_id):
    db.session.query(User).filter(User.id == user_id).delete()
    db.session.commit()
    return {'message': 'user deleted succesfuly'}

@app.post("/buy_stock", response_model=SchemaTransaction)
async def buy_stock(transaction:SchemaTransaction):
    stock = db.session.query(Stock).filter(Stock.id == transaction.stockType_id).first()
    db_transaction = Transaction(stockType_id=transaction.stockType_id, owner_id=transaction.owner_id,
     transaction_type='buy', price=stock.buy_price, quantity=transaction.quantity)
    db.session.add(db_transaction)
    db.session.commit()
    return db_transaction

@app.post("/sell_stock", response_model=SchemaTransaction)
async def sell_stock(transaction:SchemaTransaction):
    stock = db.session.query(Stock).filter(Stock.id == transaction.stockType_id).first()
    db_transaction = Transaction(stockType_id=transaction.stockType_id, owner_id=transaction.owner_id,
     transaction_type='sell', price=stock.sell_price, quantity=transaction.quantity)
    db.session.add(db_transaction)
    db.session.commit()
    return db_transaction

@app.get("/transactions")
async def get_transactions():
    transactions = db.session.query(Transaction).all()

    return transactions

@app.get("/my_transactions/{user_id}")
async def get_user_transactions(user_id):
    transactions = db.session.query(Transaction).filter(Transaction.owner_id == user_id).all()
    stocks = db.session.query(Stock).all()
    stocks_names = {}
    for stock in stocks:
        stocks_names[stock.id] = stock.name
    for transaction in transactions:
        transaction.stockType_id = stocks_names[transaction.stockType_id]
    return transactions
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)