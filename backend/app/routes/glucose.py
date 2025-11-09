"""Glucose data endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.base import get_db
from app.models.glucose import GlucoseReading
from app.schemas.glucose import GlucoseReadingCreate, GlucoseReadingResponse, GlucoseBulkUpload

router = APIRouter(prefix="/glucose", tags=["glucose"])


# Temporary: Mock user ID for MVP1 (replace with auth in MVP2)
MOCK_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


@router.post("/readings", response_model=GlucoseReadingResponse, status_code=201)
async def create_glucose_reading(
    reading: GlucoseReadingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a single glucose reading."""
    db_reading = GlucoseReading(
        user_id=MOCK_USER_ID,
        **reading.model_dump()
    )
    db.add(db_reading)
    await db.flush()
    await db.refresh(db_reading)
    return db_reading


@router.post("/bulk", status_code=201)
async def bulk_upload_glucose(
    data: GlucoseBulkUpload,
    db: AsyncSession = Depends(get_db)
):
    """Bulk upload glucose readings (e.g., from CGM export)."""
    db_readings = [
        GlucoseReading(user_id=MOCK_USER_ID, **reading.model_dump())
        for reading in data.readings
    ]
    db.add_all(db_readings)
    await db.flush()

    return {
        "status": "success",
        "records_created": len(db_readings),
        "message": f"Successfully uploaded {len(db_readings)} glucose readings"
    }


@router.get("/readings", response_model=List[GlucoseReadingResponse])
async def get_glucose_readings(
    start: Optional[datetime] = Query(None, description="Start timestamp"),
    end: Optional[datetime] = Query(None, description="End timestamp"),
    limit: int = Query(1000, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Get glucose readings within a time range."""
    query = select(GlucoseReading).where(GlucoseReading.user_id == MOCK_USER_ID)

    if start:
        query = query.where(GlucoseReading.timestamp >= start)
    if end:
        query = query.where(GlucoseReading.timestamp <= end)

    query = query.order_by(GlucoseReading.timestamp.desc()).limit(limit)

    result = await db.execute(query)
    readings = result.scalars().all()

    return readings
