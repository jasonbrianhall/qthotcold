import sys
import random
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from math import sqrt

# Global variables
WIDTH, HEIGHT = 1024, 768  # Screen dimensions
hotTolerance=20
foundTolerance=4
pixel = None              # Position of the hidden pixel
        
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.prevdistance=9999999999
        self.prevresponse="Unknown!  "

    # Calculate the distance between the mouse and the hidden pixel
    def get_distance(self):
        cursor_pos = QCursor.pos()
        x2=int(cursor_pos.x())
        y2=int(cursor_pos.y())
        distance = int(sqrt((x2 - self.x1)**2 + (y2 - self.y1)**2))
        return distance

    # Initialize the pixel position
    def init_pixel(self):
        # Get the current window geometry
        rect = self.geometry()
        # Get the window frame geometry, which includes the title bar
        frame_rect = self.frameGeometry()
        # Calculate the height of the title bar
        title_bar_height = frame_rect.height() - rect.height()
        # Generate a random position inside the window, including the title bar
        self.x1 = random.randint(rect.left(), rect.right())
        self.y1 = random.randint(rect.top() + title_bar_height, rect.bottom())
        pixel = QPoint(self.x1, self.y1)

    # Update the feedback label with a "hotter/colder" message
    def update_feedback(self, pos, label):
        distance = self.get_distance()
        cursor_pos = QCursor.pos()
        x2=int(cursor_pos.x())
        y2=int(cursor_pos.y())
        
        cheat=" Distance: " + str(distance) + " X1: " + str(self.x1) + " Y1: " + str(self.y1) + " X2: " + str(x2) + " Y2: " + str(y2)

        if distance <= foundTolerance and distance<=self.prevdistance:
            label.setText("Found it!  " + cheat)
            self.prevresponse="Found it!  "
        elif distance <= hotTolerance and distance<=self.prevdistance:
            label.setText("On Fire!  " + cheat)
            self.prevresponse="On Fire!  "
    
        elif distance < self.prevdistance:
            label.setText("Hotter!  " + cheat)
            self.prevresponse="Hotter!  "
        elif distance==self.prevdistance:
            label.setText(self.prevresponse + cheat)
        else:
            label.setText("Colder!  " + cheat)
            self.prevresponse="Colder!  "
        self.prevdistance=distance


    def initUI(self):
        # Initialize the pixel position
        self.init_pixel()

        # Hide the mouse cursor
        #self.setCursor(Qt.BlankCursor)

        # Set up the window
        self.setWindowTitle("Hotter/Colder")
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setWindowIcon(QIcon('icon.png'))

        # Set up the feedback label
        label = QLabel(self)
        label.setGeometry(10, 10, 400, 50)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("QLabel { color: red; }")

        # Set up the timer to update the feedback label
        self.timer = self.startTimer(10)

        self.show()

    # Handle the timer event
    def timerEvent(self, event):
        # Get the mouse position
        pos = QCursor.pos()

        # Update the feedback label
        self.update_feedback(pos, self.findChild(QLabel))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())

