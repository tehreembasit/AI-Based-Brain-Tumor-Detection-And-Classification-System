import sqlite3
import hashlib

# =========================
# CONNECT DB
# =========================
conn = sqlite3.connect("user.db", check_same_thread=False)
cursor = conn.cursor()

# =========================
# CREATE TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# =========================
# HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# ADD USER (SIGNUP)
# =========================
def add_user(name, age, gender, email, password):
    try:
        cursor.execute("""
        INSERT INTO users (name, age, gender, email, password)
        VALUES (?, ?, ?, ?, ?)
        """, (name, age, gender, email, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

# =========================
# VERIFY USER (LOGIN)
# =========================
def authenticate_user(email, password):
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?",
                   (email, hash_password(password)))
    return cursor.fetchone()
# =========================
# UPDATE USER
# =========================
def update_user(name, age, gender, password, email):
    cursor.execute("""
    UPDATE users
    SET name=?, age=?, gender=?, password=?
    WHERE email=?
    """, (name, age, gender, hash_password(password), email))
    conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    image_path TEXT,
    gradcam_path TEXT,
    prediction TEXT,
    confidence REAL,
    time TEXT
)
""")
conn.commit()
def add_history(email, image_path, gradcam_path, prediction, confidence, time):
    cursor.execute("""
    INSERT INTO history (email, image_path, gradcam_path, prediction, confidence, time)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (email, image_path, gradcam_path, prediction, confidence, time))
    conn.commit()
def get_history(email):
    cursor.execute("""
    SELECT * FROM history WHERE email=?
    ORDER BY id DESC
    """, (email,))
    return cursor.fetchall()
def delete_history(record_id):
    cursor.execute("DELETE FROM history WHERE id=?", (record_id,))
    conn.commit()
def init_knowledge_table():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        question TEXT,
        answer TEXT

    )
    """)

    conn.commit()
def insert_knowledge():

    data = [

        # ================= GLOIMA =================
        ("glioma", "What is glioma?",
         "Glioma is a brain tumor that starts in glial cells which support nerve cells in the brain."),

        ("glioma", "What are symptoms of glioma?",
         "Symptoms include headache, seizures, nausea, vomiting, blurred vision, memory problems, and weakness in body parts."),

        ("glioma", "What causes glioma?",
         "Exact cause is unknown but genetic mutations and exposure to radiation may increase risk."),

        ("glioma", "What is treatment of glioma?",
         "Treatment includes surgery, radiation therapy, and chemotherapy depending on severity and type."),

        ("glioma", "Can glioma be cured completely?",
         "Low-grade gliomas can sometimes be controlled for long periods, but high-grade gliomas are difficult to cure completely."),

        # ================= MENINGIOMA =================
        ("meningioma", "What is meningioma?",
         "Meningioma is a tumor that develops in the meninges, the protective layers of the brain and spinal cord."),

        ("meningioma", "What are symptoms of meningioma?",
         "Symptoms include headache, vision problems, seizures, and weakness depending on tumor location."),

        ("meningioma", "What causes meningioma?",
         "Causes are not fully known but radiation exposure and hormonal factors may contribute."),

        ("meningioma", "What is treatment of meningioma?",
         "Treatment includes observation, surgery, and sometimes radiation therapy."),

        ("meningioma", "Can meningioma be cured?",
         "Most meningiomas are benign and can often be completely cured with surgery."),

        # ================= PITUITARY =================
        ("pituitary", "What is pituitary tumor?",
         "A pituitary tumor is a growth in the pituitary gland which controls hormones in the body."),

        ("pituitary", "What are symptoms of pituitary tumor?",
         "Symptoms include hormonal imbalance, vision problems, fatigue, weight changes, and headaches."),

        ("pituitary", "What causes pituitary tumor?",
         "The exact cause is unknown but genetic mutations may play a role."),

        ("pituitary", "What is treatment of pituitary tumor?",
         "Treatment includes medication, surgery, and radiation therapy depending on tumor type."),

        ("pituitary", "Can pituitary tumor be cured?",
         "Many pituitary tumors can be successfully treated and controlled, especially if detected early.")
    ]

    cursor.executemany("""
    INSERT INTO knowledge (topic, question, answer)
    VALUES (?, ?, ?)
    """, data)

    conn.commit()