from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from config.db import conn
import psutil

app = APIRouter()

@app.get("/ping")
async def ping():
    '''
    PING PONG 😊
    '''
    return "PONG!"

@app.get("/stats")
async def stats():
    '''
    Shows Statistics of server
    
    - **Database stats**\n
    - **RAM usage**\n
    - **Cpu usage**
    '''

    process = psutil.Process()
    return {
        "version":2.0,
        "database":{
            "host":conn.HOST,
            "address":conn.address[0],
            "port":conn.address[1]
        },
        "server":{
            "ram":{
                "used":str(process.memory_info().rss / 1e+6)+" Mb",
            },
            "cpu":{
                "usage":str(process.cpu_percent())+" %"
            }
        }
    }