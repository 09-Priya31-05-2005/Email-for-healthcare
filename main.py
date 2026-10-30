from workflow.graph import complaint_graph


def main():

    print("\n")
    print("=" * 60)
    print("     PATIENT COMPLAINT MANAGEMENT SYSTEM")
    print("=" * 60)

    complaint = """
    My name is Rahul. I want to report serious misconduct that occurred 
    during my hospital visit. I believe the incident was
    extremely serious and requires immediate attention. I am
    concerned about what happened and want this matter formally
    investigated.
    """

    patient_id = "P1001"

    print("\nPatient complaint received.")
    print("\nStarting multi-agent workflow...\n")

    result = complaint_graph.invoke({
        "complaint": complaint,
        "patient_id": patient_id
    })

    # --------------------------------------------------
    # Final results
    # --------------------------------------------------

    response = result["response_result"]
    case = result["complaint_case"]

    print("\n")
    print("=" * 60)
    print("              WORKFLOW COMPLETE")
    print("=" * 60)

    print("\nCOMPLAINT ID:")
    print(case.complaint_id)

    print("\nSTATUS:")
    print(case.status)

    print("\nSEVERITY:")
    print(case.severity)

    print("\nPRIORITY:")
    print(case.priority)

    print("\nASSIGNED DEPARTMENT:")
    print(case.assigned_department)

    print("\nESCALATION:")
    print(case.escalation_required)

    print("\nNEXT ACTION:")
    print(case.next_action)

    print("\n")
    print("=" * 60)
    print("              PATIENT RESPONSE")
    print("=" * 60)

    print("\nSubject:")
    print(response.subject)

    print("\nResponse:")
    print(response.response)


if __name__ == "__main__":
    main()