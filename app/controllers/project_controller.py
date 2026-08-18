import logging
from fastapi import Form, File, UploadFile
from app.services.project_service import add_poroject_service, edit_project, get_project_service;
from app.schemas.project_schema import ProjectCreate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.config.upload import save_upload

logger = logging.getLogger(__name__)

async def get_project():
    try:
        response = await get_project_service()
        return JSONResponse(
            status_code= 200,
            content=jsonable_encoder(
                {
                    "status": True,
                    "message": "Record Fetched Successfully",
                    "data": response
                }
            )
        );
    except Exception:
        logger.exception("Error while adding project")
        raise;
    
async def add_project(
    project_name:str =Form(...),
    description: str = Form(...),
    tech_used: list[str] = Form(...),
    image_url: UploadFile = File(...),
    live_link: str = Form(...),
    github_url: str = Form(...),
):
    try:
        thumbnail = await save_upload(image_url)
        project_data = ProjectCreate(
            project_name=project_name,
            description=description,
            tech_used=tech_used,
            image_url=thumbnail,
            live_link=live_link,
            github_url=github_url,
        )
        response = await add_poroject_service(project_data)
        return JSONResponse(
            status_code= 201,
            content=jsonable_encoder(
                {
                    "status": True,
                    "message": "Project Added Successfully",
                    "data": response
                }
            )
        );
    except Exception:
        logger.exception("Error while adding project")
        raise;
    

async def change_project(project_data: ProjectCreate):
    try:
        response = await edit_project(project_data)
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
    