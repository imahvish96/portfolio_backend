import logging
from app.repositories.project_repository import create_project, update_project, fetch_project;

logger = logging.getLogger(__name__)

async def get_project_service():
    try:
        return await fetch_project();
    except Exception:
        logger.exception("Error while adding project")
        raise;
    
async def add_poroject_service(data):
    try:
        return await create_project(data);
    except Exception:
        logger.exception("Error while adding project")
        raise;
    
async def edit_project(data):
    try:
        return await update_project(data);
    except Exception:
        logger.exception("Error while adding project")
        raise;