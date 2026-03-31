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

        #Creating main vertical layout
        main_layout = QVBoxLayout()

        #App Title
        title = QLabel("Meditation-Synth")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight:bold; margin-top: 20px;")
        main_layout.addWidget(title)

        #-- The 3 Columns --
        #QHboxLayout arranges things side by side (horizontally)
        columns_layout = QHBoxLayout()

        #Column 1: Solfeggio
        col1 = QVBoxLayout()
        col1_title = QLabel("Solfeggio Frequencies")
        col1_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col1_title.setStyleSheet("font-size: 18px; color: #88CCFF;") # Light Blue
        col1.addWidget(col1_title)
        col1.addStretch() #Will push title to the top









        #setting layout at the center of the window
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MeditationApp()
    window.show()

    #To keep app running until click X to close it 
    sys.exit(app.exec())                            