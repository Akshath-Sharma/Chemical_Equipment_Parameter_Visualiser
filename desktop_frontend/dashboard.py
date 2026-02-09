import os
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import webbrowser
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QListWidget, QListWidgetItem, QDialog, QMenu, QAction)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt
from api import BASE_URL, download_csv_request
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QLabel, QMessageBox, QFileDialog, QFrame, QHeaderView)


class DashboardWindow(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.initUI()
        self.load_history()
        self.selected_file = None
    def initUI(self):
        # Setting the main dashboard design and layout
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.showMaximized() 
        self.setStyleSheet("background-color: #D1FFBD;") # check this color once

        main_dash_layout = QVBoxLayout(self)
        main_dash_layout.setContentsMargins(0, 0, 0, 0)
        main_dash_layout.setSpacing(0)
        
        # Container for the headings
        placeholder_top = QFrame()
        placeholder_top.setFixedHeight(70)
        placeholder_top.setStyleSheet("background-color: #ffffff; border-bottom: 2px solid #e2e8f0;")
        top_ph_layout = QHBoxLayout(placeholder_top)
        top_ph_layout.setContentsMargins(30, 10, 30, 10)
        top_ph_title = QLabel("🧪 Chemical Equipment Parameter Visualizer Dashboard")
        top_ph_title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        top_ph_title.setStyleSheet("color: #2d3748;")
        top_ph_layout.addWidget(top_ph_title)
        top_ph_layout.addStretch()

        # Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setFixedHeight(35)
        logout_button.setStyleSheet("""
            QPushButton {background-color: #f56565; color: white; border-radius: 8px; font-weight: bold; padding: 0 20px; font-size: 14px;}
            QPushButton:hover {background-color: #e53e3e;}
        """)
        logout_button.clicked.connect(self.back_to_login)
        top_ph_layout.addWidget(logout_button)
        main_dash_layout.addWidget(placeholder_top)

        # Content area 
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Main Horizontal Layout
        layout_container = QHBoxLayout()
        layout_container.setSpacing(20)

        # --- Left Sidebar containing Equipment table ---
        left_sidebar = QFrame()
        left_sidebar.setFixedWidth(450)
        left_sidebar.setStyleSheet("background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0;")
        left_sidebar_layout = QVBoxLayout(left_sidebar)
        left_sidebar_layout.setContentsMargins(15, 20, 15, 25)
        left_sidebar_title = QLabel("Equipment Data Preview")
        left_sidebar_title.setFont(QFont('Segoe UI', 14, QFont.Bold))
        left_sidebar_title.setStyleSheet("color: #2d3748; margin-bottom: 10px;")
        left_sidebar_layout.addWidget(left_sidebar_title)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(4)
        self.data_table.setHorizontalHeaderLabels(['Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.data_table.setStyleSheet("""
            QTableWidget {border: 1px solid #e2e8f0; border-radius: 6px; gridline-color: #e2e8f0; background-color: white; alternate-background-color: #f0fdf4;}
            QHeaderView::section {background-color: #f7fafc; padding: 8px; border: none; font-weight: bold; color: #2d3748; border-bottom: 2px solid #a8e063;}
            QTableWidget::item {padding: 8px;}   
        """)
        header = self.data_table.horizontalHeader()
        for i in range(4): header.setSectionResizeMode(i, QHeaderView.Stretch)
        content_layout.addWidget(self.data_table, 1)        
        self.data_table.setAlternatingRowColors(True)
        left_sidebar_layout.addWidget(self.data_table)
        
        table_footer = QLabel("*Showing first 10 rows of data")
        table_footer.setStyleSheet("color: #7f8c8d; font-size: 11px; margin-top: 5px;")
        left_sidebar_layout.addWidget(table_footer)

        # --- (Center)MAIN PANEL---
        main_content = QVBoxLayout()
        main_content.setSpacing(20)
        
        # Upload Feature
        upload = QFrame()
        upload.setFixedHeight(150)
        upload.setStyleSheet("background-color: #ffffff; border-radius: 12px; border: 1px solid #e0e0e0;")
        analyse_layout = QVBoxLayout(upload)
        analyse_layout.setContentsMargins(25, 20, 15, 20)
        analyse_row = QHBoxLayout()
        analyse_row.setSpacing(15)

        # BRowsing button declaration
        self.upload_button = QPushButton("Browse...")
        self.upload_button.setFixedHeight(70)
        self.upload_button.setFixedWidth(120)
        self.upload_button.setCursor(Qt.PointingHandCursor)
        self.upload_button.setStyleSheet("""
            QPushButton {background-color: #ffffff;color: #333;border: 1px solid #cbd5e0;border-radius: 6px;font-size: 17px;text-align: left;padding-left: 10px;}
            QPushButton:hover {background-color: #f7fafc; border-color: #a0aec0;}
        """)
        self.upload_button.clicked.connect(self.browse_file)
        analyse_row.addWidget(self.upload_button)
        
        # File name label
        self.filename_label = QLabel("No file selected.")
        self.filename_label.setStyleSheet("color: #718096; font-size: 14px;")
        analyse_row.addWidget(self.filename_label, stretch=1)
        # Analyse button declaration
        self.analyse_file = QPushButton("☁ Analyze CSV File")
        self.analyse_file.setFixedHeight(40)
        self.analyse_file.setFixedWidth(200)
        self.analyse_file.setCursor(Qt.PointingHandCursor)
        self.analyse_file.setStyleSheet("""
            QPushButton {background-color: #48bb78; color: white; border-radius: 6px; font-weight: bold; font-size: 17px;}
            QPushButton:hover {background-color: #38a169;}
            QPushButton:disabled {background-color: #a0aec0; cursor: not-allowed;}
        """)
        self.analyse_file.clicked.connect(self.upload_file)
        self.analyse_file.setDisabled(False)
        analyse_row.addWidget(self.analyse_file)
        analyse_layout.addLayout(analyse_row)
        main_content.addWidget(upload, stretch=1)

        # Statistics and Chart 
        chart = QFrame()
        chart.setStyleSheet("background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0;")
        chart_layout = QVBoxLayout(chart)
        chart_layout.setContentsMargins(25, 20, 25, 20)
        
        # Summary Title
        summary_title = QLabel("📊 Summary")
        summary_title.setFont(QFont('Segoe UI', 15, QFont.Bold))
        summary_title.setStyleSheet("color: #2d3748; margin-bottom: 5px;")
        chart_layout.addWidget(summary_title)

        # Statistics Row
        self.stats_frame = QFrame()
        self.stats_frame.setVisible(False)  
        self.stats_frame.setStyleSheet("background-color: transparent;")
        stats_layout = QHBoxLayout(self.stats_frame)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(15)
        
        self.total_label = self.create_stat_cards("Total", "0", is_clickable=True)
        self.flow_label = self.create_stat_cards("Avg_Flowrate", "0.00")
        self.press_label = self.create_stat_cards("Avg_Pressure", "0.00")
        self.temp_label = self.create_stat_cards("Avg_Temperature", "0.00")
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.flow_label)
        stats_layout.addWidget(self.press_label)
        stats_layout.addWidget(self.temp_label)
        chart_layout.addWidget(self.stats_frame)
        self.total_label.mousePressEvent = lambda event: self.show_distribution_pie()

        # Chart 
        self.figure = Figure(figsize=(10, 5), dpi=100, facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        chart_layout.addWidget(self.canvas, stretch=1)
        main_content.addWidget(chart, stretch=1)  

        # --- SIDEBAR(RIGHT SIDE) ---
        right_sidebar = QFrame()
        right_sidebar.setFixedWidth(300)
        right_sidebar.setStyleSheet("background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0;")
        right_sidebar_layout = QVBoxLayout(right_sidebar)
        right_sidebar_layout.setContentsMargins(20, 20, 20, 20)
        
        side_title = QLabel("📜 History")
        side_title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        side_title.setStyleSheet("color: #2d3748;")
        right_sidebar_layout.addWidget(side_title)
        
        side_subtitle = QLabel("Last 5 Uploads")
        side_subtitle.setStyleSheet("color: #718096; font-size: 12px; margin-bottom: 10px;")
        right_sidebar_layout.addWidget(side_subtitle)

        self.history_list = QListWidget()
        self.history_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.history_list.setStyleSheet("""
            QListWidget {border: none; background: transparent;}
            QListWidget::item {border-bottom: 1px solid #e2e8f0;padding: 10px 5px;}
            QListWidget::item:hover {background-color: #f0fdf4;}
            QListWidget::item:selected {background-color: #d1fae5;}
        """)
        self.history_list.itemClicked.connect(self.handle_history_click)
        right_sidebar_layout.addWidget(self.history_list)

        # Adding everything up
        layout_container.addWidget(left_sidebar)
        layout_container.addLayout(main_content, stretch=1)   
        layout_container.addWidget(right_sidebar)
        content_layout.addLayout(layout_container)
        main_dash_layout.addWidget(content_container)

    def browse_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', "CSV Files (*.csv)")
        if fname:
            self.filename_label.setText(os.path.basename(fname))
            self.filename_label.setStyleSheet("color: #2d3748; font-size: 14px; font-weight: bold;")
            self.analyse_file.setDisabled(False)
            self.selected_file = fname
        else:
            self.filename_label.setText("No file selected.")
            self.selected_file = None
            self.filename_label.setText("No file selected.")
            self.filename_label.setStyleSheet("color: #718096; font-size: 14px;")
            self.analyse_file.setEnabled(False)

    def load_history(self):
        try:
            headers = {'Authorization': f'Bearer {self.token}'}
            response = requests.get(f"{BASE_URL}/equipment/", headers=headers)
            if response.status_code == 200:
                self.history_list.clear()
                for item in response.json()[:5]:
                    list_item = QListWidgetItem(f"📄 {item['filename']}\n{item['upload_date'][:10]}")
                    list_item.setData(Qt.UserRole, item['id'])
                    self.history_list.addItem(list_item)
        except Exception as e:
            print(f"History load failed: {e}")

    def handle_history_click(self, item):
        file_id = item.data(Qt.UserRole)
        menu = QMenu(self)
        view_csv_action = QAction("📊 View CSV", self)
        download_pdf_action = QAction("📑 Download PDF", self)
        
        view_csv_action.triggered.connect(lambda: self.view_csv(file_id))
        download_pdf_action.triggered.connect(lambda: self.download_pdf(file_id))
        
        menu.addAction(view_csv_action)
        menu.addAction(download_pdf_action)
        menu.exec_(QCursor.pos())
    def create_stat_cards(self, label, value, is_clickable=False):
        card = QFrame()
        card.setFixedSize(140, 100)
        card.setStyleSheet("background-color: #edf2f7; border-radius: 12px; border: 1px solid #86efac;")
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)

        if is_clickable:
            star = QLabel("★", card)
            star.setStyleSheet("background: #2d5a27; color: #f6e05e; border-radius: 4px; padding: 2px;")
            star.setFixedSize(22, 18)
            star.move(110, 8) 
            card.setCursor(Qt.PointingHandCursor)
            card.installEventFilter(self)

        value_label = QLabel(value)
        value_label.setObjectName(f"val_{label}")
        value_label.setFont(QFont('Segoe UI', 15, QFont.Bold))
        value_label.setStyleSheet("color: #065f46;")
        value_label.setProperty("original_value", value) 

        text_label = QLabel(label)
        text_label.setFont(QFont('Segoe UI', 9))
        text_label.setStyleSheet("color: #047857;")

        layout.addWidget(value_label, alignment=Qt.AlignCenter)
        layout.addWidget(text_label, alignment=Qt.AlignCenter)
        return card

    def upload_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "No File", "Please select a CSV file first.")
            return
        
        file_size_mb = os.path.getsize(self.selected_file) / (1024 * 1024)
        MAX_SIZE_MB = 10
        if file_size_mb > MAX_SIZE_MB:
            QMessageBox.warning(self, "File Too Large", 
                              f"The selected file is {file_size_mb:.2f} MB.\n"
                              f"Please upload a file smaller than {MAX_SIZE_MB} MB.")
            return
        
        self.analyse_file.setText("⏳ Processing...")
        self.analyse_file.setDisabled(True)
        QApplication.processEvents()
        try:
            with open(self.selected_file, 'rb') as f:
                headers = {'Authorization': f'Bearer {self.token}'}
                response = requests.post(f"{BASE_URL}/equipment/", files={'file': f}, headers=headers)
                
            if response.status_code in [200, 201]:
                data = response.json()
                self.stats_frame.setVisible(True)
                total_lbl = self.total_label.findChild(QLabel, "val_Total")
                if total_lbl:
                    total_lbl.setText(str(data['total_count']))
                    print(f"DEBUG: Updated total to {data['total_count']}")
                else:
                    print("DEBUG: Could not find val_Total label")
                
                flow_lbl = self.flow_label.findChild(QLabel, "val_Avg_Flowrate")
                if flow_lbl:
                    flow_lbl.setText(f"{data['averages']['flowrate']:.2f}")
                
                press_lbl = self.press_label.findChild(QLabel, "val_Avg_Pressure")
                if press_lbl:
                    press_lbl.setText(f"{data['averages']['pressure']:.2f}")
                
                temp_lbl = self.temp_label.findChild(QLabel, "val_Avg_Temperature")
                if temp_lbl:
                    temp_lbl.setText(f"{data['averages']['temperature']:.2f}")
                
                #Hover effect to view distributions
                if 'type_distribution' in data:
                    breakdown_text = "Equipment Breakdown:\n"
                    for eq_type, count in data['type_distribution'].items():
                        breakdown_text += f"• {eq_type}: {count}\n"
                    # store distribution for pie dialog and tooltips
                    self.current_distribution_data = data['type_distribution']
                    self.total_label.setToolTip(breakdown_text)
                    lbl = self.total_label.findChild(QLabel, "val_Total")
                    if lbl is not None:
                        lbl.setToolTip(breakdown_text)

                # Update Chart
                self.plot_chart(data['type_distribution'])   

                # Update Table 
                if 'equipment_data' in data:
                    equipment_data = data['equipment_data'][:10]
                    self.data_table.setRowCount(len(equipment_data))                
                    for row_idx, row_data in enumerate(equipment_data):
                        self.data_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data.get('type', ''))))
                        self.data_table.setItem(row_idx, 1, QTableWidgetItem(str(row_data.get('flowrate', ''))))
                        self.data_table.setItem(row_idx, 2, QTableWidgetItem(str(row_data.get('pressure', ''))))
                        self.data_table.setItem(row_idx, 3, QTableWidgetItem(str(row_data.get('temperature', ''))))

                self.analyse_file.setText("☁ Analyze CSV File")
                self.load_history()
            else:
                self.analyse_file.setText("❌ Upload Failed")
                self.analyse_file.setEnabled(True)
                QMessageBox.warning(self, "Error", "Failed to process file")
        except Exception as e:
            self.analyse_file.setText("❌ Error")
            self.analyse_file.setEnabled(True)
            QMessageBox.critical(self, "Error", f"Upload failed: {str(e)}")

    def download_pdf(self, report_id):
        try:
            # For the ease of demonstration and file save, saving the report file in the code folder itself
            # namely in the reports folder inside desktop_frontend folder.
            report_dir = os.path.join(os.path.dirname(__file__), "reports")
            if not os.path.exists(report_dir):
                os.makedirs(report_dir)
                
            headers = {'Authorization': f'Bearer {self.token}'}
            response = requests.get(f"{BASE_URL}/report/{report_id}/", headers=headers)
            
            if response.status_code == 200:
                filename = f"report_{report_id}.pdf"
                full_path = os.path.join(report_dir, filename)
                with open(full_path, 'wb') as f:
                    f.write(response.content)
                webbrowser.open(os.path.abspath(full_path))
            else:
                QMessageBox.warning(self, "Error", "Could not fetch report from server.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Download failed: {str(e)}")

    def view_csv(self, csv_id):
        try:
            print(f"DEBUG: Fetching CSV file with id={csv_id}")
            response = download_csv_request(csv_id, self.token)
            
            if response.status_code == 200:
                csv_content = response.text
                lines = csv_content.strip().split('\n')
                if not lines:
                    QMessageBox.warning(self, "Error", "CSV file is empty")
                    return
                
                dialog = QDialog(self)
                dialog.setWindowTitle(f"CSV Preview - File {csv_id}")
                dialog.setGeometry(100, 100, 800, 600)
                layout = QVBoxLayout(dialog)
                
                table = QTableWidget()
                header = lines[0].split(',')
                table.setColumnCount(len(header))
                table.setHorizontalHeaderLabels(header)
                
                for i, line in enumerate(lines[1:], 1):
                    table.insertRow(i - 1)
                    values = line.split(',')
                    for j, value in enumerate(values):
                        table.setItem(i - 1, j, QTableWidgetItem(value.strip()))
                
                table.setStyleSheet("""
                    QTableWidget {border: 1px solid #e2e8f0; border-radius: 6px; background-color: white;}
                    QHeaderView::section {background-color: #f7fafc; padding: 8px; font-weight: bold; color: #2d3748;}
                    QTableWidget::item {padding: 8px;}
                """)
                
                header = table.horizontalHeader()
                for i in range(len(header)):
                    header.setSectionResizeMode(i, QHeaderView.Stretch)
                layout.addWidget(table)
                
                close_button = QPushButton("Close")
                close_button.clicked.connect(dialog.close)
                layout.addWidget(close_button)
                dialog.exec_()
            else:
                QMessageBox.warning(self, "Error", "Could not fetch CSV file from server.")
        except Exception as e:
            print(f"DEBUG: CSV view error: {e}")
            QMessageBox.critical(self, "Error", f"Failed to view CSV: {str(e)}")

    def plot_chart(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(list(data.keys()), list(data.values()), color='#48bb78', edgecolor='#2d5a27', linewidth=1.5)
        ax.set_title("Equipment Distribution", fontsize=14, fontweight='bold', color = '#2d3748')
        ax.set_xlabel("Equipment Type", fontsize=12, color = '#4a5568')
        ax.set_ylabel("Count", fontsize=12, color = '#4a5568')
        ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()
        ax.grid(axis='y', linestyle='--', alpha=0.3, color = '#cbd5e0')
        self.canvas.draw()

    def show_distribution_pie(self):
        if not hasattr(self, 'current_distribution_data'):
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("Equipment Breakdown")
        dialog.setFixedSize(500, 500)
        layout = QVBoxLayout(dialog)

        fig = Figure(figsize=(5, 5), dpi=100)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        data = self.current_distribution_data
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', 
            colors=['#48bb78', '#38a169', '#2d5a27', '#1a3a16', '#a8e063'])
        
        layout.addWidget(canvas)
        dialog.exec_()
        
    def toggle_view(self, show_pie=True):
        if show_pie:
            self.stacked_widget.setCurrentIndex(1) 
        else:
            self.stacked_widget.setCurrentIndex(0) 

    def eventFilter(self, obj, event):
        # Guard against accessing total_label before it's created
        if not hasattr(self, 'total_label'):
            return super().eventFilter(obj, event)
        
        if obj == self.total_label:
            label = obj.findChild(QLabel, "val_Total")
            if label is None:
                return super().eventFilter(obj, event)
            if event.type() == event.Enter:
                label.setText("View Details")
                label.setStyleSheet("color: #2d5a27; font-size: 10pt;")
            elif event.type() == event.Leave:
                label.setText(label.property("original_value"))
                label.setStyleSheet("color: #065f46; font-size: 12pt;")
        return super().eventFilter(obj, event)

    def show_pie_fullscreen(self):
        self.chart_stack.setCurrentIndex(1) 

    def show_summary_main(self):
        self.chart_stack.setCurrentIndex(0) 

    def back_to_login(self):
        from authentication import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()
