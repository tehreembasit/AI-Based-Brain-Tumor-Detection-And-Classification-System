import streamlit as st
import numpy as np
import cv2
import os
from PIL import Image
from styles import apply_styles
apply_styles()
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from gradcam import get_gradcam, overlay_heatmap
import db
from report_generator import generate_pdf
from profile_page import profile_page

# =========================
# SESSION STATE INIT
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "dashboard"
    st.session_state.last_result = None
if "generated_report" not in st.session_state:
    st.session_state.generated_report = None

# =========================
# LOGIN / SIGNUP
# =========================
def login_signup():
 
    st.title("🔐 Login / Signup")

    choice = st.radio("Choose Option", ["Login", "Signup"])

    if choice == "Signup":
        name = st.text_input("Name")
        age = st.number_input("Age", 1, 100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Signup"):
            if db.add_user(name, age, gender, email, password):
                st.success("Signup Successful! Now Login")
            else:
                st.error("Email already exists!")

    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = db.authenticate_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid credentials")

# =========================
# DASHBOARD
# =========================
def dashboard():
    st.markdown("""
        <style>
        /* This selector is very strong to override global .stButton styles */
        div.main-dashboard [data-testid="stButton"] button {
            min-height: 150px !important; 
            width: 100% !important;
            font-size: 24px !important;
            font-weight: 700 !important;
            background-color: rgba(26, 54, 93, 0.95) !important;
            border: 3px solid #00E5FF !important;
            border-radius: 20px !important;
            margin-bottom: 20px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.4) !important;
        }

        /* Stronger hover selector */
        div.main-dashboard [data-testid="stButton"] button:hover {
            background-color: #00E5FF !important;
            color: #1A365D !important;
            transform: scale(1.05) !important;
            box-shadow: 0 0 35px #00E5FF !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>🏠 AI Brain Tumor Dashboard</h1>", unsafe_allow_html=True)
    st.write(f"Welcome {st.session_state.user[1]} 👋")
    st.markdown('<div class="main-dashboard">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, _ = st.columns(2)

    if col1.button("🧠 Upload MRI Scan"):
        st.session_state.page = "upload"

    if col2.button("📜 View History"):
        st.session_state.page = "history"

    if col3.button("📄 Generate Report"):
        st.session_state.page = "report"

    if col4.button("🤖 Chatbot Assistant"):
        st.session_state.page = "chatbot"

    if col5.button("⚙️ Profile Settings"):
        st.session_state.page = "profile"
    st.markdown('</div>', unsafe_allow_html=True)
# =========================
# UPLOAD MRI PAGE
# =========================
def upload_page():

    st.title("🧠 MRI Scan Analysis")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"

    model = load_model("model/brain_tumor_model.h5")
    class_names = ['glioma', 'meningioma', 'notumor', 'pituitary']

    uploaded_files = st.file_uploader(
        "Upload MRI Images",
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files:

        for file in uploaded_files:

            st.subheader(file.name)

            # =========================
            # SAVE IMAGE
            # =========================
            img = Image.open(file).convert("RGB")
            img = img.resize((224, 224))

            img_path = f"media/mri/{file.name}"
            os.makedirs("media/mri", exist_ok=True)
            img.save(img_path)

            img_array = image.img_to_array(img)
            img_array = preprocess_input(img_array)
            img_input = np.expand_dims(img_array, axis=0)
            # =========================
            # PREDICTION
            # =========================
            preds = model.predict(img_input)

            class_idx = np.argmax(preds)
            confidence = np.max(preds) * 100
            prediction = class_names[class_idx]

            st.markdown(f"""
    <div style="
        background-color: rgba(26, 54, 93, 0.85); 
        padding: 20px; 
        border-radius: 15px; 
        border: 2px solid #00E5FF;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);
    ">
        <h3 style="color: #00E5FF; margin: 0; font-family: sans-serif;">
            🧠 Prediction: <span style="color: white;">{prediction}</span>
        </h3>
        <h4 style="color: #00E5FF; margin: 10px 0 0 0; font-family: sans-serif; opacity: 0.9;">
            📊 Confidence: <span style="color: white;">{confidence:.2f}%</span>
        </h4>
    </div>
""", unsafe_allow_html=True)

            st.image(img)

            # =========================
            # GRAD-CAM
            # =========================
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            heatmap = get_gradcam(model, img_input, layer_name="last_conv")

            gradcam_path = None

            if heatmap is not None:
                overlay = overlay_heatmap(img_cv, heatmap)
                import time
                os.makedirs("media/gradcam", exist_ok=True)
                gradcam_path = f"media/gradcam/gradcam_{int(time.time())}_{file.name}"
                success = cv2.imwrite(gradcam_path, overlay)
                if not success:
                  st.error("Grad-CAM could not be saved")
                  gradcam_path = None
                else:
                 st.image(gradcam_path, caption="Grad-CAM Result")
            else:
                st.warning("Grad-CAM failed")

            # =========================
            # SAVE TO DATABASE (IMPORTANT CHANGE)
            # =========================
            import datetime

            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.add_history(
                email=st.session_state.user[4],
                image_path=img_path,
                gradcam_path=gradcam_path,
                prediction=prediction,
                confidence=confidence,
                time=time_now
            )

            # =========================
            # OPTIONAL: STORE LAST RESULT (for report page)
            # =========================
            st.session_state.last_result = {
                "img_path": img_path,
                "gradcam_path": gradcam_path,
                "prediction": prediction,
                "confidence": confidence
            }

# =========================
# REPORT PAGE
# =========================
def report_page():

    st.title("📄 Generate Report")

    if st.button("⬅ Back"):
        st.session_state.page = "dashboard"

    if st.button("Generate Report"):

        if not st.session_state.last_result:
            st.markdown(f"""
    <div style="
        background-color: rgba(139, 0, 0, 0.9); 
        color: white; 
        padding: 15px; 
        border-radius: 10px; 
        border: 2px solid #FF4B4B;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.4);
    ">
        ⚠️ No scan data available. Upload MRI first.
    </div>
""", unsafe_allow_html=True)
            return

        data = st.session_state.last_result
        user = st.session_state.user

        # =========================
        # GENERATE PDF (background)
        # =========================
        pdf_file = generate_pdf(
            user=user,
            original_img_path=data["img_path"],
            gradcam_path=data["gradcam_path"],
            prediction=data["prediction"],
            confidence=data["confidence"]
        )

        st.session_state.generated_report = pdf_file

        # =========================
        # SHOW REPORT ON SCREEN
        # =========================

        # -------- Patient Info --------
        st.markdown("## 👤 Patient Information")
        st.write(f"**Name:** {user[1]}")
        st.write(f"**Age:** {user[2]}")
        st.write(f"**Gender:** {user[3]}")
        st.write(f"**Email:** {user[4]}")

        # -------- MRI Image --------
        st.markdown("## 🧠 MRI Scan")
        st.image(data["img_path"])

        # -------- Prediction --------
        st.markdown("## 📊 Prediction Result")
        st.write(f"**Prediction:** {data['prediction']}")
        st.write(f"**Confidence:** {data['confidence']:.2f}%")

        # -------- Grad-CAM --------
        if data["gradcam_path"]:
            st.markdown("## 🔥 Grad-CAM Visualization")
            st.image(data["gradcam_path"])

        # -------- Date & Time --------
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.markdown("## ⏰ Generated On")
        st.write(now)

        st.info("📥 You can download this report later from Profile Page.")
# =========================
# OTHER PAGES
# =========================
def history_page():

    st.title("📜 MRI Scan History")

    if st.button("⬅ Back"):
        st.session_state.page = "dashboard"

    email = st.session_state.user[4]
    records = db.get_history(email)

    if len(records) == 0:
        st.markdown(f"""
    <div style="
        background-color: rgba(26, 54, 93, 0.95); 
        color: #00E5FF; 
        padding: 15px; 
        border-radius: 10px; 
        border: 2px solid #00E5FF;
        text-align: center;
        font-weight: bold;
        margin: 15px 0;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
    ">
        ℹ️ No history found.
    </div>
""", unsafe_allow_html=True)
        return

    for record in records:

        record_id = record[0]
        image_path = record[2]
        gradcam_path = record[3]
        prediction = record[4]
        confidence = record[5]
        time = record[6]

        # =========================
        # SAFE CONFIDENCE FIX (IMPORTANT)
        # =========================
        try:
            if isinstance(confidence, bytes):
                confidence = float(np.frombuffer(confidence, dtype=np.float32)[0])
            else:
                confidence = float(confidence)
        except:
            confidence = 0.0

        st.markdown("---")
        st.subheader(f"🧠 {prediction}")

        st.write(f"**Confidence:** {confidence:.2f}%")
        st.write(f"**Time:** {time}")

        col1, col2, col3, col4 = st.columns(4)

        # ================= VIEW IMAGE =================
        with col1:
            if os.path.exists(image_path):
                st.image(image_path, caption="MRI")

        # ================= VIEW GRADCAM =================
        with col2:
            if gradcam_path and os.path.exists(gradcam_path):
                st.image(gradcam_path, caption="Grad-CAM")

        # ================= GENERATE PDF =================
        with col3:
            if st.button(f"📄 Report {record_id}"):
                pdf = generate_pdf(
                    user=st.session_state.user,
                    original_img_path=image_path,
                    gradcam_path=gradcam_path,
                    prediction=prediction,
                    confidence=confidence
                )
                with open(pdf, "rb") as f:
                    st.download_button(
                        "⬇ Download PDF",
                        f,
                        file_name=f"report_{record_id}.pdf"
                    )

        # ================= DELETE =================
        with col4:
            if st.button(f"🗑 Delete {record_id}"):
                db.delete_history(record_id)
                st.rerun()
def chatbot_page():

    st.title("🤖 Brain Tumor FAQ Assistant")

    if st.button("⬅ Back"):
        st.session_state.page = "dashboard"

    # ================= CHAT HISTORY =================
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    question = st.text_input("Ask your question")

    if st.button("Send"):

        if question:

            user_q = question
            question = question.lower()

            cursor = db.conn.cursor()

            cursor.execute("""
            SELECT answer FROM knowledge
            WHERE LOWER(question) LIKE ?
            """, ('%' + question + '%',))

            result = cursor.fetchone()

            if result:
                answer = result[0]
            else:
                answer = "No answer found. Try asking about glioma, meningioma, or pituitary tumors."

            # Save chat
            st.session_state.chat_history.append(("user", user_q))
            st.session_state.chat_history.append(("bot", answer))

    # ================= DISPLAY CHAT =================
    for role, msg in st.session_state.chat_history:

        if role == "user":
            st.markdown(f"""
            <div style="
                text-align: right;
                background: linear-gradient(135deg, #6a5cff, #00f5ff);
                padding: 12px;
                border-radius: 15px;
                margin: 10px;
                color: #1A365D !important;
                box-shadow: 0 0 10px #00f5ff;
            ">
            👤 {msg}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div style="
                text-align: left;
                background: rgba(0,255,255,0.1);
                padding: 12px;
                border-radius: 15px;
                margin: 10px;
                color: #1A365D !important;
                box-shadow: 0 0 10px #00f5ff;
            ">
            🤖 {msg}
            </div>
            """, unsafe_allow_html=True)
# =========================
# MAIN ROUTING
# =========================
if not st.session_state.logged_in:
    login_signup()
    st.stop()

if st.session_state.page == "dashboard":
    dashboard()

elif st.session_state.page == "upload":
    upload_page()

elif st.session_state.page == "history":
    history_page()

elif st.session_state.page == "report":
    report_page()

elif st.session_state.page == "chatbot":
    chatbot_page()

elif st.session_state.page == "profile":
    profile_page()