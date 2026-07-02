import pandas as pd


# Load and preprocess data
df_TH = pd.read_csv('thingsboard_EM300-TH-13-10.csv')

df_TH["time(ns)"] = df_TH["time(ns)"].astype("datetime64[ns]")
df_TH = df_TH.sort_values(by='time(ns)')


df_TH['humidity'] = pd.to_numeric(df_TH['humidity'], errors='coerce')
df_TH['temperature'] = pd.to_numeric(df_TH['temperature'], errors='coerce')
df_TH['time(ns)'] = pd.to_datetime(df_TH['time(ns)'])
df_TH['hour'] = df_TH['time(ns)'].dt.hour

hourly_humidity = df_TH.groupby('hour')['humidity'].agg(['mean', 'max', 'min']).reset_index()
hourly_temperature = df_TH.groupby('hour')['temperature'].agg(['mean', 'max', 'min']).reset_index()


def calculate_irrigation_priority():
    list_temperature = []
    list_humidity = []
    diff_temperature_humidity = []
    diff_all = []
    for i in range(24):  
        list_humidity.append(float(hourly_humidity['mean'][i]))
        list_temperature.append(float(hourly_temperature['mean'][i]))
        diff_temperature_humidity.append(float(list_humidity[i]) - float(list_temperature[i]))

        diff_all.append(int(diff_temperature_humidity[i]) - int(list_temperature[i]))
    return diff_all
with open('output.txt', 'w') as f:
    f.write(str(output()))

print(output())

