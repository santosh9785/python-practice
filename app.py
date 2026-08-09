# from flask import Flask, render_template, request, redirect, url_for
# import sqlite3
# from database import init_db

# app = Flask(__name__)

# # Which doctor handles which condition — expand this as you add more specialities
# DOCTORS = {
#     "Cardiology": "Dr. Aditi Rao",
#     "Neurology": "Dr. Sameer Khan",
#     "Dermatology": "Dr. Priya Nair",
#     "Gastroenterology": "Dr. Arjun Mehta",
#     "General Medicine": "Dr. Kavita Singh",
# }

# @app.route("/")
# def landing():
#     return render_template("landing.html")

# @app.route("/about")
# def about():
#     return render_template("about.html")

# @app.route("/dashboard")
# def dashboard():
#     connection = sqlite3.connect("hospital.db")
#     cursor = connection.cursor()
#     cursor.execute("SELECT COUNT(*) FROM patients")
#     total_patients = cursor.fetchone()[0]
#     connection.close()
#     return render_template("dashboard.html", total_patients=total_patients, doctors=DOCTORS)

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         name = request.form["name"]
#         age = request.form["age"]
#         gender = request.form["gender"]
#         disease = request.form["disease"]
#         doctor = DOCTORS.get(disease, "Dr. Kavita Singh")
#         appointment_date = request.form["appointment_date"]

#         connection = sqlite3.connect("hospital.db")
#         cursor = connection.cursor()
#         cursor.execute(
#             "INSERT INTO patients (name, age, gender, disease, doctor, appointment_date) VALUES (?, ?, ?, ?, ?, ?)",
#             (name, age, gender, disease, doctor, appointment_date)
#         )
#         connection.commit()
#         connection.close()

#         return redirect(url_for("patients"))

#     return render_template("register.html", doctors=DOCTORS)

# @app.route("/patients")
# def patients():
#     connection = sqlite3.connect("hospital.db")
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM patients")
#     patient_list = cursor.fetchall()
#     connection.close()
#     return render_template("patients.html", patients=patient_list)

# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True)


import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection, init_db

app = Flask(__name__)
app.secret_key = "replace-this-with-a-long-random-string"

SPECIALITIES = ["Cardiology", "Neurology", "Dermatology", "Gastroenterology", "General Medicine"]

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/get-started")
def get_started():
    return render_template("get_started.html")

