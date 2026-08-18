import logging

from app.schemas.information_schema import Information
from app.config import database
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json

logger = logging.getLogger(__name__)
async def feth_information():
    try: 
        query = """SELECT * FROM information"""
        response = await database.pool.fetchrow(
            query,
        )
        return response
    except Exception:
        logger.exception("Something Went Wrong")
        raise
    

async def set_peronal_information(data: Information):
    try: 
        query = """INSERT INTO information (profile_summary, email, message, skills, profile_image, resume_url)
        VALUES ($1, $2, $3, $4::jsonb, $5, $6)""";
        await database.pool.execute(
            query,
            data.profile_summary,
            data.email,
            data.message,
            json.dumps(data.skills),
            data.profile,
            data.resume
        )
        return {
            "success": True,
            "message": "Record Created Successfully",
            "status_code": 201,
        }
    except Exception as Error:
        print("Error In Repository", Error)
        
async def edit_information(data: Information):
    try: 
        query = """UPDATE information
        SET profile_summary = $1, email = $2, message = $3, skills = $4::jsonb
        WHERE id = $5""";
        await database.pool.execute(
            query,
            data.profile_summary,
            data.email,
            data.message,
            json.dumps(data.skills),    
            1
        )
        return {
            "success": True,
            "message": "Record Updated Successfully",
            "status_code": 200,
        }
    except Exception as Error:
        print("Error In Repository", Error)

async def delete_information(id: int):
    try:
        query = """DELETE FROM information WHERE id=$1"""
        response = await database.pool.execute(
            query,
            id
        )
        
        return response;
    except Exception:
        logger.exception("Something went wrong")
        raise