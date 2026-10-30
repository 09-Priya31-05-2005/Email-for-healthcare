from agents.intake_agent import analyze_complaint
from agents.investigation_agent import investigate_complaint
from agents.resolution_agent import determine_resolution


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
# Step 1: Intake
# --------------------------------------------------

intake_result = analyze_complaint(complaint)


print("\n========== INTAKE ==========\n")

print(intake_result)


# --------------------------------------------------
# Step 2: Investigation
# --------------------------------------------------

investigation_result = investigate_complaint(
    complaint=complaint,
    patient_id="P1001"
)


print("\n========== INVESTIGATION ==========\n")

print(investigation_result)


# --------------------------------------------------
# Step 3: Resolution
# --------------------------------------------------

resolution_result = determine_resolution(
    complaint=complaint,
    investigation=investigation_result.model_dump_json()
)


print("\n========== RESOLUTION ==========\n")

print("Severity           :", resolution_result.final_severity)
print("Action             :", resolution_result.action)
print("Assigned Department:", resolution_result.assigned_department)
print("Escalation Required:", resolution_result.escalation_required)
print("Priority           :", resolution_result.priority)
print("Reasoning          :", resolution_result.reasoning)