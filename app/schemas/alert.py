# app/schemas/alert.py
"""
ARGUS Alert Schemas
===================
Pydantic models define the shape of alert data.
"""

from pydantic import BaseModel
from typing import Optional

class AlertResponse(BaseModel):
    """Schema for returning alert data from API"""
    id:          int
    rule_name:   str
    description: str
    severity:    str
    source_ip:   str
    log_ids:     str
    status:      str
    created_at:  str

    class Config:
        from_attributes = True

class AlertListResponse(BaseModel):
    """Schema for returning a list of alerts"""
    total:  int
    alerts: list[AlertResponse]

class AlertStatusUpdate(BaseModel):
    """Schema for updating alert status"""
    status: str