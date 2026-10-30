from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os


# Load environment variables
load_dotenv()


# --------------------------------------------------
# 1. Define the structured output
# --------------------------------------------------

class ComplaintDetails(BaseModel):

    complaint_type: str = Field(
        description="The category of the patient's complaint"
    )

    department: str = Field(
        description="The hospital department related to the complaint"
    )

    service: str = Field(
        description="The healthcare service involved in the complaint"
    )

    appointment_date: str = Field(
        description="Appointment date if mentioned, otherwise 'Not mentioned'"
    )

    appointment_time: str = Field(
        description="Appointment time if mentioned, otherwise 'Not mentioned'"
    )

    issue: str = Field(
        description="A concise description of the patient's main issue"
    )

    severity: str = Field(
        description="Complaint severity: Low, Medium, or High"
    )


# --------------------------------------------------
# 2. Connect to the LLM
# --------------------------------------------------

llm = ChatOpenAI(
    model=os.getenv("model_name"),
    api_key=os.getenv("api_key"),
    base_url=os.getenv("base_url"),
    temperature=0
)


# --------------------------------------------------
# 3. Tell the LLM to return our Pydantic structure
# --------------------------------------------------

structured_llm = llm.with_structured_output(ComplaintDetails)


# --------------------------------------------------
# 4. Create the prompt
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a Patient Complaint Intake Agent for a healthcare
complaint-management system.

Your job is to analyze a patient's complaint email and:

1. Understand the complaint.
2. Categorize the complaint.
3. Extract appointment information.
4. Identify the relevant department.
5. Identify the healthcare service involved.
6. Summarize the main issue.
7. Determine the severity.

Severity rules:

- Low: Minor inconvenience or general feedback.
- Medium: Service problem that requires investigation.
- High: Serious, sensitive, safety-related, misconduct-related,
  or potentially harmful complaint.

Do not invent information that is not present in the complaint.
If information is missing, use "Not mentioned".
"""
    ),
    (
        "human",
        """
Analyze the following patient complaint:

{complaint}
"""
    )
])


# --------------------------------------------------
# 5. Create the agent chain
# --------------------------------------------------

intake_agent = prompt | structured_llm


# --------------------------------------------------
# 6. Function to analyze a complaint
# --------------------------------------------------

def analyze_complaint(complaint: str) -> ComplaintDetails:

    result = intake_agent.invoke({
        "complaint": complaint
    })

    return result