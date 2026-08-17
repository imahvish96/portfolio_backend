import asyncpg
import os

DATABASE_URL = os.getenv("DB_URL")

pool = None;

async def connect_db():
    global pool
    pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=1,
        max_size=5,
        statement_cache_size=0,
    )
    print(50 * "*");
    print("✅ Database Connected")
    print(50 * "*");
    
async def close_db():
    global pool
    if pool:
        await pool.close();
    print("❌ Database Closed")
        