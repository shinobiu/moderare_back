import httpx
from fastapi import HTTPException
from core.config import settings


TURNSTILE_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


async def verify_captcha(token: str):

    async with httpx.AsyncClient() as client:
        response = await client.post(
            TURNSTILE_URL,
            data={
                "secret": settings.SITE_SECRET,
                "response": token,
            },
        )

    result = response.json()

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail="Captcha inválido"
        )