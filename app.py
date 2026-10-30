import streamlit as st

from workflow.graph import complaint_graph


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Patient Complaint Management",
    page_icon="🏥",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🏥 Patient Complaint Management System")

st.write(
    "AI-powered multi-agent system for analyzing, "
    "investigating, routing, escalating, and tracking "
    "patient complaints."
)


# --------------------------------------------------
# Input section
# --------------------------------------------------

st.subheader("Submit a Patient Complaint")

patient_id = st.text_input(
    "Patient ID",
    value="P1001"
)

complaint = st.text_area(
    "Patient Complaint",
    height=180,
    placeholder="Enter the patient's complaint here..."
)


# --------------------------------------------------
# Run workflow
# --------------------------------------------------

if st.button("Analyze Complaint", type="primary"):

    if not complaint.strip():

        st.warning("Please enter a patient complaint.")

    elif not patient_id.strip():

        st.warning("Please enter a patient ID.")

    else:

        with st.spinner(
            "Running multi-agent complaint workflow..."
        ):

            result = complaint_graph.invoke({
                "complaint": complaint,
                "patient_id": patient_id
            })


        # --------------------------------------------------
        # Extract results
        # --------------------------------------------------

        intake = result["intake_result"]
        investigation = result["investigation_result"]
        resolution = result["resolution_result"]
        response = result["response_result"]
        case = result["complaint_case"]


        # --------------------------------------------------
        # Complaint Analysis
        # --------------------------------------------------

        st.divider()

        st.header("📋 Complaint Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Complaint Type",
                intake.complaint_type
            )

        with col2:
            st.metric(
                "Department",
                intake.department
            )

        with col3:
            st.metric(
                "Severity",
                intake.severity
            )


        st.write("**Issue:**")
        st.write(intake.issue)


        # --------------------------------------------------
        # Investigation
        # --------------------------------------------------

        st.divider()

        st.header("🔎 Investigation")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**Patient Found**")
            st.write(
                "✅ Yes"
                if investigation.patient_found
                else "❌ No"
            )

        with col2:
            st.write("**Appointment Confirmed**")
            st.write(
                "✅ Yes"
                if investigation.appointment_confirmed
                else "❌ No"
            )

        with col3:
            st.write("**History Found**")
            st.write(
                "✅ Yes"
                if investigation.history_found
                else "❌ No"
            )

        st.write("**Investigation Status:**")
        st.info(investigation.investigation_status)

        st.write("**Findings:**")
        st.write(investigation.findings)


        # --------------------------------------------------
        # Resolution
        # --------------------------------------------------

        st.divider()

        st.header("⚙️ Resolution")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Severity",
                resolution.final_severity
            )

        with col2:
            st.metric(
                "Priority",
                resolution.priority
            )

        with col3:
            st.metric(
                "Department",
                resolution.assigned_department
            )

        with col4:
            st.metric(
                "Escalation",
                "YES"
                if resolution.escalation_required
                else "NO"
            )

        st.write("**Action:**")
        st.write(resolution.action)

        st.write("**Reasoning:**")
        st.write(resolution.reasoning)


        # --------------------------------------------------
        # Case Tracking
        # --------------------------------------------------

        st.divider()

        st.header("📌 Case Tracking")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**Complaint ID**")
            st.code(case.complaint_id)

        with col2:
            st.write("**Status**")
            st.write(case.status)

        with col3:
            st.write("**Next Action**")
            st.write(case.next_action)


        # --------------------------------------------------
        # Patient Response
        # --------------------------------------------------

        st.divider()

        st.header("💬 Patient Response")

        st.write("**Subject:**")
        st.write(response.subject)

        st.text_area(
            "Generated Response",
            value=response.response,
            height=250
        )