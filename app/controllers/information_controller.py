import logging

logger = logging.getLogger(__name__);
from fastapi import Form, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.information_service import get_information_service, add_personal_information_service, update_information_service, remove_information_service, get_information_skills_service
from app.schemas.information_schema import Information, InformationUpdate
from app.config.upload import save_upload, save_uploads, delete_uploads

async def get_information():
    try:
        response = await get_information_service()
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(
                {
                    "success": True,
                    "mssage": "Record Fetched Successfully",
                    "data": response
                }
            )
        )
    except Exception:
        logger.exception("Something Went Wrong")
        raise

async def add_information(
    profile_summary: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    skils: list[UploadFile] = File(...),
    profile_image: UploadFile = File(...),
    resume_url: UploadFile = File(...),

):
    try:
        profile = await save_upload(profile_image);
        resume = await save_upload(resume_url);
        skill_urls = await save_uploads(skils)

        information_data = Information(
            profile_summary=profile_summary,
            email=email,
            message=message,
            skills=skill_urls,
            profile=profile,
            resume=resume
        )
        response = await add_personal_information_service(information_data)
        return response
    except Exception as Error:
        print("Controller Error", Error)
    
async def update_information(
    id: int,
    profile_summary: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    skils: list[UploadFile] | None = File(None),
    existing_skils: list[str] | None = Form(None),
    profile_image: UploadFile | None = File(None),
    resume_url: UploadFile | None = File(None),
):
    try:
        # sirf tabhi upload karo jab nayi file aayi ho, warna None (purani value rahegi)
        profile = await save_upload(profile_image) if profile_image else None
        resume = await save_upload(resume_url) if resume_url else None

        # skills: agar dono field khali hain to skills touch nahi hua -> None (DB value rahegi)
        # warna final = rakhi hui URLs + sirf nayi files ke uploaded URLs
        orphan_skills = []
        if skils is None and existing_skils is None:
            final_skills = None
        else:
            uploaded_skill_urls = await save_uploads(skils) if skils else []
            final_skills = (existing_skils or []) + uploaded_skill_urls
            # diff: purani skills jo ab final list mein nahi -> baad mein bucket se delete
            old_skills = await get_information_skills_service(id) or []
            orphan_skills = [url for url in old_skills if url not in final_skills]

        information_data = InformationUpdate(
            profile_summary=profile_summary,
            email=email,
            message=message,
            skills=final_skills,
            profile=profile,
            resume=resume
        )
        response = await update_information_service(information_data, id)

        # DB update ho gaya -> ab orphan images bucket se hata do (best-effort)
        if orphan_skills:
            await delete_uploads(orphan_skills)

        return response
    except Exception:
        logger.exception("Something Went Wrong");
        raise;

async def remove_information(id: int):
    try:
        response = await remove_information_service(id);
        # id DB mein nahi mili -> None -> 404 do
        if response is None:
            raise HTTPException(
                status_code=404,
                detail=f"Information not found",
            )
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(
                {
                    "success": True,
                    "mssage": "Recoed deleted successfully",
                    "data": response
                }
            )

        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Something went wrong in controller")
        raise