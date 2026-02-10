from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QPushButton,QAbstractButton, QLineEdit, QLabel, QMessageBox, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import api  
import traceback
from api import BASE_URL

class LoginWindow(QWidget):
    def __init__(self, switch_callback=None):
        super().__init__()
        self.switch_callback = switch_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login - Chemical Visualizer")
        self.setFixedSize(1000, 800) 
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #a8e063, stop:1 #fbedad);") 
    
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        self.card = QFrame()
        self.card.setFixedSize(400, 450) 
        self.card.setStyleSheet("QFrame {background-color: white; border-radius: 12px;} QLabel { background: transparent; }")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)
        title = QLabel("🧪 Equip Visualizer")
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setStyleSheet("color: #2d5a27;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 12px; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 14px;")
        card_layout.addWidget(self.username_input)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 12px; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 14px;")
        card_layout.addWidget(self.password_input)

        login_button = QPushButton("Log In")
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.setFixedHeight(45)
        login_button.setStyleSheet("background-color: #2d5a27; color: white; font-weight: bold; border-radius: 6px;")
        login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(login_button)

        register_window_link = QPushButton("Need an account? Sign Up")
        register_window_link.setCursor(Qt.PointingHandCursor)
        register_window_link.setStyleSheet("color: #2d5a27; border: none; background: transparent; text-decoration: underline;")
        register_window_link.clicked.connect(self.open_register)
        card_layout.addWidget(register_window_link)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e53e3e; font-size: 12px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.error_label)

        main_layout.addWidget(self.card)
        self.setLayout(main_layout)

    def handle_login(self):
        self.error_label.setText("Connecting...")
        QApplication.processEvents()
        try:
            response = api.login_request(self.username_input.text(), self.password_input.text())
            if response.status_code == 200:
                token = response.json().get('access')
                try:
                    from dashboard import DashboardWindow 
                    print(f"DEBUG: Creating DashboardWindow with token {token[:20]}...")
                    self.dashboard = DashboardWindow(token)
                    print("DEBUG: DashboardWindow created successfully")
                    self.dashboard.show()
                    print("DEBUG: DashboardWindow shown")
                    self.close()
                except Exception as dashboard_err:
                    tb = traceback.format_exc()
                    print(f"DEBUG: Dashboard init failed: {dashboard_err}\n{tb}")
                    self.error_label.setText(f"Dashboard error: {dashboard_err}")
                    QMessageBox.critical(self, "Dashboard Error", f"Could not load dashboard:\n{dashboard_err}\n\nSee console for details.")
            else:
                try:
                    err = response.json()
                except Exception:
                    err = response.text
                self.error_label.setText(f"Login Failed: {response.status_code} - {err}")
        except Exception as e:
            tb = traceback.format_exc()
            print(f"DEBUG ERROR: {e}\n{tb}")
            self.error_label.setText(f"Internal error: {e}")
            QMessageBox.critical(self, "Internal Error", f"An unexpected error occurred:\n{e}\n\nSee console for full traceback.")

    def open_register(self):
        self.reg_win = RegisterWindow()
        self.reg_win.show()
        self.close()

class RegisterWindow(QWidget):
    def __init__(self, switch_callback=None):
        super().__init__()
        self.switch_callback = switch_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Register - Chemical Visualizer")
        self.setFixedSize(1000, 800)
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fbedad, stop:1 #a8e063);")
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        self.card = QFrame()
        self.card.setFixedSize(400, 450)
        # Match Login card styles and ensure labels are transparent
        self.card.setStyleSheet("QFrame {background-color: white; border-radius: 12px;} QLabel { background: transparent; }")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)
        title = QLabel("🧪 Create Account")
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setStyleSheet("color: #2d5a27;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 12px; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 14px;")
        card_layout.addWidget(self.username_input)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 12px; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 14px;")
        card_layout.addWidget(self.password_input)

        signup_button = QPushButton("Sign Up")
        signup_button.setCursor(Qt.PointingHandCursor)
        signup_button.setFixedHeight(45)
        signup_button.setStyleSheet("background-color: #2d5a27; color: white; font-weight: bold; border-radius: 6px;")
        signup_button.clicked.connect(self.handle_register)
        card_layout.addWidget(signup_button)

        back_button = QPushButton("Already have an account? Log In")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.setStyleSheet("color: #2d5a27; border: none; background: transparent; text-decoration: underline;")
        back_button.clicked.connect(self.back_to_login)
        card_layout.addWidget(back_button)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e53e3e; font-size: 12px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.error_label)

        main_layout.addWidget(self.card)
        self.setLayout(main_layout)

    def handle_register(self):
        user = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not user or not password:
            self.error_label.setText("Please provide both username and password.")
            return
        
        self.error_label.setText("Connecting...")
        QApplication.processEvents()
        try:
            response = api.register_request(user, password)
            if response.status_code in (200, 201):
                QMessageBox.information(self, "Success", "Account created!")
                self.back_to_login()
            else:
                try:
                    err = response.json()
                except Exception:
                    err = response.text
                self.error_label.setText(f"Registration Failed: {response.status_code} - {err}")
        except Exception as e:
            tb = traceback.format_exc()
            print(f"REGISTER DEBUG ERROR: {e}\n{tb}")
            self.error_label.setText(f"Internal error: {e}")
            QMessageBox.critical(self, "Registration Error", f"Could not register user:\n{e}\n\nSee console for details.")

    def back_to_login(self):
        # If a switch callback was provided, call it to let the caller manage window switching.
        if self.switch_callback:
            try:
                self.switch_callback()
            except Exception:
                pass
        # Fallback: open a fresh LoginWindow
        self.login_win = LoginWindow()
        self.login_win.show()
        self.close()