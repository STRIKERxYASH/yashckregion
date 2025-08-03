from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

@app.get("/region")
async def get_region(request: Request):
    uid = request.query_params.get("uid")
    if not uid:
        return JSONResponse({"message": "Please provide a UID"})

    url = "https://shop2game.com/api/auth/player_id_login"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://shop2game.com",
        "Referer": "https://shop2game.com/app",
        "User-Agent": "Mozilla/5.0",
        "x-datadome-clientid": "10BIK2pOeN3Cw42~iX48rEAd2OmRt6MZDJQsEeK5uMirIKyTLO2bV5Ku6~7pJl_3QOmDkJoSzDcAdCAC8J5WRG_fpqrU7crOEq0~_5oqbgJIuVFWkbuUPD~lUpzSweEa"
    }

    payload = {
        "app_id": 100084,  # ✅ OB50 version
        "login_id": uid,
        "app_server_id": 0
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            data = response.json()

        if not data.get("nickname") and not data.get("region"):
            return JSONResponse({"message": "UID not found, please check the UID"})

        return {
            "uid": uid,
            "nickname": data.get("nickname", ""),
            "region": data.get("region", ""),
            "like": data.get("like", 0),
            "level": data.get("level", 0)
        }

    except Exception:
        return JSONResponse({"message": "UID not found, please check the UID"})