@app.route("/patient/signup", methods=["GET", "POST"])
def patient_signup():
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        password = request.form["password"]
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        problem = request.form["problem"]
        speciality_needed = request.form["speciality_needed"]
        appointment_date = request.form["appointment_date"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM doctors WHERE speciality = ? LIMIT 1", (speciality_needed,))
        doctor_row = cursor.fetchone()
        assigned_doctor = doctor_row["name"] if doctor_row else "To be assigned"

        try:
            cursor.execute(
                """INSERT INTO patients
                   (patient_id, password, name, age, gender, problem, speciality_needed, assigned_doctor, appointment_date)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (patient_id, generate_password_hash(password), name, age, gender,
                 problem, speciality_needed, assigned_doctor, appointment_date)
            )
            connection.commit()
        except sqlite3.IntegrityError:
            connection.close()
            return render_template(
                "patient_signup.html",
                specialities=SPECIALITIES,
                error="That Patient ID is already taken. Choose another."
            )

        connection.close()
        session["role"] = "patient"
        session["user_id"] = patient_id
        return redirect(url_for("patient_dashboard"))

    return render_template("patient_signup.html", specialities=SPECIALITIES)

@app.route("/patient/login", methods=["GET", "POST"])
def patient_login():
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
        patient = cursor.fetchone()
        connection.close()

        if patient and check_password_hash(patient["password"], password):
            session["role"] = "patient"
            session["user_id"] = patient_id
            return redirect(url_for("patient_dashboard"))

        return render_template("patient_login.html", error="Incorrect Patient ID or password.")

    return render_template("patient_login.html")

@app.route("/patient/dashboard")
def patient_dashboard():
    if session.get("role") != "patient":
        return redirect(url_for("patient_login"))

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (session["user_id"],))
    patient = cursor.fetchone()
    connection.close()

    return render_template("patient_dashboard.html", patient=patient)

@app.route("/doctor/login", methods=["GET", "POST"])
def doctor_login():
    if request.method == "POST":
        doctor_id = request.form["doctor_id"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM doctors WHERE doctor_id = ?", (doctor_id,))
        doctor = cursor.fetchone()
        connection.close()

        if doctor and check_password_hash(doctor["password"], password):
            session["role"] = "doctor"
            session["user_id"] = doctor_id
            session["doctor_name"] = doctor["name"]
            return redirect(url_for("doctor_dashboard"))

        return render_template("doctor_login.html", error="Incorrect Doctor ID or password.")

    return render_template("doctor_login.html")

@app.route("/doctor/dashboard")
def doctor_dashboard():
    if session.get("role") != "doctor":
        return redirect(url_for("doctor_login"))

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM patients WHERE assigned_doctor = ?", (session["doctor_name"],))
    my_patients = cursor.fetchall()
    connection.close()

    return render_template("doctor_dashboard.html", patients=my_patients, doctor_name=session["doctor_name"])

@app.route("/staff/login", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        staff_id = request.form["staff_id"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM staff WHERE staff_id = ?", (staff_id,))
        staff = cursor.fetchone()
        connection.close()

        if staff and check_password_hash(staff["password"], password):
            session["role"] = "staff"
            session["user_id"] = staff_id
            return redirect(url_for("staff_dashboard"))

        return render_template("staff_login.html", error="Incorrect Staff ID or password.")

    return render_template("staff_login.html")

@app.route("/staff/dashboard")
def staff_dashboard():
    if session.get("role") != "staff":
        return redirect(url_for("staff_login"))

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    connection.close()

    return render_template("staff_dashboard.html", patients=patients, doctors=doctors)

@app.route("/staff/reassign", methods=["POST"])
def staff_reassign():
    if session.get("role") != "staff":
        return redirect(url_for("staff_login"))

    patient_id = request.form["patient_id"]
    new_doctor = request.form["new_doctor"]

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE patients SET assigned_doctor = ? WHERE patient_id = ?", (new_doctor, patient_id))
    connection.commit()
    connection.close()

    return redirect(url_for("staff_dashboard"))

@app.route("/store")
def store():
    if session.get("role") != "patient":
        return redirect(url_for("patient_login"))

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    connection.close()

    return render_template("store.html", medicines=medicines)

@app.route("/store/order", methods=["POST"])
def place_order():
    if session.get("role") != "patient":
        return redirect(url_for("patient_login"))

    medicine_id = request.form["medicine_id"]
    quantity = int(request.form["quantity"])
    payment_method = request.form["payment_method"]

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO orders (patient_id, medicine_id, quantity, payment_method, status) VALUES (?, ?, ?, ?, ?)",
        (session["user_id"], medicine_id, quantity, payment_method,
         "Placed" if payment_method == "cod" else "Payment Pending")
    )
    connection.commit()
    order_id = cursor.lastrowid
    connection.close()

    if payment_method == "online":
        return redirect(url_for("mock_payment", order_id=order_id))

    return redirect(url_for("order_success", order_id=order_id))

@app.route("/store/pay/<int:order_id>")
def mock_payment(order_id):
    return render_template("mock_payment.html", order_id=order_id)

@app.route("/store/pay/<int:order_id>/confirm")
def confirm_mock_payment(order_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", ("Paid", order_id))
    connection.commit()
    connection.close()
    return redirect(url_for("order_success", order_id=order_id))

@app.route("/store/success/<int:order_id>")
def order_success(order_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT orders.*, medicines.name AS medicine_name, medicines.price
        FROM orders JOIN medicines ON orders.medicine_id = medicines.id
        WHERE orders.id = ?
    """, (order_id,))
    order = cursor.fetchone()
    connection.close()
    return render_template("order_success.html", order=order)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)