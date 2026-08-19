import logging
from app.repositories.experience_respositories import fetch_experience, create_experience, update_experience,remove_experience
from app.schemas.experience_schema import ExperienceCreate

logger = logging.getLogger(__name__)

async def get_experience_service():
    try:
        return await fetch_experience()
    except:
        logger.exception("Something Went Wrong")
        raise
    
async def add_experience_service(data: ExperienceCreate):
    try:    
        return await create_experience(data)
    except Exception:
        logger.exception("Something Went Wrong");
        raise
        
        
async def update_experience_service(data: ExperienceCreate, id:int):
    try:    
        return await update_experience(data, id)
    except Exception:
        logger.exception("Something Went Wrong");
        raise
    
async def delete_experience_service(id:int):
    try:    
        return await remove_experience(id)
    except Exception:
        logger.exception("Something Went Wrong");
        raise