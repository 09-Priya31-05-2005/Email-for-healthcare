from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os


load_dotenv()


# --------------------------------------------------
# 1. Define the resolution output
# --------------------------------------------------

class ResolutionDecision(BaseModel):

    final_severity: str = Field(
        description="Final complaint severity: Low, Medium, or High"
    )

    action: str = Field(
        description="Recommended action such as Investigate, Route, Resolve, or Escalate"
    )

    assigned_department: str = Field(
        description="Department that should handle the complaint"
    )

    escalation_required: bool = Field(
        description="Whether the complaint must be escalated"
    )

    priority: str = Field(
        description="Priority of the complaint: Low, Medium, or High"
    )

    reasoning: str = Field(
        description="Short explanation for the resolution decision"
    )


# --------------------------------------------------
# 2. Connect to LLM
# --------------------------------------------------

llm = ChatOpenAI(
    model=os.getenv("model_name"),
    api_key=os.getenv("api_key"),
    base_url=os.getenv("base_url"),
    temperature=0
)

structured_llm = llm.with_structured_output(
    ResolutionDecision
)


# --------------------------------------------------
# 3. Resolution prompt
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a Healthcare Complaint Resolution Agent.

Your responsibility is to determine what should happen next
after a patient complaint has been investigated.

Consider:

- Complaint type
- Department
- Severity
- Investigation findings
- Investigation status

Routing rules:

Appointment-related complaints:
→ Appointment Administration or relevant clinical department

Billing complaints:
→ Billing Department

Pharmacy complaints:
→ Pharmacy Department

Technical/system complaints:
→ IT Department

General service complaints:
→ Patient Services

Serious, sensitive, safety-related, misconduct-related,
or potentially harmful complaints:
→ Patient Safety / Compliance
and escalation_required must be True.

For normal complaints, escalation_required must be False.

Do not invent facts.
"""
    ),
    (
        "human",
        """
COMPLAINT:

{complaint}

INVESTIGATION RESULT:

{investigation}
"""
    )
])


# --------------------------------------------------
# 4. Create the agent
# --------------------------------------------------

resolution_agent = prompt | structured_llm


# --------------------------------------------------
# 5. Resolution function
# --------------------------------------------------

def determine_resolution(complaint, investigation):

    result = resolution_agent.invoke({
        "complaint": complaint,
        "investigation": investigation
    })

    return result