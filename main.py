from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTabWidget, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QComboBox, QDateTimeEdit, QMessageBox, QDialog, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDateTime, Qt
from database import Database
from login import LoginWindow
from PyQt5.QtWidgets import QLineEdit
import os

class DoctorPhotoViewer(QDialog):
    def __init__(self, doctor_id, db):
        super().__init__()
        self.setWindowTitle("Doctor Photo")
        self.setGeometry(300, 200, 400, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        doctor = db.fetch_query(f"SELECT name, photo_path FROM doctor WHERE ID = '{doctor_id}'")
        if doctor:
            doctor = doctor[0]
            name_label = QLabel(f"Doctor: {doctor['name']}")
            layout.addWidget(name_label)

            if doctor['photo_path']:
                if doctor['photo_path'].startswith('images/'):
                    photo_path = doctor['photo_path']
                else:
                    photo_path = os.path.join('images', doctor['photo_path'])

                if os.path.exists(photo_path):
                    pixmap = QPixmap(photo_path)
                    photo_label = QLabel()
                    photo_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
                    layout.addWidget(photo_label)
                else:
                    layout.addWidget(QLabel(f"Photo file not found at: {photo_path}"))
            else:
                layout.addWidget(QLabel("No photo available."))
        else:
            QMessageBox.warning(self, "Error", "Doctor not found!")

class MainWindow(QMainWindow):
    def __init__(self, is_admin=False, logged_in_user=None):  # is_admin değişkenini alıyoruz
        super().__init__()
        self.setWindowTitle("Blood Donation Database")
        self.setGeometry(100, 100, 1200, 800)
        self.db = Database()
        self.is_admin = is_admin  # 👈 Bunu buraya ekle!
        self.logged_in_user = logged_in_user

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.create_tabs()
    
    def get_logged_in_user_id(self):
        query = "SELECT ID FROM users WHERE username = %s"
        result = self.db.fetch_query(query, (self.logged_in_user,))
        return result[0]['ID'] if result else None


    def create_tabs(self):
        self.create_tab("Donors", self.create_donor_table, self.donor_crud)
        self.create_tab("Patients", self.create_patient_table, self.patient_crud)
        self.create_tab("Doctors", self.create_doctor_table, self.doctor_crud)
        self.create_tab("Nurses", self.create_nurse_table, self.nurse_crud)
        self.create_tab("Hospitals", self.create_hospital_table, self.hospital_crud)
        self.create_tab("Appointments", self.create_appointment_table, self.appointment_crud)
        self.create_appointment_tab()

        if self.is_admin:  # Eğer giriş yapan kullanıcı admin ise bu sekmeyi ekle
            self.create_tab("Doctors", self.create_doctor_table, self.doctor_crud)
            self.create_tab("Admin Controls", self.create_admin_table, self.admin_crud)  # Admin sekmesi eklendi


    def create_tab(self, title, table_function, crud_function):
        tab = QWidget()
        self.tabs.addTab(tab, title)
        layout = QVBoxLayout()
        tab.setLayout(layout)
        table = table_function()
        crud_buttons = crud_function(table)
        layout.addWidget(table)
        for button in crud_buttons:
            button.setStyleSheet("background-color: darkred; color: white; font-weight: bold;")
            layout.addWidget(button)

    def create_generic_table(self, headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setStyleSheet("QHeaderView::section { background-color: darkred; color: white; }")
        table.setAlternatingRowColors(True)
        return table
    

    def create_admin_table(self):
        return self.create_generic_table(["Action", "Description"])
 
    def create_donor_table(self):
        return self.create_generic_table(["ID", "Name", "Blood Group", "Age", "Disease"])

    def create_patient_table(self):
        return self.create_generic_table(["ID", "Name", "Address", "Need Blood Group", "Host Name"])

    def create_doctor_table(self):
        return self.create_generic_table(["ID", "Name", "Shift", "Vigil"])

    def create_nurse_table(self):
        return self.create_generic_table(["ID", "Name", "Shift", "Vigil"])

    def create_hospital_table(self):
        return self.create_generic_table(["Host Name", "Address", "Capacity", "Dept Host", "Block"])

    def create_appointment_table(self):
        return self.create_generic_table(["Block", "Time", "Date", "Doctor", "Patient", "Hospital"])

    def donor_crud(self, table):
        def list_donors():
            donors = self.db.fetch_query("SELECT * FROM donor")
            table.setRowCount(len(donors))
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["ID", "Name", "Blood Group", "Age", "Disease"])
            for row_index, donor in enumerate(donors):
                for col_index, key in enumerate(["ID", "name", "blood_group", "age", "disease"]):
                    table.setItem(row_index, col_index, QTableWidgetItem(str(donor[key])))

        def compatible_donors():
            compatible = self.db.fetch_query(
                """
                SELECT d.name AS Donor, p.name AS Recipient
                FROM donor d
                JOIN patient p ON d.blood_group = p.need_bloodgroup
                """
            )
            table.setRowCount(len(compatible))
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Donor", "Recipient"])
            for row_index, pair in enumerate(compatible):
                table.setItem(row_index, 0, QTableWidgetItem(pair['Donor']))
                table.setItem(row_index, 1, QTableWidgetItem(pair['Recipient']))

        def add_donor():
            name, ok = QInputDialog.getText(self, "Add Donor", "Name:")
            if not ok or not name:
                return
            donor_id, ok = QInputDialog.getText(self, "Add Donor", "ID:")
            if not ok or not donor_id:
                return
            age, ok = QInputDialog.getInt(self, "Add Donor", "Age:")
            if not ok:
                return
            blood_group, ok = QInputDialog.getText(self, "Add Donor", "Blood Group:")
            if not ok or not blood_group:
                return
            disease, ok = QInputDialog.getText(self, "Add Donor", "Disease (optional):")
            if not ok:
                disease = None

            try:
                self.db.add_donor(name=name, donor_id=donor_id, age=age, blood_group=blood_group, disease=disease)
                QMessageBox.information(self, "Success", "Donor successfully added.")
                list_donors()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while adding donor: {e}")
        
        def delete_donor():  # 👈 Yeni eklenen fonksiyon
            donor_id, ok = QInputDialog.getText(self, "Delete Donor", "Enter Donor ID:")
            if not ok or not donor_id:
                return

            self.db.cursor.execute("DELETE FROM donor WHERE ID = %s", (donor_id,))
            self.db.conn.commit()
            QMessageBox.information(self, "Success", "Donor deleted successfully!")
            list_donors()

        list_button = QPushButton("List Donors")
        list_button.clicked.connect(list_donors)

        add_button = QPushButton("Add Donor")
        add_button.clicked.connect(add_donor)

        compatible_button = QPushButton("Compatible Donors")
        compatible_button.clicked.connect(compatible_donors)

        return [list_button, add_button, compatible_button]

    def patient_crud(self, table):
        def list_patients():
            patients = self.db.fetch_query("SELECT * FROM patient")
            table.setRowCount(len(patients))
            for row_index, patient in enumerate(patients):
                for col_index, key in enumerate(["ID", "name", "address", "need_bloodgroup", "host_name"]):
                    table.setItem(row_index, col_index, QTableWidgetItem(str(patient[key])))

        list_button = QPushButton("List Patients")
        list_button.clicked.connect(list_patients)
        return [list_button]
    
    
    def admin_crud(self, table):
        def add_user():
            username, ok = QInputDialog.getText(self, "Add User", "Enter Username:")
            if not ok or not username:
                return
            password, ok = QInputDialog.getText(self, "Add User", "Enter Password:", QLineEdit.Password)
            if not ok or not password:
                return
            is_admin, ok = QInputDialog.getItem(self, "Set Admin Status", "Is Admin?", ["No", "Yes"], 0, False)
            is_admin = True if is_admin == "Yes" else False

            try:
                self.db.cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)", 
                                   (username, password, is_admin))
                self.db.conn.commit()
                QMessageBox.information(self, "Success", "User added successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

        def delete_user():
            username, ok = QInputDialog.getText(self, "Delete User", "Enter Username:")
            if not ok or not username:
                return

            try:
                self.db.cursor.execute("DELETE FROM users WHERE username = %s", (username,))
                self.db.conn.commit()
                QMessageBox.information(self, "Success", "User deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

        def add_entry(table_name, fields):
            values = []
            for field in fields:
                value, ok = QInputDialog.getText(self, f"Add {table_name.capitalize()}", f"Enter {field}:")
                if not ok or not value:
                    return
                values.append(value)

            try:
                placeholders = ", ".join(["%s"] * len(fields))
                field_names = ", ".join(fields)
                self.db.cursor.execute(f"INSERT INTO {table_name} ({field_names}) VALUES ({placeholders})", tuple(values))
                self.db.conn.commit()
                QMessageBox.information(self, "Success", f"{table_name.capitalize()} added successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

        def delete_entry(table_name, entry_id):
            try:
                self.db.cursor.execute(f"DELETE FROM {table_name} WHERE ID = %s", (entry_id,))
                self.db.conn.commit()
                QMessageBox.information(self, "Success", f"{table_name.capitalize()} deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

        def add_donor():
            add_entry("donor", ["ID", "name", "blood_group", "age", "disease"])

        def delete_donor():
            donor_id, ok = QInputDialog.getText(self, "Delete Donor", "Enter Donor ID:")
            if ok and donor_id:
                delete_entry("donor", donor_id)

        def add_patient():
            add_entry("patient", ["ID", "name", "address", "need_bloodgroup", "host_name"])

        def delete_patient():
            patient_id, ok = QInputDialog.getText(self, "Delete Patient", "Enter Patient ID:")
            if ok and patient_id:
                delete_entry("patient", patient_id)

        def add_doctor():
            add_entry("doctor", ["ID", "name", "shift", "vigil"])

        def delete_doctor():
            doctor_id, ok = QInputDialog.getText(self, "Delete Doctor", "Enter Doctor ID:")
            if ok and doctor_id:
                delete_entry("doctor", doctor_id)

        def add_nurse():
            add_entry("nurse", ["ID", "name", "shift", "vigil"])

        def delete_nurse():
            nurse_id, ok = QInputDialog.getText(self, "Delete Nurse", "Enter Nurse ID:")
            if ok and nurse_id:
                delete_entry("nurse", nurse_id)

         # 📌 Admin panelindeki butonlar
        add_user_button = QPushButton("Add User")
        add_user_button.clicked.connect(add_user)

        delete_user_button = QPushButton("Delete User")
        delete_user_button.clicked.connect(delete_user)

        add_donor_button = QPushButton("Add Donor")
        add_donor_button.clicked.connect(add_donor)

        delete_donor_button = QPushButton("Delete Donor")
        delete_donor_button.clicked.connect(delete_donor)

        add_patient_button = QPushButton("Add Patient")
        add_patient_button.clicked.connect(add_patient)

        delete_patient_button = QPushButton("Delete Patient")
        delete_patient_button.clicked.connect(delete_patient)

        add_doctor_button = QPushButton("Add Doctor")
        add_doctor_button.clicked.connect(add_doctor)

        delete_doctor_button = QPushButton("Delete Doctor")
        delete_doctor_button.clicked.connect(delete_doctor)

        add_nurse_button = QPushButton("Add Nurse")
        add_nurse_button.clicked.connect(add_nurse)

        delete_nurse_button = QPushButton("Delete Nurse")
        delete_nurse_button.clicked.connect(delete_nurse)

        return [
            add_user_button, delete_user_button,
            add_donor_button, delete_donor_button,
            add_patient_button, delete_patient_button,
            add_doctor_button, delete_doctor_button,
            add_nurse_button, delete_nurse_button
        ]

    def doctor_crud(self, table):
        def list_doctors():
            doctors = self.db.fetch_query("SELECT * FROM doctor")
            table.setRowCount(len(doctors))
            for row_index, doctor in enumerate(doctors):
                for col_index, key in enumerate(["ID", "name", "shift", "vigil"]):
                    table.setItem(row_index, col_index, QTableWidgetItem(str(doctor[key])))

        list_button = QPushButton("List Doctors")
        list_button.clicked.connect(list_doctors)

        def view_doctor_photo():
            selected_row = table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Selection Error", "Please select a doctor to view photo.")
                return

            doctor_id = table.item(selected_row, 0).text()
            photo_dialog = DoctorPhotoViewer(doctor_id, self.db)
            photo_dialog.exec_()

        photo_button = QPushButton("View Photo")
        photo_button.clicked.connect(view_doctor_photo)
        return [list_button, photo_button]

    def nurse_crud(self, table):
        def list_nurses():
            nurses = self.db.fetch_query("SELECT * FROM nurse")
            table.setRowCount(len(nurses))
            for row_index, nurse in enumerate(nurses):
                for col_index, key in enumerate(["ID", "name", "shift", "vigil"]):
                    table.setItem(row_index, col_index, QTableWidgetItem(str(nurse[key])))

        list_button = QPushButton("List Nurses")
        list_button.clicked.connect(list_nurses)
        return [list_button]

    def hospital_crud(self, table):
        def list_hospitals():
            hospitals = self.db.fetch_query("SELECT * FROM hospital")
            table.setRowCount(len(hospitals))
            for row_index, hospital in enumerate(hospitals):
                for col_index, key in enumerate(["host_name", "address", "capacity", "dept_host", "block"]):
                    table.setItem(row_index, col_index, QTableWidgetItem(str(hospital[key])))

        list_button = QPushButton("List Hospitals")
        list_button.clicked.connect(list_hospitals)
        return [list_button]

    def appointment_crud(self, table):
        def list_appointments():
            appointments = self.db.fetch_query(
                """
                SELECT 
                    a.block, a.time, a.date, 
                    COALESCE(d.name, 'Unknown') AS doctor, 
                    COALESCE(p.name, 'Unknown') AS patient, 
                    COALESCE(h.host_name, 'Unknown') AS hospital
                FROM appointment a
                LEFT JOIN doctor d ON a.doctor_id = d.ID
                LEFT JOIN patient p ON a.patient_id = p.ID
                LEFT JOIN hospital h ON a.hospital_id = h.host_name
                """
            )
            table.setRowCount(len(appointments))
            table.setColumnCount(6)
            table.setHorizontalHeaderLabels(["Block", "Time", "Date", "Doctor", "Patient", "Hospital"])
            for row_index, appointment in enumerate(appointments):
                for col_index, key in enumerate(["block", "time", "date", "doctor", "patient", "hospital"]):
                    table.setItem(row_index, col_index, QTableWidgetItem(str(appointment[key])))

        list_button = QPushButton("List Appointments")
        list_button.clicked.connect(list_appointments)
        

        cancel_button = QPushButton("Cancel Appointment")
        cancel_button.clicked.connect(self.cancel_appointment)

        return [list_button, cancel_button]
    
    def cancel_appointment(self):
        try:
            patient_name = self.logged_in_user  # Kullanıcı adı
            if not patient_name:
                QMessageBox.warning(self, "Error", "User not found. Please log in again.")
                return

            # Kullanıcının randevularını getir (Eğer ID ile kontrol ediyorsan, doğru SQL sorgusunu kullan!)
            query = "SELECT ID, date, time, hospital_id FROM appointment WHERE patient_id = %s"
            appointments = self.db.fetch_query(query, (self.logged_in_user,))

            if not appointments:
                QMessageBox.information(self, "No Appointments", "You have no scheduled appointments.")
                return

            # Kullanıcının iptal edebileceği randevuları listele
            appointment_choices = [f"{apt['date']} {apt['time']} at {apt['hospital_id']}" for apt in appointments]
            appointment_ids = [apt['ID'] for apt in appointments]

            selected_appointment, ok = QInputDialog.getItem(self, "Cancel Appointment", "Select an appointment to cancel:", appointment_choices, 0, False)
            if not ok or not selected_appointment:
                return

            # Seçilen randevunun ID'sini al
            selected_index = appointment_choices.index(selected_appointment)
            selected_appointment_id = appointment_ids[selected_index]

            # Veritabanından sil
            delete_query = "DELETE FROM appointment WHERE ID = %s"
            self.db.cursor.execute(delete_query, (selected_appointment_id,))
            self.db.conn.commit()

            QMessageBox.information(self, "Success", "Your appointment has been successfully canceled!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def create_appointment_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        patient_label = QLabel("Select Patient:")
        layout.addWidget(patient_label)

        self.patient_dropdown = QComboBox()
        patients = self.db.fetch_query("SELECT ID, name FROM patient")
        for patient in patients:
            self.patient_dropdown.addItem(patient['name'], patient['ID'])
        layout.addWidget(self.patient_dropdown)

        doctor_label = QLabel("Select Doctor:")
        layout.addWidget(doctor_label)

        self.doctor_dropdown = QComboBox()
        doctors = self.db.fetch_query("SELECT ID, name FROM doctor")
        for doctor in doctors:
            self.doctor_dropdown.addItem(doctor['name'], doctor['ID'])
        layout.addWidget(self.doctor_dropdown)

        hospital_label = QLabel("Select Hospital:")
        layout.addWidget(hospital_label)

        self.hospital_dropdown = QComboBox()
        hospitals = self.db.fetch_query("SELECT host_name, address FROM hospital")
        for hospital in hospitals:
            self.hospital_dropdown.addItem(hospital['host_name'], hospital['host_name'])
        layout.addWidget(self.hospital_dropdown)

        time_label = QLabel("Select Appointment Time:")
        layout.addWidget(time_label)

        self.time_input = QDateTimeEdit()
        self.time_input.setCalendarPopup(True)
        self.time_input.setMinimumDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.time_input)

        book_button = QPushButton("Book Appointment")
        book_button.setStyleSheet("background-color: darkred; color: white; font-weight: bold;")
        book_button.clicked.connect(self.book_appointment)
        layout.addWidget(book_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Book Appointment")

    def book_appointment(self):
        patient_id = self.patient_dropdown.currentData()
        doctor_id = self.doctor_dropdown.currentData()
        hospital_id = self.hospital_dropdown.currentText()
        appointment_time = self.time_input.dateTime()

        if not patient_id:
            QMessageBox.warning(self, "Missing Selection", "Please select a patient.")
            return

        if not doctor_id:
            QMessageBox.warning(self, "Missing Selection", "Please select a doctor.")
            return

        if not hospital_id:
            QMessageBox.warning(self, "Missing Selection", "Please select a hospital.")
            return

        current_time = QDateTime.currentDateTime()
        if appointment_time < current_time:
            QMessageBox.warning(self, "Invalid Date", "You cannot book an appointment in the past.")
            return

        query_check = """
            SELECT * FROM appointment
            WHERE date = %s AND time = %s AND hospital_id = %s
        """
        self.db.cursor.execute(query_check, (appointment_time.toString("yyyy-MM-dd"), appointment_time.toString("HH:mm:ss"), hospital_id))
        conflict = self.db.cursor.fetchone()

        if conflict:
            QMessageBox.warning(self, "Conflict", "An appointment already exists for the selected time and hospital.")
            return

        query_insert = """
            INSERT INTO appointment (block, date, time, hospital_id, patient_id, doctor_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db.cursor.execute(query_insert, ("A3", appointment_time.toString("yyyy-MM-dd"), appointment_time.toString("HH:mm:ss"), hospital_id, patient_id, doctor_id))
        self.db.conn.commit()

        QMessageBox.information(self, "Success", "Your appointment has been booked successfully!")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        is_admin = login_window.is_admin  # 👈 Admin olup olmadığını kontrol et
        logged_in_user = login_window.get_logged_in_username()  # 👈 Kullanıcı adını al
        main_window = MainWindow(is_admin=is_admin, logged_in_user=logged_in_user)  # 👈 Kullanıcı adı ile ana pencereyi başlat
        main_window.show()
        sys.exit(app.exec_())

