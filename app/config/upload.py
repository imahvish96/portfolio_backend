import os
import uuid
import httpx
from fastapi import UploadFile, HTTPException

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")


async def save_upload(file: UploadFile) -> str:
    if not (SUPABASE_URL and SUPABASE_KEY and BUCKET_NAME):
        raise HTTPException(
            status_code=500,
            detail="Supabase env vars (SUPABASE_URL / SUPABASE_KEY / BUCKET_NAME) missing hain",
        )

    # file ka content bytes mein padho
    content = await file.read()

    # unique object name banao, original extension preserve karke
    ext = ""
    if file.filename and "." in file.filename:
        ext = "." + file.filename.rsplit(".", 1)[1].lower()
    object_path = f"{uuid.uuid4().hex}{ext}"

    base = SUPABASE_URL.rstrip("/")
    upload_url = f"{base}/storage/v1/object/{BUCKET_NAME}/{object_path}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": file.content_type or "application/octet-stream",
        # same path pe dobara upload ho to overwrite kar de
        "x-upsert": "true",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(upload_url, content=content, headers=headers)

    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=502,
            detail=f"Supabase upload failed: {response.status_code} {response.text}",
        )

    # public URL (agar bucket public hai to ye directly khulega)
    return f"{base}/storage/v1/object/public/{BUCKET_NAME}/{object_path}"
