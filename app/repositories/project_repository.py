import logging
from app.config import database
from app.schemas.project_schema import ProjectCreate, ProjectUpdate

logger = logging.getLogger(__name__)

async def fetch_project():
    try:
        query = """SELECT * FROM project"""
        return await database.pool.fetch(query);
    except Exception:
        logger.exception("Something Went Wrong");
        raise
    
async def create_project(data: ProjectCreate):
    try:
        query = """INSERT INTO
        project (project_name, description, tech_used, image_url, live_link, github_url)
        VALUES ($1, $2, $3::jsonb, $4, $5, $6)"""
        response = await database.pool.execute(
            query,
                data.project_name,
                data.description,
                data.tech_used,
                data.image_url,
                data.live_link,
                data.github_url
            );
        return response
    except Exception:
        logger.exception("Something Went Wrong");
        raise
    
async def update_project(data: ProjectUpdate, id: int):
    try:
        # image_url COALESCE: None aaya to purani image rahegi
        query = """UPDATE project
        SET project_name=$1,
            description=$2,
            tech_used=$3::jsonb,
            image_url=COALESCE($4, image_url),
            live_link=$5,
            github_url=$6
        WHERE id=$7"""
        response = await database.pool.execute(
            query,
                data.project_name,
                data.description,
                data.tech_used,
                data.image_url,
                data.live_link,
                data.github_url,
                id
            );
        return response
    except Exception:
        logging.exception("Something Went Wrong");
        raise
    
async def remove_project(id: int):
    try:
        query = """DELETE FROM project WHERE id=$1 RETURNING id"""
        row = await database.pool.fetchrow(query, id);
        return row
    except Exception:
        logger.exception("Something Went Wrong");
        raise
    