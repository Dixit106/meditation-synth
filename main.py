#Removed everything for PyQt6
#importing
import sys
import random 
import math  
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton 
from PyQt6.QtCore import Qt, QTimer 
from PyQt6.QtGui import QPainter, QPen, QColor  

#Bringing my custom math engine
from audio_engine import Tone 

# -- The Math Visualizer --
class Visualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(120) #This will be height of the animation box
        self.mode = "idle"
        self.wave_color = QColor("#FFFFFF")
        self.phase = 0.0

        # Runs the animation at 60 FPS ( :) )
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    def animate(self):
        self.phase += 0.15 #Will be the speed of the wave movement
        self.update() # Something about triggering the paintEvent to redraw

    def set_mode(self, mode, color_hex):
        self.mode = mode
        self.wave_color = QColor(color_hex)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        mid_y = h / 2

        #Seetingup the glowing pen
        pen = QPen(self.wave_color)
        pen.setWidth(3)
        painter.setPen(pen)

        old_x, old_y = 0, mid_y 
        old_y2 = mid_y # For the binaural second wave

        for x in range(0, w, 4): #Calculate a point every 4 pixels for somethign(animation)

            if self.mode == "sine":
                # Smooth math wave
                y = mid_y + math.sin(x * 0.05 + self.phase) * 40
                painter.drawLine(old_x, int(old_y), x, int(y))
                old_y = y 

            elif self.mode == "noise":
                # Chaotic random spikes
                y = mid_y + random.uniform(-40, 40)
                painter.drawLine(old_x, int(old_y), x, int(y))
                old_y = y 

            elif self.mode == "binaural":
                # Two overlapping, slightly different waves as its binaural
                y1 = mid_y + math.sin(x * 0.04 + self.phase) * 30
                y2 = mid_y + math.sin(x * 0.05 + self.phase) * 30

                painter.drawLine(old_x, int(old_y), x, int(y1))

                # To Draw second wave slightly dimmer
                pen.setAlpha(100)
                painter.setPen(pen)
                painter.drawLine(old_x, int(old_y2), x, int(y2))

                pen.setAlpha(225) # Will Reset the brightness
                painter.setPen(pen)

                old_y = y1 
                old_y2 = y2 

            else:
                # Flatline when idle
                painter.drawLine(old_x, int(mid_y), x, int(mid_y))

            old_x = x                 

class MeditationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        #Setting up the main window 
        self.setWindowTitle("Meditation Audio Engine")
        self.setGeometry(100, 100, 800, 600) #x, y, width, height

        #CSS for the background of suitable vibe
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")

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

        # Creating our new visualizer!
        self.vis = Visualizer()

        #Column 1: Solfeggio
        col1 = QVBoxLayout()
        col1_title = QLabel("Solfeggio Frequencies")
        col1_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col1_title.setStyleSheet("font-size: 18px; color: #88CCFF;") # Light Blue
        col1.addWidget(col1_title)

        #Wiring th buttons for column1
        btn_432 = self.create_btn("432Hz (Calming)", "#88CCFF")
        btn_432.clicked.connect(lambda: Tone.sine(432))
        col1.addWidget(btn_432)

        btn_528 = self.create_btn("528Hz (Repair)", "#88CCFF")
        btn_528.clicked.connect(lambda: Tone.sine(528))
        col1.addWidget(btn_528)

        btn_639 = self.create_btn("639Hz (Connection)", "#88CCFF")
        btn_639.clicked.connect(lambda: Tone.sine(639))
        col1.addWidget(btn_639)
        col1.addStretch()

        #Column 2: Noise
        col2 = QVBoxLayout()
        col2_title = QLabel("Atmospheric Noise")
        col2_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col2_title.setStyleSheet("font-size: 18px; color: #AADD88;") #Light green
        col2.addWidget(col2_title)

        btn_white = self.create_btn("White (Static)", "#AADD88")
        btn_white.clicked.connect(lambda: Tone.white_noise())
        col2.addWidget(btn_white)

        btn_pink = self.create_btn("Pink (Rainfall)", "#AADD88")
        btn_pink.clicked.connect(lambda: Tone.pink_noise())
        col2.addWidget(btn_pink)

        btn_brown = self.create_btn("Brown (Waterfall)", "#AADD88")
        btn_brown.clicked.connect(lambda: Tone.brown_noise())
        col2.addWidget(btn_brown)
        col2.addStretch()

        #Column 3: Brainwaves
        col3 = QVBoxLayout()
        col3_title = QLabel("Binaural Beats")
        col3_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col3_title.setStyleSheet("font-size: 18px; color: #DDAA88;") #Light organge
        col3.addWidget(col3_title)

        btn_alpha = self.create_btn("Alpha (Focus)", "#DDAA88")
        btn_alpha.clicked.connect(lambda: Tone.binaural_beat(200, 10))
        col3.addWidget(btn_alpha)

        btn_theta = self.create_btn("Theta (Deep)", "#DDAA88")
        btn_theta.clicked.connect(lambda: Tone.binaural_beat(200, 5))
        col3.addWidget(btn_theta)

        btn_delta = self.create_btn("Delta (Sleep)", "#DDAA88")
        btn_delta.clicked.connect(lambda: Tone.binaural_beat(200, 2.5))
        col3.addWidget(btn_delta)
        col3.addStretch()

        #Adding the 3 vertical columns into horizontal layout
        columns_layout.addLayout(col1)
        columns_layout.addLayout(col2)
        columns_layout.addLayout(col3)

        #Adding the columns to the main layout
        main_layout.addLayout(columns_layout)

        # Adding Visualizer Here too
        main_layout.addWidget(self.vis)

        # --- BIG STOP BUTTON ---
        main_layout.addSpacing(20)
        stop_btn = QPushButton("STOP AUDIO")
        stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4444; color: white; font-size: 18px;
                font-weight: bold; border-radius: 8px; padding: 15px;                                  
            }                       
            QPushButton:hover { background-color: #FF2222; }   
        """)
        stop_btn.clicked.connect(lambda: Tone.stop())
        main_layout.addWidget(stop_btn)

        #setting layout at the center of the window
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    #helper fxn to trigger both Audio and Visuals at the same time
        

    #helper fxn to make buttons look good
    def create_btn(self, text, color):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #2A2A2A; color: {color}; border: 1px solid {color};
                border-radius: 6px; padding: 10px; font-size: 14px; font-weight: bold;            
            }}              
            QPushButton:hover {{ background-color: {color}; color:#121212; }}              
        """) 
        return btn
       

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #SILENCING MY ARCH LINUX WARNING!
    app.setStyle("Fusion")   

    window = MeditationApp()
    window.show()

    #To keep app running until click X to close it 
    sys.exit(app.exec())                            