import sys
import pprint
import requests
from dateutil.parser import parse


class YahooWheatherForecast:
    """
    docstring
    """
    def get(self, city):
        """
        yahoo
        """
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=d97974845f0992623ec15809aab46267&units=metric&lang=ru"
        data = requests.get(url).json()
        forecast = []
        forecast_data = data["main"]
        forecast.append({
                #"date": parse(day_data["date"]),
                "temp": float(forecast_data["temp"])#,
                #"feel_like": int(forecast_data["feel_like"])
            })
        #for day_data in forecast_data:
          #  )
        
        return forecast

class CityInfo:

    def __init__(self, city, forecast_provider = None):
        """
        init
        """
        self.city = city.lower()
        self._forecast_provider = forecast_provider or YahooWheatherForecast()

    def weather_forecast(self):
        """
        docstring
        """
        return self._forecast_provider.get(self.city)

def _main():
    city = CityInfo("Moscow")
    forecast  = city.weather_forecast()
    pprint.pprint(forecast)


if __name__ == "__main__":
    _main()