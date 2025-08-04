from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import sys
import requests
from datetime import datetime

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Прогноз погоди")
        self.setGeometry(100, 100, 400, 300)
        
        self.central_Widget = QWidget()
        self.setCentralWidget(self.central_Widget)
        self.layout = QVBoxLayout()
        self.central_Widget.setLayout(self.layout)
        
        self.city_label = QLabel('Обери місто', self)
        self.layout.addWidget(self.city_label)
        self.city_combo = QComboBox(self)
        self.city_combo.addItems(["Винники", "Львів",
                                  "Київ", "Лондон", "Дубай", "Варшава"])

        self.layout.addWidget(self.city_combo)
        self.city_combo.currentIndexChanged.connect(self.get_weather)
        
        
        self.button = QPushButton("Отримати погоду",self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.get_weather)

        self.button.setStyleSheet("""
                                         
            QPushButton{
                background-color: #28a745;
                color: #fff;
                padding: 7px 10px;
                border: none;
                border-radius: 3px;
            }  
                                         """)
        
        self.button_update = QPushButton("Оновити",self)
        self.layout.addWidget(self.button_update)
        self.button_update.clicked.connect(self.update_weather)

        self.button_update.setStyleSheet("""
                                         
            QPushButton{
                background-color: #28a745;
                color: #fff;
                padding: 7px 10px;
                border: none;
                border-radius: 3px;
            }
                                         
                                         """)
        
        self.weather_label = QLabel('', self)
        self.layout.addWidget(self.weather_label)
        self.weather_label.setStyleSheet("font-size: 18px;")

        self.icon_label = QLabel(self)
        self.layout.addWidget(self.icon_label)
        
        self.last_update = QLabel('', self)
        self.layout.addWidget(self.last_update)

        self.get_weather()

    def get_weather(self):
        api_key = 'f81703c1f3b81ad93e6644153c4a426e'
        city = self.city_combo.currentText()
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['weather'][0]['icon']
            icon_name = data['weather'][0]['icon']
            icon_urn = f'http://openweathermap.org/img/w/{icon_name}.png'

            weather_text = f'Погода:{weather}\n Температура: {temperature}C\n Вологість: {humidity}%\n Швидкість вітку: {wind_speed}м/c'
            self.weather_label.setText(weather_text)

            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(icon_urn).content)
            self.icon_label.setPixmap(pixmap)

            now = datetime.now()
            formatted_date = now.strftime("%d.%m.%Y %H.%M.%S")
            self.last_update.setText(f"Останнє оновлення: {formatted_date}")

        else:
            self.weather_label.setText("Ьшсто не знайдено!")

    def update_weather(self):
        self.get_weather()



app = QApplication(sys.argv)

file = QFile("style")
file.open(QFile.ReadOnly | QFile.Text)
stream = QTextStream(file)
app.setStyleSheet(stream.readAll())
file.close()

window = WeatherApp()
window.show()
sys.exit(app.exec_())