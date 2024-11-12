import os
import shutil
import json
import logging
from PyQt5 import QtWidgets, QtGui, QtCore


# Function to check and generate a default config file if needed
def load_or_generate_config(config_path='config.json'):
    default_config = {
        "base_dir": "~/Downloads",
        "file_types": {
            "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".doc"],
            "Videos": [".mp4", ".mkv", ".mov", ".avi"],
            "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "Music": [".mp3", ".wav", ".flac", ".aac"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Programs": [".exe", ".msi", ".sh", ".bat"],
            "MayaProjects": [".ma", ".mb", ".obj", ".fbx"]
        },
        "target_dirs": {
            "Documents": "~/Documents",
            "Videos": "~/Videos",
            "Pictures": "~/Pictures",
            "Music": "~/Music",
            "Archives": "~/Downloads/Archives",
            "Programs": "~/Downloads/Programs",
            "MayaProjects": "~/Documents/Maya"
        }
    }

    if not os.path.exists(config_path):
        with open(config_path, 'w') as config_file:
            json.dump(default_config, config_file, indent=4)
            print("Default config.json file created.")
    else:
        print("Loading existing config.json file.")

    with open(config_path, 'r') as config_file:
        return json.load(config_file)


# Load configuration
config_data = load_or_generate_config()

# Configure logging
logging.basicConfig(filename='file_organizer.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# Function to organize files into folders
def organize_files(directory, config, progress_callback):
    script_name = os.path.basename(__file__)
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f != script_name]

    for i, filename in enumerate(files):
        progress_callback.emit(int((i + 1) / len(files) * 100))
        file_path = os.path.join(directory, filename)
        moved = False

        for folder, extensions in config['file_types'].items():
            if filename.lower().endswith(tuple(extensions)):
                target_folder = os.path.expanduser(config['target_dirs'].get(folder, directory))
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                new_path = os.path.join(target_folder, filename)
                if not os.path.exists(new_path):
                    shutil.move(file_path, new_path)
                    logging.info(f"Moved {filename} to {target_folder}")
                else:
                    base, ext = os.path.splitext(filename)
                    new_filename = f"{base}_copy{ext}"
                    new_path = os.path.join(target_folder, new_filename)
                    shutil.move(file_path, new_path)
                    logging.info(f"Renamed and moved {filename} to {new_path} due to conflict")

                moved = True
                break

        if not moved:
            logging.info(f"Skipped {filename}: no matching extension")


# PyQt GUI Class
class FileOrganizerApp(QtWidgets.QWidget):
    progress_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.progress_bar = None
        self.btn_start = None
        self.btn_browse = None
        self.label = None
        self.dir_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Advanced File Organizer')
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #1b1b2f;  /* Dark background */
            }
            QLabel, QLineEdit {
                font-size: 14px;
                color: #e0e0e0;  /* Light gray text */
                background-color: #1b1b2f;
            }
            QLineEdit {
                border: 2px solid #4caf50;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #2f2f4f;  /* Dark button background */
                color: #f72585;  /* Neon pink text */
                border: 2px solid #f72585;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7209b7;  /* Purple hover effect */
                border: 2px solid #3a0ca3;  /* Dark purple border */
            }
            QProgressBar {
                background-color: #2f2f4f;
                border: 2px solid #4caf50;
                border-radius: 5px;
                color: #e0e0e0;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4895ef;  /* Bright electric blue progress */
            }
        """)

        # Layout and widgets
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel('Select the directory to organize:')
        self.dir_path = QtWidgets.QLineEdit()
        self.btn_browse = QtWidgets.QPushButton('Browse')
        self.btn_start = QtWidgets.QPushButton('Start Organizing')
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)

        # Adding widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.dir_path)
        layout.addWidget(self.btn_browse)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        # Button events
        self.btn_browse.clicked.connect(self.browse_folder)
        self.btn_start.clicked.connect(self.start_organizing)
        self.progress_signal.connect(self.update_progress)

    def browse_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        if folder:
            self.dir_path.setText(folder)

    def start_organizing(self):
        directory = self.dir_path.text()
        if directory and os.path.exists(directory):
            self.progress_bar.setValue(0)
            QtWidgets.QApplication.processEvents()
            self.run_organize_task(directory)
            QtWidgets.QMessageBox.information(self, 'Complete', 'File organization completed!')
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please select a valid directory.')

    def run_organize_task(self, directory):
        self.progress_signal.emit(0)
        organize_files(directory, config_data, self.progress_signal)

    def update_progress(self, value):
        self.progress_bar.setValue(value)


# Run the app
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = FileOrganizerApp()
    window.setWindowIcon(QtGui.QIcon('icon.png'))  # Add an icon for the window if desired
    window.show()
    sys.exit(app.exec_())
