from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    transactions = relationship("Transaction", back_populates="owner")

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sell_price = Column(Integer)
    buy_price = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    stockTransactions = relationship("Transaction", back_populates="stockType")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String)
    price = Column(Integer)
    quantity = Column(Float)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    stockType_id = Column(Integer, ForeignKey("stocks.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="transactions")
    stockType = relationship("Stock", back_populates="stockTransactions")
