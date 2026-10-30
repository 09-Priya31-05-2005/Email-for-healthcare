from agents.intake_agent import analyze_complaint
from agents.investigation_agent import investigate_complaint
from agents.resolution_agent import determine_resolution
from agents.response_agent import generate_patient_response


# --------------------------------------------------
# Patient complaint
# --------------------------------------------------

complaint = """
I had an appointment with the Cardiology department yesterday
at 10 AM. I arrived 30 minutes early but had to wait almost
two hours before anyone attended to me. Nobody explained the
delay. This was extremely frustrating.
"""


# --------------------------------------------------
# Intake
# --------------------------------------------------

intake_result = analyze_complaint(complaint)


# --------------------------------------------------
# Investigation
# --------------------------------------------------

investigation_result = investigate_complaint(
    complaint=complaint,
    patient_id="P1001"
)


# --------------------------------------------------
# Resolution
# --------------------------------------------------

resolution_result = determine_resolution(
    complaint=complaint,
    investigation=investigation_result.model_dump_json()
)


# --------------------------------------------------
# Response
# --------------------------------------------------

response_result = generate_patient_response(
    complaint=complaint,
    investigation=investigation_result.model_dump_json(),
    resolution=resolution_result.model_dump_json()
)


# --------------------------------------------------
# Display response
# --------------------------------------------------

print("\n========== PATIENT RESPONSE ==========\n")

print("Subject:")
print(response_result.subject)

print("\nResponse:")
print(response_result.response)