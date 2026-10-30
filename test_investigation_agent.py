from agents.investigation_agent import investigate_complaint


complaint = """
I had an appointment with the Cardiology department yesterday
at 10 AM. I arrived 30 minutes early but had to wait almost
two hours before anyone attended to me. Nobody explained the
delay. This was extremely frustrating.
"""


result = investigate_complaint(
    complaint=complaint,
    patient_id="P1001"
)


print("\n========== INVESTIGATION RESULT ==========\n")

print("Patient Found       :", result.patient_found)
print("Appointment Confirmed:", result.appointment_confirmed)
print("History Found       :", result.history_found)
print("Findings            :", result.findings)
print("Previous Complaints :", result.previous_complaints)
print("Investigation Status:", result.investigation_status)