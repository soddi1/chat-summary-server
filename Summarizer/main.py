from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from supabase_client import supabase

app = FastAPI()

class Message(BaseModel):
    sender: str
    channel_name: str
    message: str
    date: datetime

@app.post("/slack")
def insert_slack_msg(msg: Message):
    data = msg.dict()
    data['date'] = data['date'].isoformat()
    try:
        res = supabase.table("slack_messages").insert(data).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/discord")
def insert_discord_msg(msg: Message):
    data = msg.dict()
    data['date'] = data['date'].isoformat()
    try:
        res = supabase.table("discord_messages").insert(data).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/telegram")
def insert_telegram_msg(msg: Message):
    data = msg.dict()
    data['date'] = data['date'].isoformat()
    try:
        res = supabase.table("telegram_messages").insert(data).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
