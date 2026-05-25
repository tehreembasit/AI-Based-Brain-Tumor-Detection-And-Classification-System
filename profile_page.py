import streamlit as st
import db
import os

def profile_page():

    st.title("⚙️ Profile Settings")

    # =========================
    # BACK BUTTON
    # =========================
    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"

    user = st.session_state.user

    # =========================
    # VIEW PROFILE
    # =========================
    st.markdown("## 👤 User Information")

    st.write(f"**Name:** {user[1]}")
    st.write(f"**Age:** {user[2]}")
    st.write(f"**Gender:** {user[3]}")
    st.write(f"**Email:** {user[4]}")

    st.markdown("---")

    # =========================
    # EDIT PROFILE
    # =========================
    st.markdown("## ✏️ Edit Profile")

    new_name = st.text_input("Name", value=user[1])
    new_age = st.number_input("Age", 1, 100, value=user[2])
    new_gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        index=["Male", "Female", "Other"].index(user[3])
    )
    new_password = st.text_input("New Password", type="password")

    if st.button("Update Profile"):

        if new_password == "":
            st.error("Password cannot be empty")
        else:
            db.update_user(new_name, new_age, new_gender, new_password, user[4])

            # update session state
            st.session_state.user = (
                user[0], new_name, new_age, new_gender, user[4], user[5]
            )

            st.success("Profile updated successfully!")

    st.markdown("---")

    # =========================
    # DOWNLOAD REPORT
    # =========================
    st.markdown("## 📄 Latest Report")

    report = st.session_state.get("generated_report", None)

    if report and os.path.exists(report):

        with open(report, "rb") as f:
            st.download_button(
                label="📥 Download Report",
                data=f,
                file_name="brain_tumor_report.pdf",
                mime="application/pdf"
            )

    else:
        st.markdown(f"""
    <div style="
        background-color: rgba(255, 165, 0, 0.15); /* Semi-transparent orange */
        backdrop-filter: blur(10px);               /* Glass effect */
        color: #FFD700;                            /* Gold/Yellow text */
        padding: 15px; 
        border-radius: 12px; 
        border: 2px solid #FFA500;                 /* Orange border */
        text-align: center;
        font-weight: 700;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(255, 165, 0, 0.2);
    ">
        ⚠️ No report found. Please generate report first.
    </div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # =========================
    # LOGOUT
    # =========================
    st.markdown("## 🚪 Logout")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
    