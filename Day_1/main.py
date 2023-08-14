import requests
from bs4 import BeautifulSoup
import lxml
from win10toast import ToastNotifier

toaster = ToastNotifier()


def get_data(url: str) -> dict:
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')

    result = {}
    temperature = soup.find('span', class_='CurrentConditions--tempValue--MHmYY').text
    weather_type = soup.find('div', class_='CurrentConditions--phraseValue--mZC_p').text

    result['temperature'] = temperature
    result['weather-type'] = weather_type

    return result


def main():
    weather = get_data('https://weather.com/en-IN/weather/today/l/a944f87f387a92bc4718ec1bf6f06b1c03217976fc96db720be23e8ba0d954bb')

    toaster.show_toast('Current weather in Almaty', 
                       'Temperature: {}, \nType: {}'.format(weather['temperature'], weather['weather-type']),
                       duration=6)


if __name__ == '__main__':
    main()