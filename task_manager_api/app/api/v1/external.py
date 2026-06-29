import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/external", tags=["external"])


@router.get("/uuid")
async def fetch_uuid() -> dict:
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get("https://httpbin.org/uuid")
        response.raise_for_status()
        data = response.json()
    return {"source": "httpbin", "uuid": data["uuid"]}
