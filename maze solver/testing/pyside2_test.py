import sys
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout

class MazeSolver(QDialog):

    def __init__(self, parent=None):
        super(MazeSolver, self).__init__(parent)
        self.setWindowTitle("Maze Solver")

        # Create widgets
        self.edit = QLineEdit("Write my name here..")
        self.button = QPushButton("Show Greetings")
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)
        
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)

    # Greets the user
    def greetings(self):
        print ("Hello {}".format(self.edit.text()))

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    mazeSolver = MazeSolver()
    mazeSolver.show()
    # Run the main Qt loop
    sys.exit(app.exec_())