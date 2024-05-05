import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt, QThreadPool, QRunnable
from fpdf import FPDF
import os

class LongRunningTask(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super(LongRunningTask, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 150)
        self.setWindowTitle("Bulk Img to PDF")

        layout = QVBoxLayout()

        self.select_button = QPushButton("Select Image Folder")
        self.select_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_button)

        self.name_label = QLabel("Enter File Name:")
        layout.addWidget(self.name_label)

        self.entry = QLineEdit()
        layout.addWidget(self.entry)

        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate)
        layout.addWidget(self.generate_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        self.image_dir = None
        self.thread_pool = QThreadPool.globalInstance()

    def select_folder(self):
        self.image_dir = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if self.image_dir:
            self.status_label.setText("Image Directory Selected")
            self.status_label.setStyleSheet("color: green")

    def generate(self):
        if self.image_dir:
            self.status_label.setText("Generating...")
            self.status_label.setStyleSheet("color: blue")

            task = LongRunningTask(self.generate_pdf)
            self.thread_pool.start(task)
        else:
            self.status_label.setText("Please select an image folder first!")
            self.status_label.setStyleSheet("color: red")

    def generate_pdf(self):
        pdf_file = f'{self.entry.text()}.pdf'

        # Create an FPDF object
        pdf = FPDF(unit="mm", format="A4")

        # Set the font and font size
        pdf.set_font("Helvetica", size=10)

        # Set the image width and height
        image_width = 60
        image_height = 60

        # Calculate the number of pages needed
        num_pages = -(-415 // (4 * 3))  # Ceiling division

        for page in range(num_pages):
            # Add a new page
            pdf.add_page()

            # Loop through each row
            for row in range(4):
                # Loop through each column
                for col in range(3):
                    # Calculate the image index
                    image_index = page * 12 + row * 3 + col

                    # Check if the image index is within the range
                    if image_index < 415:
                        # Get the image file name
                        image_file = os.listdir(self.image_dir)[image_index]
                        image_path = os.path.join(self.image_dir, image_file)

                        # Add the image to the PDF
                        pdf.image(image_path, x=10 + col * (image_width + 5), y=10 + row * (image_height + 5),
                                  w=image_width, h=image_height)

        # Save the PDF file
        pdf.output(pdf_file, "F")

        self.status_label.setText("Pdf Generated Successfully!")
        self.status_label.setStyleSheet("color: green")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
