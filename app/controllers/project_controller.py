import logging
from fastapi import Form, File, UploadFile, HTTPException
from app.services.project_service import add_poroject_service, update_project_service, get_project_service, delete_project_service;
from app.schemas.project_schema import ProjectCreate, ProjectUpdate
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
    
async def update_project(
    id: int,
    project_name: str = Form(...),
    description: str = Form(...),
    tech_used: list[str] = Form(...),
    live_link: str = Form(...),
    github_url: str = Form(...),
    image_url: UploadFile | None = File(None),
):
    try:
        # nayi image aayi to upload karo, warna None (purani image rahegi)
        thumbnail = await save_upload(image_url) if image_url else None
        project_data = ProjectUpdate(
            project_name=project_name,
            description=description,
            tech_used=tech_used,
            image_url=thumbnail,
            live_link=live_link,
            github_url=github_url,
        )
        response = await update_project_service(project_data, id)
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

async def delete_project(id:int):
    try: 
        response = await delete_project_service(id);
        if response is None:
            raise HTTPException(
                status_code=404,
                detail=f"Information not found",
            )
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
        raise
    