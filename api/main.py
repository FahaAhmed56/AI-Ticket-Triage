"""Run: uvicorn api.main:app --reload"""
from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.model import TicketTriage

app=FastAPI(title='AI Ticket Triage API',version='1.0.0',description='Demo text classification, not production decision automation.')
class TicketRequest(BaseModel):
 text:str=Field(min_length=1,max_length=10000)

@lru_cache(maxsize=1)
def triage():return TicketTriage()

@app.get('/health')
def health():return {'status':'ok'}

@app.post('/predict')
def predict(req:TicketRequest):
 try:return triage().predict(req.text)
 except ValueError as err:raise HTTPException(status_code=422,detail=str(err)) from err
