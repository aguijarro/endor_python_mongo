from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.test import Test
from sqlalchemy import text

router = APIRouter()

@router.post("/")
async def create_test(name: str, db: AsyncSession = Depends(get_db)):
    test_item = Test(name=name)
    db.add(test_item)
    await db.commit()
    await db.refresh(test_item)
    return test_item

@router.get("/")
async def read_tests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM test_table"))
    tests = [dict(row._mapping) for row in result.all()]
    return tests
