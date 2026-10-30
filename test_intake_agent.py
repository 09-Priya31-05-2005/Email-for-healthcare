from agents.intake_agent import analyze_complaint


complaint = """
I had an appointment with the Cardiology department yesterday
at 10 AM. I arrived 30 minutes early but had to wait almost
two hours before anyone attended to me. Nobody explained the
delay. This was extremely frustrating.
"""


result = analyze_complaint(complaint)


print("\n========== COMPLAINT ANALYSIS ==========\n")

print("Complaint Type :", result.complaint_type)
print("Department     :", result.department)
print("Service        :", result.service)
print("Appointment Date:", result.appointment_date)
print("Appointment Time:", result.appointment_time)
print("Issue          :", result.issue)
print("Severity       :", result.severity)