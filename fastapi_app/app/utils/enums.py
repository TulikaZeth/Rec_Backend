from enum import Enum

class EmailStatus(str,Enum):
    """Email status enumeration"""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    SENT = "sent"
    FAILED = "failed"


class screeningStatus(Enum):
    """screening status enumeration"""
    SELECTED = "selected"
    REJECTED = "rejected"
    SCHEDULED = "scheduled"
    PENDING = "pending"

class TaskStatus(Enum):
    """Task status enumeration for user tasks"""
    PENDING = "pending"  # Default status
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
