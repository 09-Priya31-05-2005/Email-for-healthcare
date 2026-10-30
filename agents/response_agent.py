from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os


load_dotenv()


# --------------------------------------------------
# 1. Define response output
# --------------------------------------------------

class PatientResponse(BaseModel):

    subject: str = Field(
        description="Email subject for the patient"
    )

    response: str = Field(
        description="Professional and empathetic response to the patient"
    )


# --------------------------------------------------
# 2. Connect to LLM
# --------------------------------------------------

llm = ChatOpenAI(
    model=os.getenv("model_name"),
    api_key=os.getenv("api_key"),
    base_url=os.getenv("base_url"),
    temperature=0.3
)

structured_llm = llm.with_structured_output(
    PatientResponse
)


# --------------------------------------------------
# 3. Response prompt
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a Patient Communication Agent for a healthcare
complaint-management system.

Your job is to draft an empathetic, professional response
to a patient based on the complaint investigation and
resolution decision.

Your response must:

1. Acknowledge the patient's concern.
2. Show empathy.
3. Clearly communicate what was found.
4. Explain what action is being taken.
5. Avoid making claims that are not supported by the investigation.
6. Avoid exposing internal technical details.
7. Maintain a professional healthcare communication tone.

If the complaint requires further investigation, explain
that it has been forwarded to the appropriate department.

If the complaint has been escalated, communicate that the
matter has been referred for appropriate review.

Do not blame the patient or any employee.
Do not make promises about outcomes that are not known.

Only mention appointment, department, service, or other
patient-record details when they are directly relevant to
the complaint being addressed.

Do not introduce unrelated information from the patient's
records into the response.

Use only information that is relevant to the current complaint
and supported by the investigation.
"""
    ),
    (
        "human",
        """
PATIENT COMPLAINT:

{complaint}


INVESTIGATION RESULT:

{investigation}


RESOLUTION DECISION:

{resolution}
"""
    )
])


# --------------------------------------------------
# 4. Create response agent
# --------------------------------------------------

response_agent = prompt | structured_llm


# --------------------------------------------------
# 5. Generate patient response
# --------------------------------------------------

def generate_patient_response(
    complaint,
    investigation,
    resolution
):

    result = response_agent.invoke({
        "complaint": complaint,
        "investigation": investigation,
        "resolution": resolution
    })

    return result