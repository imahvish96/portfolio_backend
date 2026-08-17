import logging
from app.repositories.experience_respositories import fetch_experience, create_experience, update_experience
from app.schemas.experience_schema import ExperienceCreate

logger = logging.getLogger(__name__)

async def get_experience_service():
    await fetch_experience()
    
async def add_experience_service(data: ExperienceCreate):
    try:    
        response = await create_experience(data)
        return response
    except Exception:
        logging.exception("Something Went Wrong");
        raise
        
        
async def edit_experience(data: ExperienceCreate):
    try:    
        response = await update_experience(data)
        return response
    except Exception:
        logging.exception("Something Went Wrong");
        raise