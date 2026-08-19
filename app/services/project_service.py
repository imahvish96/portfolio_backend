import logging
from app.repositories.project_repository import create_project, update_project, fetch_project, remove_project;

logger = logging.getLogger(__name__)

async def get_project_service():
    try:
        return await fetch_project();
    except Exception:
        logger.exception("Error while fetching project")
        raise;
    
async def add_poroject_service(data):
    try:
        return await create_project(data);
    except Exception:
        logger.exception("Error while adding project")
        raise;
    
async def update_project_service(data, id: int):
    try:
        return await update_project(data, id);
    except Exception:
        logger.exception("Error while updating project")
        raise;
    
async def delete_project_service(id: int):
    try:
        return await remove_project(id);
    except Exception:
        logger.exception("Error while updating project")
        raise;