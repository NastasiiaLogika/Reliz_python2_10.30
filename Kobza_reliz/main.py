from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import sys
import requests
from datetime import datetime, timedelta

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Реальна погода")
        self.setGeometry(100, 100, 400, 300)

        self.central_Widget = QWidget()
        self.setCentralWidget(self.central_Widget)
        self.layout = QVBoxLayout()
        self.central_Widget.setLayout(self.layout)


        self.city_label = QLabel("Обрене місто: ", self)
        self.layout.addWidget(self.city_label)

        self.city_combo = QLineEdit(self)
        self.layout.addWidget(self.city_combo)
        



        self.button = QPushButton("Дізнатися погоду", self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.get_weather)

        self.button.setStyleSheet("""

        QPushButton{
            background-color: #106a99;
            color: black;
            padding: 7px 10px;
            border: none;                            
            border-radius: 3px;
        }
                                                                     
    
                                                                         """)

        self.button_update = QPushButton("Оновлення", self)
        self.layout.addWidget(self.button_update)
        self.button_update.clicked.connect(self.update_weather)

        self.button_update.setStyleSheet("""

        QPushButton{
            background-color: #f9f62e;
            color: black;
            padding: 7px 10px;
            border: none;                            
            border-radius: 3px;
        }
                                                                     
    
                                                                         """)
        
        self.weather_label = QLabel('', self)
        self.layout.addWidget(self.weather_label)
        self.weather_label.setStyleSheet("font_size: 18px;")

        self.icon_label = QLabel(self)
        self.layout.addWidget(self.icon_label)


        self.tomorrow_label = QLabel("Завтрішня погода", self)
        self.layout.addWidget(self.tomorrow_label)
        self.tomorrow_label.setStyleSheet("font_size: 19px;")

        self.weather_label_tomorrow = QLabel('', self)
        self.layout.addWidget(self.weather_label_tomorrow)
        self.weather_label_tomorrow.setStyleSheet("font_size: 18px;")

        self.icon_label_tomorrow = QLabel(self)
        self.layout.addWidget(self.icon_label_tomorrow)



        self.last_update = QLabel('', self)
        self.layout.addWidget(self.last_update)

        self.get_weather()


    def get_weather(self):
        api_key = 'f81703c1f3b81ad93e6644153c4a426e'
        city = self.city_combo.text().strip()
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            icon_name = data['weather'][0]['icon']
            icon_url = f'http://openweathermap.org/img/w/{icon_name}.png'

            weather_text = f'Погода: {weather}\n Температура: {temperature}C\n Вологість: {humidity}%\n Швидкість вітру: {wind_speed}m/c'
            self.weather_label.setText(weather_text)

            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(icon_url).content)
            self.icon_label.setPixmap(pixmap)

        else:
            self.weather_label.setText("Місто не знайдено")
            return

        url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

        response2 = requests.get(url_forecast)
        data2 = response2.json()

        if data2['cod'] == '200':
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            forecast_list = data2["list"]

            # знаходимо прогноз на завтра о 12:00
            forecast_12pm = next((f for f in forecast_list if f["dt_txt"].startswith(tomorrow) and "12:00:00" in f["dt_txt"]), None)


            if forecast_12pm:
                weather = forecast_12pm['weather'][0]['description']
                temperature = forecast_12pm['main']['temp']
                humidity = forecast_12pm['main']['humidity']
                wind_speed = forecast_12pm['wind']['speed']
                icon_name = forecast_12pm['weather'][0]['icon']
                icon_url = f'http://openweathermap.org/img/w/{icon_name}.png'

                weather_text_2 = f'Погода: {weather}\n Температура: {temperature}C\n Вологість: {humidity}%\n Швидкість вітру: {wind_speed}m/c'
                self.weather_label_tomorrow.setText(weather_text_2)

                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(icon_url).content)
                self.icon_label.setPixmap(pixmap)

                now = datetime.now()
                formatted_date = now.strftime("%d.%m.%Y %H.%M.%S")
                self.last_update.setText(f'Останнє оновлення: {formatted_date}')

            else:
                self.weather_label_tomorrow.setText("Немає прогнозу погоди на 12:00 завтра")

        else:
            self.weather_label.setText("Місто не знайдено")

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


