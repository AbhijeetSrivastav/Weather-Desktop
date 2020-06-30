__author__ = "Abhijeet Srivastav"
__copyright__ = "2020 Abhijeet Srivastav"
__license__ = "Public Domain"
__version__ = "1.0"

"""Importing required modules"""
import json
import tkinter as tk
from tkinter import messagebox, StringVar, Entry
from tkinter import ttk
import requests
from PIL import Image, ImageTk

try:
    """For high DPI displays only window machines"""
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    pass


# noinspection PyAttributeOutsideInit
class App(tk.Tk):
    city_entry: Entry
    city_name: StringVar

    def __init__(self):
        super().__init__()

        HEIGHT = 600
        WIDTH = 700

        self.title('Weather')
        self.geometry('{}x{}'.format(WIDTH, HEIGHT))
        self.resizable(False, False)
        self.iconbitmap('icon.ico')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, background='#76ffff')
        canvas.grid(sticky='NSEW')

        background = ImageTk.PhotoImage(Image.open('w.jpg'))
        canvas.background = background
        bg = canvas.create_image(350, 90, image=background)

        self.main_frame = tk.Frame(canvas, borderwidth=10, relief='ridge', background='#03a9f4')
        self.main_frame.grid(row=0, column=0, sticky='NSEW', padx=80, pady=100, ipadx=15, ipady=15)

        self.CreateWidgets()

    def CreateWidgets(self):
        self.city_name = tk.StringVar()

        city_label = ttk.Label(self.main_frame, text='CITY NAME:', background='#4caf50', relief='ridge', borderwidth=6)
        city_label.grid(row=0, column=0)

        self.city_entry = tk.Entry(self.main_frame, width=36, textvariable=self.city_name, relief='sunken',
                                   borderwidth=5)
        self.city_entry.grid(row=0, column=1)
        self.city_entry.focus()

        city_coordinate = ttk.Label(self.main_frame, text='CITY COORDINATES:', background='#4caf50', relief='ridge',
                                    borderwidth=6)
        city_coordinate.grid(row=1, column=0)

        self.city_coordinate_entry = tk.Entry(self.main_frame, width=36, relief='ridge', borderwidth=5)
        self.city_coordinate_entry.grid(row=1, column=1)

        temp_label = ttk.Label(self.main_frame, text='TEMPERATURE:', background='#4caf50', relief='ridge',
                               borderwidth=6)
        temp_label.grid(row=2, column=0)

        self.temp_entry = tk.Entry(self.main_frame, width=36, relief='ridge', borderwidth=5)
        self.temp_entry.grid(row=2, column=1)

        humidity_label = ttk.Label(self.main_frame, text='HUMIDITY:', background='#4caf50', relief='ridge',
                                   borderwidth=6)
        humidity_label.grid(row=3, column=0)

        self.humidity_entry = tk.Entry(self.main_frame, width=36, relief='ridge', borderwidth=5)
        self.humidity_entry.grid(row=3, column=1)

        wind_label = ttk.Label(self.main_frame, text='WIND:', background='#4caf50', relief='ridge', borderwidth=6)
        wind_label.grid(row=4, column=0)

        self.wind_entry = tk.Entry(self.main_frame, width=36, relief='ridge', borderwidth=5)
        self.wind_entry.grid(row=4, column=1)

        pressure_label = ttk.Label(self.main_frame, text='ATMOSPHERIC PRESSURE:', background='#4caf50', relief='ridge',
                                   borderwidth=6)
        pressure_label.grid(row=5, column=0)

        self.pressure_entry = tk.Entry(self.main_frame, width=36, relief='ridge', borderwidth=5)
        self.pressure_entry.grid(row=5, column=1)

        desc_label = ttk.Label(self.main_frame, text='WEATHER DESCRIPTION:', background='#4caf50', relief='ridge',
                               borderwidth=6)
        desc_label.grid(row=6, column=0)

        self.desc_entry = tk.Entry(self.main_frame, width=36, relief='ridge', borderwidth=5)
        self.desc_entry.grid(row=6, column=1)

        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

        find_button = tk.Button(self.main_frame, text='FIND', command=self.FindWeather, relief='raised', borderwidth=3,
                                activebackground='#e91e63')
        find_button.grid(row=7, column=0, columnspan=2)

        clear_button = tk.Button(self.main_frame, text='CLEAR', command=self.ClearEntries, relief='raised',
                                 borderwidth=3, activebackground='#e91e63')
        clear_button.grid(row=7, column=1, columnspan=2)

    def FindWeather(self):
        """Method to fetch data from API and update the widgets"""

        # Storing weather API key
        APIKEY = "64ed795e86547751fa5c3491ff2e31c0"

        # Storing the Weather URL (base URL) to which the requests has to be sent
        weather_URL = "http://api.openweathermap.org/data/2.5/weather?"

        # Fetching the user input city
        city_name = self.city_name.get()

        """Concatenating API key with user input city name with weather URL(base URL)
            and storing the complete URL in requests_URL and setting units = metric means temperature 
            will be shown in celsius"""
        requests_URL = weather_URL + "appid=" + APIKEY + "&q=" + city_name + "&units=metric"

        # Sending the requests to URL and Fetching and Storing the response
        response = requests.get(requests_URL)

        # Converting the response which is in json format data into python format
        weather_response = response.json()

        # Printing weather_response dictionary(optional)
        print(json.dumps(weather_response, indent=2))

        # some values from above weather_response dictionary will be fetched and displayed in tk window

        # Checking if the value is not equal to 404

        if weather_response['cod'] != 404:
            # Fetching and storing the value of "main" key from weather_response
            weather_para = weather_response['main']

            # Fetching and storing the value of "coord" key from weather_response
            coordinates = weather_response['coord']

            # Storing latitude and longitude from coordinates
            latitude = str(coordinates['lat'])
            longitude = str(coordinates['lon'])

            # Fetching and storing the value of "wind" key from weather_response
            wind = weather_response['wind']

            # Storing the speed key value from wind
            wind_speed = str(wind['speed'])

            # Check if deg key present in 'wind' key of weather_response dictionary
            if 'deg' in wind.keys():
                wind_direct = str(['deg'])
            else:
                wind_direct = ''

            # Fetching and storing the temperature value from weather_para
            temperature = str(weather_para['temp'])

            # Fetching and storing the pressure value from weather_para
            pressure = str(weather_para['pressure'])

            # Fetching and storing the humidity value from weather_para
            humidity = str(weather_para['humidity'])

            # Fetching and storing weather value which is a list from weather_response
            weather_desc = weather_response['weather']

            # Storing the description value from 0 index item of weather_disc list
            weather_description = weather_desc[0]['description']

            """SHOWING THE RESULT IN TKINTER"""
            self.city_coordinate_entry.insert('0', 'LATITUDE: ' + latitude + ' LONGITUDE: ' + longitude)
            self.temp_entry.insert('0', temperature + ' °C')
            self.humidity_entry.insert('0', str(humidity) + ' %')
            self.wind_entry.insert('0', 'SPEED:' + wind_speed + ' m/s ' + 'DIRECTION:' + wind_direct + ' deg')
            self.pressure_entry.insert('0', pressure + ' hPa')
            self.desc_entry.insert('0', weather_description)
        else:
            # If cod key value is 404 then city not found
            messagebox.showerror('ERROR', 'CITY NOT FOUND!')

    def ClearEntries(self):
        """This function clears all the value from the text field of the widgets"""
        self.city_name.set('')
        self.city_coordinate_entry.delete(0)
        self.temp_entry.delete(0)
        self.humidity_entry.delete(0)
        self.wind_entry.delete(0)
        self.pressure_entry.delete(0)
        self.desc_entry.delete(0)


if __name__ == '__main__':
    app = App()
    app.mainloop()
