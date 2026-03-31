#Removed everything for PyQt6
#importing
import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget 
from PyQt6.QtCore import Qt 

class MeditationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        #Setting up the main window 
        self.setWindowTitle("Meditation Audio Engine")
        self.setGeometry(100, 100, 800, 600) #x, y, width, height

        #CSS for the background of suitable vibe
        self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")

        #Creating a basic layout
        layout = QVBoxLayout()

        #Add a test title
        title = QLabel("Welcome to the UI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight:bold; margin-top: 20px;")
        layout.addWidget(title)

        #setting layout at the center of the window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MeditationApp()
    window.show()

    #To keep app running until click X to close it 
    sys.exit(app.exec())                            