import pandas as pd
import matplotlib.pyplot as plt
df_TH = pd.read_csv('thingsboard_EM300-TH_2025-09-03.csv')
df_SMTC = pd.read_csv('thingsboard_EM500-SMTC_2025-09-03.csv')
import seaborn as sns
df_TH["timestamp"] = df_TH["timestamp"].astype("datetime64[ns]")
df_SMTC["timestamp"] = df_SMTC["timestamp"].astype("datetime64[ns]")
df_merged = pd.merge_asof(df_SMTC, df_TH, on='timestamp', direction="nearest")

df_merged['moisture'] = pd.to_numeric(df_merged['moisture'], errors='coerce')
df_merged['humidity'] = pd.to_numeric(df_merged['humidity'], errors='coerce')
df_merged['temperature(above-ground)'] = pd.to_numeric(df_merged['temperature(above-ground)'], errors='coerce')
df_merged['ec'] = pd.to_numeric(df_merged['ec'], errors='coerce')

df_merged['timestamp'] = pd.to_datetime(df_merged['timestamp'])
df_merged['hour'] = df_merged['timestamp'].dt.hour

hourly_moisture = df_merged.groupby('hour')['moisture'].agg(['mean', 'max', 'min']).reset_index()
hourly_humidity = df_merged.groupby('hour')['humidity'].agg(['mean', 'max', 'min']).reset_index()
hourly_temperature = df_merged.groupby('hour')['temperature(above-ground)'].agg(['mean', 'max', 'min']).reset_index()
hourly_ec = df_merged.groupby('hour')['ec'].agg(['mean', 'max', 'min']).reset_index()
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))


#plt.plot(hourly_ec['hour'], hourly_ec['mean'], label=' electro conductivity', marker='o')
plt.plot(hourly_temperature['hour'], hourly_temperature['mean'], label=' temperature', marker='o')
plt.plot(hourly_humidity['hour'], hourly_humidity['mean'], label=' humidity', marker='x')
plt.plot(hourly_moisture['hour'], hourly_moisture['mean'], label=' moisture', marker='s')

"""
plt.plot(hourly_humidity['hour'], hourly_humidity['max'], label='Max humidity', marker='s', linestyle='--')
plt.plot(hourly_humidity['hour'], hourly_humidity['min'], label='Min humidity', marker='x', linestyle=':')
plt.plot(hourly_temperature['hour'], hourly_temperature['max'], label='Max temperature', marker='s', linestyle='--')
plt.plot(hourly_temperature['hour'], hourly_temperature['min'], label='Min temperature', marker='x', linestyle=':')

"""
#plt.plot(hourly_moisture['hour'], hourly_moisture['max'], label='Max moisture', marker='s', linestyle='--')
#plt.plot(hourly_moisture['hour'], hourly_moisture['min'], label='Min moisture', marker='x', linestyle=':')


plt.title('Mean of moisture, humidity, and temperature Over a 24-Hour Cycle')
plt.xlabel('Hour of the Day')
plt.ylabel('moisture, humidity, and temperature')
plt.xticks(range(0, 24))
plt.legend()

plt.tight_layout()
plt.savefig('main_plot.png')

y = df_merged['humidity']
x = df_merged['moisture']
colors = df_merged['temperature(above-ground)']

plt.scatter(x, y, c=colors, alpha=0.3, cmap = 'inferno')
plt.xlabel("moisture")
cbar = plt.colorbar()
cbar.set_label('Based on temperature')
plt.ylabel("humidity")
plt.savefig('hu_moi_scatter.png')
plt.show()

#penguins = sns.load_dataset("penguins")
sns.histplot(data=df_merged, x="humidity", y = 'moisture')
plt.savefig('hu_moi_histplot.png')

#penguins = sns.load_dataset("penguins")
sns.histplot(data=df_merged, x="humidity", hue ='hour', legend=False)
#plt.legend(loc='lower left', ncol=2, fontsize='x-large')

plt.savefig('humidity_histplot.png')