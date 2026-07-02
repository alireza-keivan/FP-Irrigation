import requests
api_key = 'a789125a4e865b16b2d16034e054b6d1'

city = ("Mashhad")

url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    temp = data['main']['temp'] - 273
    print(f"Temperature: {temp:.2f}")
    
else:
    print('Error fetching weather data')
