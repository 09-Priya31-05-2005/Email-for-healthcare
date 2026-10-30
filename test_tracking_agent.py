from agents.investigation_agent import investigate_complaint
from agents.resolution_agent import determine_resolution
from agents.tracking_agent import create_complaint_case


complaint = """
I had an appointment with the Cardiology department yesterday
at 10 AM. I arrived 30 minutes early but had to wait almost
two hours before anyone attended to me. Nobody explained the
delay. This was extremely frustrating.
"""


# Investigation
investigation_result = investigate_complaint(
    complaint=complaint,
    patient_id="P1001"
)


# Resolution
resolution_result = determine_resolution(
    complaint=complaint,
    investigation=investigation_result.model_dump_json()
)


# Tracking
case = create_complaint_case(resolution_result)


print("\n========== COMPLAINT CASE ==========\n")

print("Complaint ID       :", case.complaint_id)
print("Status             :", case.status)
print("Severity           :", case.severity)
print("Priority           :", case.priority)
print("Assigned Department:", case.assigned_department)
print("Escalation Required:", case.escalation_required)
print("Next Action        :", case.next_action)
print("Created At         :", case.created_at)