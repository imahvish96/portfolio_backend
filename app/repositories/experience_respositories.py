import json
import logging
from app.config import database
from app.schemas.experience_schema import ExperienceCreate

logger = logging.getLogger(__name__)

async def fetch_experience():
    try:
        query = """SELECT * FROM experience"""
        return await database.pool.fetch(query);
    except Exception:
        logging.exception("Something Went Wrong");
        raise
    
async def create_experience(data: ExperienceCreate):
    try:
        query = """INSERT INTO
        experience (designation, organization, start_date, end_date, is_current)
        VALUES ($1, $2, $3, $4, $5)"""
        response = await database.pool.execute(
            query,
                data.designation,
                data.organization,
                data.start,
                data.end,
                data.is_current
            );
        return response
    except Exception:
        logging.exception("Something Went Wrong");
        raise
    
async def update_experience(data: ExperienceCreate, id):
    try:
        query = """UPDATE experience
        SET designation=$1, organization=$2, start_date=$3, end_date=$4, is_current=$5,
        WHERE id=$6"""
        response = await database.pool.execute(
            query,
            data.designation,
            data.organization,
            data.start,
            data.end,
            data.is_current,
            id
        );
        return response
    except Exception:
        logger.exception("Something Went Wrong");
        raise
    
async def remove_experience(id:int):
    try:
        query = """DELETE FROM experience WHERE id=$1"""
        response = await database.pool.execute(query, id);
        return response
    except Exception:
        logger.exception("Something Went Wrong");
        raise
    