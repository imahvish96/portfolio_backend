import json
import logging
from app.config import database
from app.schemas.project_schema import ProjectCreate

logger = logging.getLogger(__name__)

async def fetch_project():
    try:
        query = """SELECT * FROM project WHERE id=$1"""
        row = await database.pool.fetchrow(query, 2);
        return dict(row) if row else None
    except Exception:
        logging.exception("Something Went Wrong");
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
                json.dumps(data.tech_used),
                data.image_url,
                data.live_link,
                data.github_url
            );
        return response
    except Exception:
        logging.exception("Something Went Wrong");
        raise
    
async def update_project(data: ProjectCreate):
    try:
        query = """UPDATE project
        SET project_name=$1, description=$2, tech_used=$3, image_url=$4, live_link=$5, github_url=$6
        WHERE id=$7"""
        response = await database.pool.execute(
            query,
                data.project_name,
                data.description,
                json.dumps(data.tech_used),
                data.image_url,
                data.live_link,
                data.github_url,
                2
            );
        return response
    except Exception:
        logging.exception("Something Went Wrong");
        raise
    