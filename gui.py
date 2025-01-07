from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel


class InputPopup(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("What deals are you looking for today?")
        self.setMinimumSize(300, 150)

        # Layout
        layout = QVBoxLayout()

        # Input field
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Meats, Razors, etc.")
        layout.addWidget(QLabel("List the items you're looking for deals on:"))
        layout.addWidget(self.input_field)

        # Buttons
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)  # Accept the dialog
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)  # Reject the dialog

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def get_input(self):
        """Returns the input text when dialog is accepted."""
        return self.input_field.text()