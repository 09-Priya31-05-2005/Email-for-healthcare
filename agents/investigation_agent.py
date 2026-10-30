import json
from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os


load_dotenv()


# --------------------------------------------------
# 1. Define investigation output
# --------------------------------------------------

class InvestigationResult(BaseModel):

    patient_found: bool = Field(
        description="Whether the patient was found in authorized records"
    )

    appointment_confirmed: bool = Field(
        description="Whether the appointment details match the records"
    )

    history_found: bool = Field(
        description="Whether authorized interaction history was found"
    )

    findings: str = Field(
        description="Summary of the investigation findings"
    )

    previous_complaints: str = Field(
        description="Summary of previous complaints if available"
    )

    investigation_status: str = Field(
        description="Investigation status such as Confirmed, Mismatch, or Requires Review"
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
    InvestigationResult
)


# --------------------------------------------------
# 3. Load authorized data
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename):

    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


patients = load_json("patients.json")
appointments = load_json("appointments.json")
interaction_history = load_json("interaction_history.json")


# --------------------------------------------------
# 4. Retrieve authorized patient information
# --------------------------------------------------

def get_patient_information(patient_id):

    patient = next(
        (
            p for p in patients
            if p["patient_id"] == patient_id
            and p["authorized"] is True
        ),
        None
    )

    if not patient:
        return None

    appointment = next(
        (
            a for a in appointments
            if a["patient_id"] == patient_id
        ),
        None
    )

    history = next(
        (
            h for h in interaction_history
            if h["patient_id"] == patient_id
        ),
        None
    )

    return {
        "patient": patient,
        "appointment": appointment,
        "history": history
    }


# --------------------------------------------------
# 5. Investigation prompt
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a Healthcare Complaint Investigation Agent.

Your responsibility is to investigate a patient's complaint
using ONLY the authorized information provided to you.

Compare the patient's complaint with the appointment
and interaction information.

Do not invent facts.

Determine:

1. Whether the patient exists in authorized records.
2. Whether the appointment details are confirmed.
3. Whether authorized history is available.
4. What the investigation findings are.
5. Whether previous complaints exist.
6. Whether the case is Confirmed, Mismatch, or Requires Review.
"""
    ),
    (
        "human",
        """
PATIENT COMPLAINT:

{complaint}


AUTHORIZED PATIENT INFORMATION:

{patient_information}
"""
    )
])


# --------------------------------------------------
# 6. Investigation function
# --------------------------------------------------

def investigate_complaint(complaint, patient_id):

    patient_information = get_patient_information(patient_id)

    if patient_information is None:

        return InvestigationResult(
            patient_found=False,
            appointment_confirmed=False,
            history_found=False,
            findings="Patient was not found in authorized records.",
            previous_complaints="Not available",
            investigation_status="Requires Review"
        )

    chain = prompt | structured_llm

    result = chain.invoke({
        "complaint": complaint,
        "patient_information": patient_information
    })

    return result