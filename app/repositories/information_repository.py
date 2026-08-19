import logging

from app.schemas.information_schema import Information, InformationUpdate
from app.config import database
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


async def get_information_skills(id: int):
    # us record ki abhi wali skills (list of URLs) laao — diff-delete ke liye
    try:
        row = await database.pool.fetchrow(
            """SELECT skills FROM information WHERE id=$1""", id
        )
        return row["skills"] if row else None
    except Exception:
        logger.exception("Something Went Wrong")
        raise


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
            data.skills,
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
        
async def edit_information(data: InformationUpdate, id: int):
    try:
        # COALESCE: agar naya value None hai to column ki purani value hi rakho
        query = """UPDATE information
        SET profile_summary = $1,
            email = $2,
            message = $3,
            skills = COALESCE($4::jsonb, skills),
            profile_image = COALESCE($5, profile_image),
            resume_url = COALESCE($6, resume_url)
        WHERE id = $7""";
        await database.pool.execute(
            query,
            data.profile_summary,
            data.email,
            data.message,
            data.skills,
            data.profile,
            data.resume,
            id
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
        # RETURNING id: agar row mili to uski id wapas, warna None (id DB mein nahi)
        query = """DELETE FROM information WHERE id=$1 RETURNING id"""
        row = await database.pool.fetchrow(
            query,
            id
        )
        return row
    except Exception:
        logger.exception("Something went wrong")
        raise