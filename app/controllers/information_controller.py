import logging

logger = logging.getLogger(__name__);
from fastapi import Form, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.information_service import get_information_service, add_personal_information_service, update_information_service, remove_information_service
from app.schemas.information_schema import Information
from app.config.upload import save_upload

async def get_information():
    return await get_information_service()

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
        skill_urls = [await save_upload(file) for file in skils]

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
    profile_summary: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    skils: list[str] = Form(...),
        profile_image: UploadFile = File(...),
    resume_url: UploadFile = File(...),
):
    try:
        profile = await save_upload(profile_image);
        resume = await save_upload(resume_url);
        information_data = Information(
            profile_summary=profile_summary,
            email=email,
            message=message,
            skills=skils,
            profile=profile,
            resume=resume
        )
        response = await update_information_service(information_data)
        return response
    except Exception as Error:
        print("Controller Error", Error)

async def remove_information(id: int):
    try: 
        response = await remove_information_service(id);
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
    except Exception:
        logger.exception("Something went wrong in controller")
        raise