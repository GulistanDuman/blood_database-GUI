from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import mysql.connector

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 200, 500, 400)  # Yüksekliği logoya yer açmak için artırdım
        self.setStyleSheet("background-color: darkred;")

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Glstn12345!",
            database="blood_database"
        )
        self.cursor = self.conn.cursor(dictionary=True)

        self.is_admin = False  # Admin olup olmadığını takip edeceğiz
        self.logged_in_user = None  # Kullanıcı adını saklayacağız

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Logo ekleme
        self.logo_label = QLabel(self)
        pixmap = QPixmap("./images/background.jpg")  # Logonun yolunu ayarladım
        self.logo_label.setPixmap(pixmap.scaled(200, 150))  # Logo boyutunu ayarladım
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # "Save Life" metni ekleme
        self.save_life_label = QLabel("Save Life", self)
        self.save_life_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.save_life_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.save_life_label)

        # Username
        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        # Password
        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Buttons
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("background-color: white; color: darkred; font-weight: bold;")
        self.login_button.clicked.connect(self.validate_login)
        layout.addWidget(self.login_button)

        self.admin_login_button = QPushButton("Admin Login", self)
        self.admin_login_button.setStyleSheet("background-color: white; color: darkred; font-weight: bold;")
        self.admin_login_button.clicked.connect(self.validate_admin_login)
        layout.addWidget(self.admin_login_button)

        self.register_button = QPushButton("Sign Up", self)
        self.register_button.setStyleSheet("background-color: white; color: darkred; font-weight: bold;")
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def validate_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        user = self.cursor.fetchone()

        if user:
            self.is_admin = user.get("is_admin", False)
            self.logged_in_user = username
            QMessageBox.information(self, "Success", "Login successful!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password!")

    def validate_admin_login(self):
        username, ok1 = QInputDialog.getText(self, "Admin Login", "Enter Admin Username:")
        if not ok1 or not username:
            return

        password, ok2 = QInputDialog.getText(self, "Admin Login", "Enter Admin Password:", QLineEdit.Password)
        if not ok2 or not password:
            return

        query = "SELECT * FROM users WHERE username = %s AND password = %s AND is_admin = TRUE"
        self.cursor.execute(query, (username, password))
        user = self.cursor.fetchone()

        if user:
            self.is_admin = True
            self.logged_in_user = username
            QMessageBox.information(self, "Success", "Admin login successful!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid admin credentials!")

    def register_user(self):
        username, ok1 = QInputDialog.getText(self, "Sign Up", "Enter a username:")
        if not ok1 or not username:
            QMessageBox.warning(self, "Input Error", "Username is required.")
            return

        password, ok2 = QInputDialog.getText(self, "Sign Up", "Enter a password:", QLineEdit.Password)
        if not ok2 or not password:
            QMessageBox.warning(self, "Input Error", "Password is required.")
            return

        is_admin, ok3 = QInputDialog.getItem(self, "Admin Access", "Is this an admin account?", ["No", "Yes"], 0, False)
        is_admin = is_admin == "Yes"

        self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if self.cursor.fetchone():
            QMessageBox.warning(self, "Error", "Username already exists!")
            return

        try:
            self.cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)", (username, password, is_admin))
            self.conn.commit()
            QMessageBox.information(self, "Success", "User registered successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to register user: {e}")

    def get_logged_in_username(self):
        return self.username_input.text()
