import os
import hashlib
import asyncio
import httpx
from fastapi import UploadFile, HTTPException

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# har upload ke liye zyada time do (default 5s bahut kam tha)
UPLOAD_TIMEOUT = httpx.Timeout(60.0)


async def save_upload(file: UploadFile, client: httpx.AsyncClient | None = None) -> str:
    if not (SUPABASE_URL and SUPABASE_KEY and BUCKET_NAME):
        raise HTTPException(
            status_code=500,
            detail="Supabase env vars (SUPABASE_URL / SUPABASE_KEY / BUCKET_NAME) missing hain",
        )

    # file ka content bytes mein padho
    content = await file.read()

    # object name = file content ka sha256 hash (same image -> same naam)
    # isse duplicate content dobara upload ho to naya object nahi banta, wahi overwrite hota hai
    ext = ""
    if file.filename and "." in file.filename:
        ext = "." + file.filename.rsplit(".", 1)[1].lower()
    object_path = f"{hashlib.sha256(content).hexdigest()}{ext}"

    base = SUPABASE_URL.rstrip("/")
    upload_url = f"{base}/storage/v1/object/{BUCKET_NAME}/{object_path}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": file.content_type or "application/octet-stream",
        # same path pe dobara upload ho to overwrite kar de
        "x-upsert": "true",
    }

    # agar bahar se client mila to wahi reuse karo, warna apna banao
    own_client = client is None
    if own_client:
        client = httpx.AsyncClient(timeout=UPLOAD_TIMEOUT)
    try:
        response = await client.post(upload_url, content=content, headers=headers)
    finally:
        if own_client:
            await client.aclose()

    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=502,
            detail=f"Supabase upload failed: {response.status_code} {response.text}",
        )

    # public URL (agar bucket public hai to ye directly khulega)
    return f"{base}/storage/v1/object/public/{BUCKET_NAME}/{object_path}"


async def save_uploads(files: list[UploadFile]) -> list[str]:
    # saari files ko ek hi client se parallel upload karo (sequential nahi)
    async with httpx.AsyncClient(timeout=UPLOAD_TIMEOUT) as client:
        return await asyncio.gather(*[save_upload(f, client) for f in files])


def _object_path_from_url(url: str) -> str | None:
    # public URL: {base}/storage/v1/object/public/{bucket}/{object_path}
    marker = f"/object/public/{BUCKET_NAME}/"
    if marker in url:
        return url.split(marker, 1)[1]
    return None


async def delete_upload(url: str, client: httpx.AsyncClient | None = None) -> None:
    # ek object ko bucket se delete karo (best-effort; fail ho to sirf ignore)
    if not (SUPABASE_URL and SUPABASE_KEY and BUCKET_NAME):
        return
    object_path = _object_path_from_url(url)
    if not object_path:
        return

    base = SUPABASE_URL.rstrip("/")
    delete_url = f"{base}/storage/v1/object/{BUCKET_NAME}/{object_path}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }

    own_client = client is None
    if own_client:
        client = httpx.AsyncClient(timeout=UPLOAD_TIMEOUT)
    try:
        await client.request("DELETE", delete_url, headers=headers)
    finally:
        if own_client:
            await client.aclose()


async def delete_uploads(urls: list[str]) -> None:
    # saare orphan objects ko ek hi client se parallel delete karo
    if not urls:
        return
    async with httpx.AsyncClient(timeout=UPLOAD_TIMEOUT) as client:
        await asyncio.gather(*[delete_upload(u, client) for u in urls])
