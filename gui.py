from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTabWidget, QPushButton, QWidget,
    QTableWidget, QTableWidgetItem, QInputDialog
)
from PyQt5.QtGui import QBrush, QColor, QPalette
from PyQt5.QtCore import Qt
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blood Donation Database")
        self.setGeometry(100, 100, 1200, 800)

        self.db = Database()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { background: darkred; color: white; font-weight: bold; }")
        self.layout.addWidget(self.tabs)

        self.create_tab("Donors", self.create_donor_table, self.donor_crud)
        self.create_tab("Patients", self.create_patient_table, self.patient_crud)
        self.create_tab("Nurses", self.create_nurse_table, self.nurse_crud)
        self.create_tab("Appointments", self.create_appointment_table, self.appointment_crud)
        self.create_tab("Hospitals", self.create_hospital_table, self.hospital_crud)

        self.setStyleSheet("background-color: #f5f5f5;")

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

    def create_donor_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Name", "Blood Group", "Age", "Disease"])
        table.setStyleSheet("QHeaderView::section { background-color: darkred; color: white; }")
        table.setAlternatingRowColors(True)
        table.setPalette(self.create_table_palette())
        self.donor_table = table
        return table

    def create_table_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor("#f5f5f5"))
        palette.setColor(QPalette.AlternateBase, QColor("#ffffff"))
        return palette

    def donor_crud(self, table):
        def list_donors():
            donors = self.db.fetch_query("SELECT * FROM donor")
            table.setRowCount(len(donors))
            for row_index, donor in enumerate(donors):
                for col_index, key in enumerate(["ID", "name", "blood_group", "age", "disease"]):
                    item = QTableWidgetItem(str(donor[key]))
                    if row_index % 2 == 0:
                        item.setBackground(QBrush(QColor("#f5f5f5")))
                    else:
                        item.setBackground(QBrush(QColor("#ffffff")))
                    table.setItem(row_index, col_index, item)

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
            if not ok:
                return
            disease, ok = QInputDialog.getText(self, "Add Donor", "Disease (optional):")
            if not ok:
                disease = None
            self.db.add_donor(name, donor_id, age, blood_group, disease)
            list_donors()

        def delete_donor():
            donor_id, ok = QInputDialog.getText(self, "Delete Donor", "Enter Donor ID:")
            if not ok or not donor_id:
                return
            self.db.delete_donor(donor_id)
            list_donors()

        def update_donor():
            donor_id, ok = QInputDialog.getText(self, "Update Donor", "Enter Donor ID:")
            if not ok or not donor_id:
                return
            name, ok = QInputDialog.getText(self, "Update Donor", "New Name (leave blank to skip):")
            if not ok:
                name = None
            age, ok = QInputDialog.getInt(self, "Update Donor", "New Age (0 to skip):")
            if not ok or age == 0:
                age = None
            blood_group, ok = QInputDialog.getText(self, "Update Donor", "New Blood Group (leave blank to skip):")
            if not ok:
                blood_group = None
            disease, ok = QInputDialog.getText(self, "Update Donor", "New Disease (leave blank to skip):")
            if not ok:
                disease = None
            self.db.update_donor(donor_id, name=name, age=age, blood_group=blood_group, disease=disease)
            list_donors()

        list_button = QPushButton("List Donors")
        list_button.clicked.connect(list_donors)

        add_button = QPushButton("Add Donor")
        add_button.clicked.connect(add_donor)

        delete_button = QPushButton("Delete Donor")
        delete_button.clicked.connect(delete_donor)

        update_button = QPushButton("Update Donor")
        update_button.clicked.connect(update_donor)

        return [list_button, add_button, delete_button, update_button]

    def create_patient_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Name", "Address", "Need Blood Group", "Host Name"])
        table.setStyleSheet("QHeaderView::section { background-color: darkred; color: white; }")
        table.setAlternatingRowColors(True)
        table.setPalette(self.create_table_palette())
        self.patient_table = table
        return table

    def patient_crud(self, table):
        def list_patients():
            patients = self.db.fetch_query("SELECT * FROM patient")
            table.setRowCount(len(patients))
            for row_index, patient in enumerate(patients):
                for col_index, key in enumerate(["ID", "name", "address", "need_bloodgroup", "host_name"]):
                    item = QTableWidgetItem(str(patient[key]))
                    if row_index % 2 == 0:
                        item.setBackground(QBrush(QColor("#f5f5f5")))
                    else:
                        item.setBackground(QBrush(QColor("#ffffff")))
                    table.setItem(row_index, col_index, item)

        def add_patient():
            patient_id, ok = QInputDialog.getText(self, "Add Patient", "Enter Patient ID:")
            if not ok or not patient_id:
                return
            name, ok = QInputDialog.getText(self, "Add Patient", "Enter Name:")
            if not ok or not name:
                return
            address, ok = QInputDialog.getText(self, "Add Patient", "Enter Address:")
            if not ok or not address:
                return
            need_bloodgroup, ok = QInputDialog.getText(self, "Add Patient", "Enter Needed Blood Group:")
            if not ok or not need_bloodgroup:
                return
            host_name, ok = QInputDialog.getText(self, "Add Patient", "Enter Host Name:")
            if not ok or not host_name:
                return
            self.db.cursor.execute(
                "INSERT INTO patient (ID, name, address, need_bloodgroup, host_name) VALUES (%s, %s, %s, %s, %s)",
                (patient_id, name, address, need_bloodgroup, host_name)
            )
            self.db.conn.commit()
            list_patients()

        list_button = QPushButton("List Patients")
        list_button.clicked.connect(list_patients)

        add_button = QPushButton("Add Patient")
        add_button.clicked.connect(add_patient)

        return [list_button, add_button]

    def create_nurse_table(self):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Name", "Shift", "Vigil"])
        table.setStyleSheet("QHeaderView::section { background-color: darkred; color: white; }")
        table.setAlternatingRowColors(True)
        table.setPalette(self.create_table_palette())
        self.nurse_table = table
        return table

    def nurse_crud(self, table):
        def list_nurses():
            nurses = self.db.fetch_query("SELECT * FROM nurse")
            table.setRowCount(len(nurses))
            for row_index, nurse in enumerate(nurses):
                for col_index, key in enumerate(["ID", "name", "shift", "vigil"]):
                    item = QTableWidgetItem(str(nurse[key]))
                    if row_index % 2 == 0:
                        item.setBackground(QBrush(QColor("#f5f5f5")))
                    else:
                        item.setBackground(QBrush(QColor("#ffffff")))
                    table.setItem(row_index, col_index, item)

        list_button = QPushButton("List Nurses")
        list_button.clicked.connect(list_nurses)
        return [list_button]

    def create_appointment_table(self):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Block", "Time", "Date", "Room Number"])
        table.setStyleSheet("QHeaderView::section { background-color: darkred; color: white; }")
        table.setAlternatingRowColors(True)
        table.setPalette(self.create_table_palette())
        self.appointment_table = table
        return table

    def appointment_crud(self, table):
        def list_appointments():
            appointments = self.db.fetch_query("SELECT * FROM appointment")
            table.setRowCount(len(appointments))
            for row_index, appointment in enumerate(appointments):
                for col_index, key in enumerate(["block", "time", "date", "room_number"]):
                    item = QTableWidgetItem(str(appointment[key]))
                    if row_index % 2 == 0:
                        item.setBackground(QBrush(QColor("#f5f5f5")))
                    else:
                        item.setBackground(QBrush(QColor("#ffffff")))
                    table.setItem(row_index, col_index, item)

        list_button = QPushButton("List Appointments")
        list_button.clicked.connect(list_appointments)
        return [list_button]

    def create_hospital_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Host Name", "Address", "Capacity", "Dept Host", "Block"])
        table.setStyleSheet("QHeaderView::section { background-color: darkred; color: white; }")
        table.setAlternatingRowColors(True)
        table.setPalette(self.create_table_palette())
        self.hospital_table = table
        return table

    def hospital_crud(self, table):
        def list_hospitals():
            hospitals = self.db.fetch_query("SELECT * FROM hospital")
            table.setRowCount(len(hospitals))
            for row_index, hospital in enumerate(hospitals):
                for col_index, key in enumerate(["host_name", "address", "capacity", "dept_host", "block"]):
                    item = QTableWidgetItem(str(hospital[key]))
                    if row_index % 2 == 0:
                        item.setBackground(QBrush(QColor("#f5f5f5")))
                    else:
                        item.setBackground(QBrush(QColor("#ffffff")))
                    table.setItem(row_index, col_index, item)

        list_button = QPushButton("List Hospitals")
        list_button.clicked.connect(list_hospitals)
        return [list_button]

    def closeEvent(self, event):
        self.db.close_connection()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
