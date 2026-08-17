import json
import logging
from app.config import database
from app.schemas.experience_schema import ExperienceCreate

logger = logging.getLogger(__name__)

async def fetch_experience():
    try:
        query = """SELECT * FROM experience WHERE id=$1"""
        row = await database.pool.fetchrow(query, 2);
        return dict(row) if row else None
    except Exception:
        logging.exception("Something Went Wrong");
        raise
    
async def create_experience(data: ExperienceCreate):
    try:
        query = """INSERT INTO
        experience (designation, organization, start_date, end_date)
        VALUES ($1, $2, $3, $4)"""
        response = await database.pool.execute(
            query,
                data.designation,
                data.organization,
                data.start,
                data.end,
            );
        return response
    except Exception:
        logging.exception("Something Went Wrong");
        raise
    
async def update_experience(data: ExperienceCreate):
    try:
        query = """UPDATE experience
        SET designation=$1, organization=$2, start_date=$3, end_date=$4
        WHERE id=$5"""
        response = await database.pool.execute(
            query,
                data.designation,
                data.organization,
                data.start,
                data.end,
                2
            );
        return response
    except Exception:
        logging.exception("Something Went Wrong");
        raise
    