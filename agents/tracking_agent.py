from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class ComplaintCase(BaseModel):

    complaint_id: str = Field(
        description="Unique complaint identifier"
    )

    status: str = Field(
        description="Current complaint status"
    )

    severity: str = Field(
        description="Complaint severity"
    )

    priority: str = Field(
        description="Complaint priority"
    )

    assigned_department: str = Field(
        description="Department responsible for handling the complaint"
    )

    escalation_required: bool = Field(
        description="Whether the complaint has been escalated"
    )

    next_action: str = Field(
        description="Next action required for the complaint"
    )

    created_at: str = Field(
        description="Complaint creation timestamp"
    )


def create_complaint_case(resolution):

    complaint_id = "CMP-" + str(uuid.uuid4())[:8].upper()

    if resolution.escalation_required:
        status = "Escalated"
        next_action = "Immediate review by Patient Safety / Compliance"
    else:
        status = "Under Investigation"
        next_action = (
            f"Review complaint by {resolution.assigned_department}"
        )

    case = ComplaintCase(
        complaint_id=complaint_id,
        status=status,
        severity=resolution.final_severity,
        priority=resolution.priority,
        assigned_department=resolution.assigned_department,
        escalation_required=resolution.escalation_required,
        next_action=next_action,
        created_at=datetime.now().isoformat(timespec="seconds")
    )

    return case