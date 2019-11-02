from bs4 import BeautifulSoup
import requests

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.core.image import Image
from kivy.core.window import Window


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


class WindowManager(ScreenManager):
    pass


class MainWindow(Screen):
    search = ObjectProperty(None)

    def search_btn(self):
        self.ids.weather_img.source = ""
        city = self.search.text
        print(f"Searching {city}")

        url = f"https://www.google.com/search?q={city}+weather"
        s = requests.Session()
        raw_html = s.get(url, headers=headers).text
        weather_soup = BeautifulSoup(raw_html, "lxml")

        city_found = weather_soup.find("div", id="wob_loc")
        temp = weather_soup.find("span", id="wob_tm")
        condition = weather_soup.find("span", id="wob_dc")

        print(city_found.text)
        print(temp.text)
        print(condition.text)

        self.ids.city.text = city_found.text
        self.ids.temp.text = f"{condition.text}\n{temp.text} Degrees"


        if condition.text.count("Sunny") > 0:
            self.ids.weather_img.source = "./images/sunny.png"
        elif condition.text == "Mostly Cloudy" or condition.text == "Partly Cloudy":
            self.ids.weather_img.source = "./images/partly_cloudy.png"
        elif condition.text == "Cloudy":
            self.ids.weather_img.source = "./images/cloudy.png"
        elif condition.text == "Scattered Showers" or condition.text == "Rain" or condition.text.count("Rain") > 0:
            self.ids.weather_img.source = "./images/rain.png"
        elif condition.text.count("Snow") > 0:
            self.ids.weather_img.source = "./images/snow.png"

        if 0 == 1:
            print("true")


kv = Builder.load_file("./Weather_gui.kv")


class WeatherApp(App):
    def build(self):
        self.title = "Weather App"
        self.icon = "./icon.ico"
        return kv


if __name__ == "__main__":
    WeatherApp().run()