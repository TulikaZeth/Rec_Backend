from typing import List, Optional
from odmantic import Model, EmbeddedModel
from datetime import datetime


class DomainPreference(EmbeddedModel):
    """Domain preference model"""
    name: str
    reason: str


class ShortlistedStage(EmbeddedModel):
    status: str
    date_time: datetime


class GDStage(EmbeddedModel):
    status: str
    date_time: datetime
    remarks: Optional[str]


class PIStage(EmbeddedModel):
    status: str
    date_time: datetime
    remarks: Optional[str]
    domain: Optional[str]
    reason: Optional[str]


class TaskStage(EmbeddedModel):
    status: str
    tasks: List[str]


class User(Model):
    """User model representing a candidate"""
    name: str
    email: str
    phone: int
    fb_id: str
    domain_pref_one: DomainPreference
    domain_pref_two: DomainPreference
    linkedIn: str
    domains: List[str]
    shortlisted: List[ShortlistedStage]
    gd: Optional[GDStage] = None
    pi: Optional[PIStage] = None
    task: Optional[TaskStage] = None
