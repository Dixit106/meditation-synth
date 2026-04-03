#Removed everything for PyQt6
#importing
import sys
import random 
import math  
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSpinBox  
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
                dim_color = QColor(self.wave_color)
                dim_color.setAlpha(100)
                pen.setColor(dim_color)
                painter.setPen(pen)
                painter.drawLine(old_x, int(old_y2), x, int(y2))

                pen.setColor(self.wave_color) # Will Reset the brightness
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

        #List to keep track of all buttons
        self.all_buttons = []

        #Set up the invisible countdown timer
        self.time_left = 0
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_timer)

        #to track intro is active
        self.intro_active = True 

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
        btn_432.clicked.connect(lambda checked=False, b=btn_432: self.play_sound("sine", 432, "#88CCFF", b))
        col1.addWidget(btn_432)

        btn_528 = self.create_btn("528Hz (Repair)", "#88CCFF")
        btn_528.clicked.connect(lambda checked=False, b=btn_528: self.play_sound("sine", 528, "#88CCFF", b))
        col1.addWidget(btn_528)

        btn_639 = self.create_btn("639Hz (Connection)", "#88CCFF")
        btn_639.clicked.connect(lambda checked=False, b=btn_639: self.play_sound("sine", 639, "#88CCFF", b))
        col1.addWidget(btn_639)
        col1.addStretch()

        #Column 2: Noise
        col2 = QVBoxLayout()
        col2_title = QLabel("Atmospheric Noise")
        col2_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col2_title.setStyleSheet("font-size: 18px; color: #AADD88;") #Light green
        col2.addWidget(col2_title)

        btn_white = self.create_btn("White (Static)", "#AADD88")
        btn_white.clicked.connect(lambda checked=False, b=btn_white: self.play_sound("white", 0, "#AADD88", b))
        col2.addWidget(btn_white)

        btn_pink = self.create_btn("Pink (Rainfall)", "#AADD88")
        btn_pink.clicked.connect(lambda checked=False, b=btn_pink: self.play_sound("pink", 0, "#AADD88", b))
        col2.addWidget(btn_pink)

        btn_brown = self.create_btn("Brown (Waterfall)", "#AADD88")
        btn_brown.clicked.connect(lambda checked=False, b=btn_brown: self.play_sound("brown", 0, "#AADD88", b))
        col2.addWidget(btn_brown)
        col2.addStretch()

        #Column 3: Brainwaves
        col3 = QVBoxLayout()
        col3_title = QLabel("Binaural Beats")
        col3_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col3_title.setStyleSheet("font-size: 18px; color: #DDAA88;") #Light organge
        col3.addWidget(col3_title)

        btn_alpha = self.create_btn("Alpha (Focus)", "#DDAA88")
        btn_alpha.clicked.connect(lambda checked=False, b=btn_alpha: self.play_sound("binaural", (200, 10), "#DDAA88", b))
        col3.addWidget(btn_alpha)

        btn_theta = self.create_btn("Theta (Deep)", "#DDAA88")
        btn_theta.clicked.connect(lambda checked=False, b=btn_theta: self.play_sound("binaural", (200, 5), "#DDAA88", b))
        col3.addWidget(btn_theta)

        btn_delta = self.create_btn("Delta (Sleep)", "#DDAA88")
        btn_delta.clicked.connect(lambda checked=False, b=btn_delta: self.play_sound("binaural", (200, 2.5), "#DDAA88", b))
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

        # --- NEW TIMER UI SECTION ---
        timer_layout = QHBoxLayout()

        self.time_input = QSpinBox()
        self.time_input.setRange(1, 120)# 1 minute to 120min
        self.time_input.setSuffix(" min")
        self.time_input.setStyleSheet("background: #2A2A2A; color: white; padding: 5px; font-size: 16px;")


        start_timer_btn = QPushButton("Start Fade-Out Timer")
        start_timer_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        start_timer_btn.setStyleSheet("background-color: #555555; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        start_timer_btn.clicked.connect(self.start_timer)

        self.time_display = QLabel("00:00")
        self.time_display.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF;")

        timer_layout.addWidget(QLabel("Meditation Duration:"))
        timer_layout.addWidget(self.time_input)
        timer_layout.addWidget(start_timer_btn)
        timer_layout.addWidget(self.time_display)

        main_layout.addLayout(timer_layout)

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
        stop_btn.clicked.connect(self.stop_audio)
        main_layout.addWidget(stop_btn)

        #setting layout at the center of the window
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        #Floating skip label
        self.skip_label = QLabel("", self)
        #Positining in botton right corner(x,y, width, height)
        self.skip_label.setGeometry(600, 620, 180, 20)
        self.skip_label.setStyleSheet("color: #888888; font-size:12px; font-style: italic; background: transparent;")
        self.skip_label.hide() #Hidden by default

        #Start the intro audio
        Tone.intro_sequence()

        #6 sec timer to show the skip label
        self.voice_timer = QTimer()
        self.voice_timer.setSingleShot(True) # runs once
        self.voice_timer.timeout.connect(Tone.play_voice)
        self.voice_timer.start(3000) #3sec wait

        #Timer 2 skip message after 6 sec
        self.skip_timer = QTimer()
        self.skip_timer.setSingleShot(True)
        self.skip_timer.timeout.connect(self.show_skip_message)
        self.skip_timer.start(6000)

        #Timer 4: to turn off intro mode after 10 seconds
        self.end_intro_timer = QTimer()
        self.end_intro_timer.setSingleShot(True)
        self.end_intro_timer.timeout.connect(self.end_intro_state)
        self.end_intro_timer.start(10000)

        

        #Show skip label function
    def show_skip_message(self):
        if self.intro_active:
            self.skip_label.setText("Press ENTER to skip intro")
            self.skip_label.show()
            Tone.play_click()#to play gta sound

    def end_intro_state(self):
        self.intro_active = False 
        self.skip_label.setText("")
        self.skip_label.hide()        

        #Enter key to skip
    def keyPressEvent(self, event):
            #check if enter pressed
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self.intro_active:
                self.intro_active = False 
                self.skip_label.setText("")
                self.skip_label.hide()

                #To stop pending timers so they don't fire late
                self.voice_timer.stop()
                self.skip_timer.stop()
                self.end_intro_timer.stop()         

                #To play the intro
                Tone.skip_intro()

    #helper fxn to trigger both Audio and Visuals at the same time
    def play_sound(self, wave_type, freq, color, clicked_btn=None):

        #if user clicks we skip
        if self.intro_active:
            self.intro_active = False 
            self.skip_label.setText("")
            self.voice_timer.stop()
            self.skip_timer.stop()
            self.end_intro_timer.stop()
            Tone.skip_intro()

        #Reset all buttons to  default dark grey
        for btn in self.all_buttons:
            btn.setStyleSheet(btn.default_style)

        #Making the clicked button brightly colored
        if clicked_btn:
            clicked_btn.setStyleSheet(clicked_btn.active_style)

        #To make sure vol is 100% in case we were fading out previously
        Tone.set_volume(1.0)    

        if wave_type == "sine":
            Tone.sine(freq)
            self.vis.set_mode("sine", color)
        elif wave_type == "white":
            Tone.white_noise()
            self.vis.set_mode("noise", color)
        elif wave_type == "pink":
            Tone.pink_noise()
            self.vis.set_mode("noise", color)
        elif wave_type == "brown":
            Tone.brown_noise()
            self.vis.set_mode("noise", color)
        elif wave_type == "binaural":
            base, beat = freq 
            Tone.binaural_beat(base, beat)
            self.vis.set_mode("binaural", color)

    def stop_audio(self):
        Tone.stop()
        self.vis.set_mode("idle", "#FFFFFF")
        self.countdown_timer.stop()
        self.time_display.setText("00:00")

        for btn in self.all_buttons:
            btn.setStyleSheet(btn.default_style)

    #Timer logic functions
    def start_timer(self):
        # Min to seconds
        self.time_left = self.time_input.value() * 60
        self.update_display()
        self.countdown_timer.start(1000) #To tick every 1000 milisecond which is 1 sec

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_display()

            #if under 10 second, lower volume by 10% per second
            if self.time_left <= 10:
                fade_volume = self.time_left / 10.0
                Tone.set_volume(fade_volume)

        else:
            self.stop_audio() # Time's up then stop completely

    def update_display(self):
        mins = self.time_left // 60
        secs = self.time_left % 60
        self.time_display.setText(f"{mins:02d}:{secs:02d}")

    #helper fxn to make buttons look good
    def create_btn(self, text, color):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        
        btn.default_style = f"background-color: #2A2A2A; color: {color}; border: 1px solid {color}; border-radius: 6px; padding: 10px; font-size: 14px; font-weight: bold;"
        btn.active_style = f"background-color: {color}; color: #121212; border: 1px solid {color};  border-radius: 6px; padding: 10px; font-size: 14px; font-weight: bold;"

        btn.setStyleSheet(btn.default_style)
        self.all_buttons.append(btn)            
        return btn
       

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #SILENCING MY ARCH LINUX WARNING!
    app.setStyle("Fusion")   
    window = MeditationApp()
    window.show()
    #To keep app running until click X to close it 
    sys.exit(app.exec())                            