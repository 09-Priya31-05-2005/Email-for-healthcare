from typing import TypedDict, Optional

from langgraph.graph import StateGraph, START, END

from agents.intake_agent import (
    analyze_complaint,
)

from agents.investigation_agent import (
    investigate_complaint,
)

from agents.resolution_agent import (
    determine_resolution,
)

from agents.response_agent import (
    generate_patient_response,
)

from agents.tracking_agent import (
    create_complaint_case,
)


# ==========================================================
# 1. Define the shared state
# ==========================================================

class ComplaintState(TypedDict, total=False):

    # Original input
    complaint: str
    patient_id: str

    # Agent outputs
    intake_result: object
    investigation_result: object
    resolution_result: object
    response_result: object
    complaint_case: object

    # Workflow information
    workflow_action: str


# ==========================================================
# 2. Intake Agent Node
# ==========================================================

def intake_node(state: ComplaintState):

    print("\n[1] Running Intake Agent...")

    result = analyze_complaint(
        state["complaint"]
    )

    print("    Complaint Type:", result.complaint_type)
    print("    Department:", result.department)
    print("    Severity:", result.severity)

    return {
        "intake_result": result
    }


# ==========================================================
# 3. Investigation Agent Node
# ==========================================================

def investigation_node(state: ComplaintState):

    print("\n[2] Running Investigation Agent...")

    result = investigate_complaint(
        complaint=state["complaint"],
        patient_id=state["patient_id"]
    )

    print("    Patient Found:", result.patient_found)
    print("    Appointment Confirmed:", result.appointment_confirmed)
    print("    Investigation Status:", result.investigation_status)

    return {
        "investigation_result": result
    }


# ==========================================================
# 4. Resolution Agent Node
# ==========================================================

def resolution_node(state: ComplaintState):

    print("\n[3] Running Resolution Agent...")

    investigation = state["investigation_result"]

    result = determine_resolution(
        complaint=state["complaint"],
        investigation=investigation.model_dump_json()
    )

    print("    Severity:", result.final_severity)
    print("    Action:", result.action)
    print("    Department:", result.assigned_department)
    print("    Escalation:", result.escalation_required)

    return {
        "resolution_result": result
    }


# ==========================================================
# 5. Decide routing or escalation
# ==========================================================

def decide_workflow(state: ComplaintState):

    resolution = state["resolution_result"]

    if resolution.escalation_required:

        return "escalate"

    return "route"


# ==========================================================
# 6. Normal routing node
# ==========================================================

def route_node(state: ComplaintState):

    resolution = state["resolution_result"]

    print("\n[4] Routing Complaint...")

    print(
        f"    Routed to: "
        f"{resolution.assigned_department}"
    )

    return {
        "workflow_action": "Complaint routed to appropriate department"
    }


# ==========================================================
# 7. Escalation node
# ==========================================================

def escalation_node(state: ComplaintState):

    resolution = state["resolution_result"]

    print("\n[4] Escalating Complaint...")

    print(
        "    Escalation Required: YES"
    )

    print(
        f"    Escalation Department: "
        f"{resolution.assigned_department}"
    )

    return {
        "workflow_action": "Complaint escalated for immediate review"
    }


# ==========================================================
# 8. Response Agent Node
# ==========================================================

def response_node(state: ComplaintState):

    print("\n[5] Running Response Agent...")

    investigation = state["investigation_result"]
    resolution = state["resolution_result"]

    result = generate_patient_response(
        complaint=state["complaint"],
        investigation=investigation.model_dump_json(),
        resolution=resolution.model_dump_json()
    )

    print("    Patient response generated.")

    return {
        "response_result": result
    }


# ==========================================================
# 9. Tracking Agent Node
# ==========================================================

def tracking_node(state: ComplaintState):

    print("\n[6] Running Tracking Agent...")

    resolution = state["resolution_result"]

    case = create_complaint_case(
        resolution
    )

    print("    Complaint ID:", case.complaint_id)
    print("    Status:", case.status)
    print("    Priority:", case.priority)

    return {
        "complaint_case": case
    }


# ==========================================================
# 10. Build the graph
# ==========================================================

builder = StateGraph(ComplaintState)


# Add nodes

builder.add_node(
    "intake",
    intake_node
)

builder.add_node(
    "investigation",
    investigation_node
)

builder.add_node(
    "resolution",
    resolution_node
)

builder.add_node(
    "route",
    route_node
)

builder.add_node(
    "escalate",
    escalation_node
)

builder.add_node(
    "response",
    response_node
)

builder.add_node(
    "tracking",
    tracking_node
)


# ==========================================================
# 11. Define workflow
# ==========================================================

builder.add_edge(
    START,
    "intake"
)

builder.add_edge(
    "intake",
    "investigation"
)

builder.add_edge(
    "investigation",
    "resolution"
)


# Conditional routing

builder.add_conditional_edges(
    "resolution",
    decide_workflow,
    {
        "route": "route",
        "escalate": "escalate"
    }
)


builder.add_edge(
    "route",
    "response"
)

builder.add_edge(
    "escalate",
    "response"
)

builder.add_edge(
    "response",
    "tracking"
)

builder.add_edge(
    "tracking",
    END
)


# ==========================================================
# 12. Compile graph
# ==========================================================

complaint_graph = builder.compile()