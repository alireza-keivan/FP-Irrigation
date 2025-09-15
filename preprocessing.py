import pandas as pd
import numpy as np
import scipy.signal as signal
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import base64
from io import BytesIO
import json
import sys

# This section acts as the 'parameters' cell in the notebook.
# It is designed to be injected with the CSV file path by papermill.
input_csv_path = 'default_path_to_a_test_file.csv'

def generate_charts(input_path):
    """
    Reads a CSV, generates charts, and returns them as a list of base64 strings.
    """
    try:
        df = pd.read_csv(input_path)
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df.set_index('ts', inplace=True)
    except FileNotFoundError:
        print(f"Error: File not found at '{input_path}'", file=sys.stderr)
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}", file=sys.stderr)
        return []

    charts = []

    # Chart 1: Temperature and Humidity
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x=df.index, y='temperature', label='Temperature (°C)')
    sns.lineplot(data=df, x=df.index, y='humidity', label='Humidity (%)')
    plt.title('Store Temperature and Humidity Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    charts.append(base64.b64encode(buf.read()).decode('utf-8'))
    plt.close()

    # Chart 2: Soil Metrics
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x=df.index, y='moisture', label='Soil Moisture (%)')
    sns.lineplot(data=df, x=df.index, y='soil_temperature', label='Soil Temperature (°C)')
    plt.title('Soil Metrics Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    charts.append(base64.b64encode(buf.read()).decode('utf-8'))
    plt.close()

    return charts

if __name__ == '__main__':
    # This block is for testing purposes and can be removed when using papermill
    # Pass the input_csv_path from the command line arguments
    if len(sys.argv) > 1:
        input_csv_path = sys.argv[1]
    
    all_charts = generate_charts(input_csv_path)
    
    # In a notebook, charts are automatically displayed. 
    # In a script, we print them to stdout, which `papermill` captures.
    for chart in all_charts:
        print(chart)
