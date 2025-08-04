from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import sys

class CurrtncyConvecter(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвектатор валют")
        self.setFixedSize(500, 500)
        self.setStyleSheet("background-color: #333333")

        self.exchange_rates = {
            'USD' : 1,
            'UAH' : 41,
            'EUR' : 0.92,
            'GBR' : 0.81,
            'JPY' : 136.58,
            'CAD' : 1.35,
            'AUD' : 1.47,
            'CHF' : 0.92,
            'CNY' : 7.05,

        }

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Конвектатор валют")
        title.setFont(QFont("Helvetica", 16, QFont.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        amount_label = QLabel("Кількість:")
        amount_label.setFont(QFont("Helvetica", 12))
        amount_label.setStyleSheet("color: white;")
        layout.addWidget(amount_label)

        self.amount_input = QLineEdit()
        self.amount_input.setFont(QFont('Helvetica', 14))
        self.amount_input.setStyleSheet("background-color: #f1f1f1; padding: 5px;")
        layout.addWidget(self.amount_input)

        self.from_currency = QComboBox()
        self.from_currency.addItems(self.exchange_rates.keys())
        self.from_currency.setCurrentText('USD')
        self.from_currency.setFont(QFont('Helvetica', 12))
        self.from_currency.setStyleSheet("background-color: #f1f1f1; color: #333333;")
        layout.addWidget(self.from_currency)

        self.to_currency = QComboBox()
        self.to_currency.addItems(self.exchange_rates.keys())
        self.to_currency.setCurrentText('UAH')
        self.to_currency.setFont(QFont('Helvetica', 12))
        self.to_currency.setStyleSheet("background-color: #f1f1f1; color: #333333;")
        layout.addWidget(self.to_currency)

        self.button = QPushButton("Конвертувати")
        self.button.setFont(QFont('Helvetica', 14, QFont.Bold))
        self.button.setStyleSheet("""
                QPushButton{
                        background-color: #4caf50;
                        color: white;
                        border: none;
                        padding: 10px;
                                  
                                  }

                                  QPushButton:hover{
                                    background-color: #45a049;
                                  
                                  }
                                  """)
        self.button.clicked.connect(self.convert_currency)
        layout.addWidget(self.button)

        self.result = QLabel("")
        self.result.setFont(QFont('Helvetica', 14))
        self.result.setStyleSheet("color:white;")
        layout.addWidget(self.result)
                
        self.setLayout(layout)

    def convert_currency(self):
        try:
            amount = float(self.amount_input.text())
            from_curr = self.from_currency.currentText()
            to_carr = self.to_currency.currentText()



            from_rate = self.exchange_rates[from_curr]
            to_rate = self.exchange_rates[to_carr]

            result_curr = (amount / from_rate) * to_rate
            self.result.setText(f"{amount} {from_curr} = {result_curr:.2f} {to_carr}")


        except ValueError:
            self.result.setText("Помилка вводу")

            






app = QApplication(sys.argv)
Window = CurrtncyConvecter() 
Window.show()
sys.exit(app.exec_())