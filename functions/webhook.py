import requests
import json
from datetime import datetime, timezone
from config import constant

def send_webhook(title, description, color):
    if(constant.WEBHOOK_URI is None):return
    payload = json.dumps({
    "embeds": [
        {
            "title": title,
            "description": description,
            "color": color,
            "type": "rich",
            "timestamp":datetime.now(timezone.utc).isoformat(),
            "author":{
                "name":"Techquiz-Logs",
                "icon_url":"https://cdn.discordapp.com/attachments/821261326918615040/881058219584278528/WhatsApp_Image_2021-08-18_at_8.40.20_PM.jpeg"
            },
            "footer":{
                "text":"Event happened at"
            }
        }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': '__cfruid=3be88afa3e6ff8eb1c98b667caaa11471ab267c9-1630090212; __dcfduid=9be7d0fa076711eca26c42010a0a04ad; __sdcfduid=9be7d0fa076711eca26c42010a0a04adea71af91041b59faa2c137f1aff7f8ee10841d10a34206fa897ec3ea0c81dd60'
    }
    return requests.request("POST", constant.WEBHOOK_URI, headers=headers, data=payload)