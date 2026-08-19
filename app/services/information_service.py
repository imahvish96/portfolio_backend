import logging

from app.repositories.information_repository import feth_information, set_peronal_information, edit_information, delete_information, get_information_skills
from app.schemas.information_schema import Information, InformationUpdate

logger = logging.getLogger(__name__)
async def get_information_service():
    try: 
        return await feth_information()
    except Exception:
        logger.exception("Something Went Wrong");
        raise
    
async def add_personal_information_service(data: Information):
    try:    
        response = await set_peronal_information(data)
        return response
    except Exception as Error:
        print("Service Error", Error)
        
async def get_information_skills_service(id: int):
    try:
        return await get_information_skills(id)
    except Exception:
        logger.exception("Something Went Wrong");
        raise


async def update_information_service(data: InformationUpdate, id: int):
    try:
        response = await edit_information(data, id)
        return response
    except Exception as Error:
        print("Service Error", Error)

async def remove_information_service(id: int):
    try:
        response = await delete_information(id)
        return response
    except Exception:
        logger.exception("Something Went Wrong");
        raise
        
