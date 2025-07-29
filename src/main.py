from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import httpx
import os

load_dotenv()
app = FastAPI()

NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_URL = "https://api.nasa.gov/planetary/apod"

@app.get("/")
def root():
    return {"message": "Bem-vindo à Visualize API!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/apod")
async def get_apod():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(NASA_URL, params={"api_key": NASA_API_KEY})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Erro da API da NASA: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Erro de conexão com a API da NASA: {str(e)}")
