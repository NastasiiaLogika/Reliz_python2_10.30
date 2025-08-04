from PyQt5.QtWidgets import*
import requests
import sys

class CurrencyConvertator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("конвертатор")
        self.setGeometry(100, 100, 600, 600)

        self.amount_label = QLabel("Сума:", self)
        self.amount_input = QLineEdit(self)
        self.from_currency_label = QLabel("З валюти:", self)
        self.from_currency = QComboBox(self)
        self.from_currency.addItems(["USD", "EUR", "UAH", "JPY", "GBP", "CNY", "BRL", "KZT"])

        self.to_currency_label = QLabel("У валюту:", self)
        self.to_currency = QComboBox(self)
        self.to_currency.addItems(["USD", "EUR", "UAH", "JPY", "GBP", "CNY", "BRL", "KZT"])

        self.convert_button = QPushButton("конвертувати", self)
        self.convert_button.clicked.connect(self.convert_currency)

        self.result = QLabel("", self)

        layout = QVBoxLayout()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.from_currency_label)
        layout.addWidget(self.from_currency)
        layout.addWidget(self.to_currency_label)
        layout.addWidget(self.to_currency)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.result)

        self.setLayout(layout)


    def get_exchange_rate(self, from_currency, to_currency):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url)
            data = response.json()
            return data["rates"].get(to_currency, None)
        except Exception as e:
            return None
        

    def convert_currency(self):
        try:
            amount = float(self.amount_input.text())
            from_currency = self.from_currency.currentText()
            to_currency = self.to_currency.currentText()

            if from_currency == to_currency:
                self.result.setText("Виберіть різні валюти!")
                return
            
            rate = self.get_exchange_rate(from_currency, to_currency)
            if rate is None:
                self.result.setText("Помилка отримання даних!")

            convert_amount = round(amount*rate, 2)
            self.result.setText(f"{amount} {from_currency} = {convert_amount} {to_currency}")

        except ValueError:
            self.result.setText("Некоректно введенні дані!")

app = QApplication(sys.argv)

with open('style', 'r') as style_file:
    style = style_file.read()
    app.setStyleSheet(style)

window = CurrencyConvertator()
window.show()
app.exec_()