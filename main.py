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
        