# app/schemas/log.py
"""
ARGUS Log Schemas
=================
Pydantic models define the shape of log data.

Why Pydantic:
- Automatic data validation
- Clear API documentation in Swagger
- Type safety — prevents wrong data types
- FastAPI uses these to validate requests and responses
"""

from pydantic import BaseModel
from typing import Optional

class LogBase(BaseModel):
    """Fields shared by all log operations"""
    timestamp: str
    level:     str
    message:   str
    source:    str

class LogCreate(LogBase):
    """Schema for creating a new log — same as base"""
    pass

class LogResponse(LogBase):
    """
    Schema for returning log data from API.
    Includes id which is assigned by database.
    """
    id: int

    class Config:
        from_attributes = True

class LogListResponse(BaseModel):
    """Schema for returning a list of logs"""
    total: int
    logs:  list[LogResponse]