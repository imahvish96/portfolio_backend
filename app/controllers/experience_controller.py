import logging
from fastapi import Form
from app.services.experience_service import get_experience_service, add_experience_service, update_experience_service, delete_experience_service;
from app.schemas.experience_schema import ExperienceCreate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)

async def get_experience():
    try:
        response = await get_experience_service()
        return JSONResponse(
            status_code= 201,
            content=jsonable_encoder(
                {
                    "status": True,
                    "message": "Record Fetched Successfully",
                    "data": response
                }
            )
        );
    except Exception:
        logger.exception("Error while adding experience")
        raise;
    
async def add_experience(experience_data: ExperienceCreate):
    try:
        response = await add_experience_service(experience_data)
        return JSONResponse(
            status_code= 201,
            content=jsonable_encoder(
                {
                    "status": True,
                    "message": "Experience Added Successfully",
                    "data": response
                }
            )
        );
    except Exception:
        logger.exception("Error while adding project")
        raise;
    

async def update_experience(experience_data: ExperienceCreate, id:int):
    try:
        response = await update_experience_service(experience_data, id)
        return JSONResponse(
            status_code= 200,
            content=jsonable_encoder(
                {
                    "status": True,
                    "message": "Project Updated Successfully",
                    "data": response
                }
            )
        );
    except Exception:
        logger.exception("Error while adding project")
        raise;
    
async def delete_experience(id:int):
    try:
        response = await delete_experience_service(id)
        return JSONResponse(
            status_code= 200,
            content=jsonable_encoder(
                {
                    "status": True,
                    "message": "Project Deleted Successfully",
                    "data": response
                }
            )
        );
    except Exception:
        logger.exception("Error while adding project")
        raise;