from fastapi import security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY_SECRET = os.getenv("API_KEY")

api_key_header = APIKeyHeader(name="X-API-Key" , auto_error=False)

async def get_api_key(api_key: str = security(api_key_header)):
    if api_key == API_KEY_SECRET:
        return api_key
    raise HTTPException(
        status_code=401, detail="Unauthorised: Invalid X-API-Key"
    )