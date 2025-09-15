import paho.mqtt.client as paho
import os
import json
import time
import logging
import pandas as pd
import numpy as np
from numpy.lib.stride_tricks import as_strided

df_TH = pd.read_csv('/home/.../thingsboard_EM300-TH_2025-09-03.csv')

df_TH["timestamp"] = df_TH["timestamp"].astype("datetime64[ns]")
df_TH = df_TH.sort_values(by='timestamp')


df_TH['humidity'] = pd.to_numeric(df_TH['humidity'], errors='coerce')
df_TH['temperature'] = pd.to_numeric(df_TH['temperature'], errors='coerce')
df_TH['timestamp'] = pd.to_datetime(df_TH['timestamp'])
df_TH['hour'] = df_TH['timestamp'].dt.hour

hourly_humidity = df_TH.groupby('hour')['humidity'].agg(['mean', 'max', 'min']).reset_index()
hourly_temperature = df_TH.groupby('hour')['temperature'].agg(['mean', 'max', 'min']).reset_index()



def output():
    list_temperature = []
    list_humidity = []
    diff_temperature_humidity = []
    diff_all = []
    for i in range(23):  
        list_humidity.append(float(hourly_humidity['mean'][i]))
        list_temperature.append(float(hourly_temperature['mean'][i]))
        diff_temperature_humidity.append(float(list_humidity[i]) - float(list_temperature[i]))

        diff_all.append(int(diff_temperature_humidity[i]) - int(list_temperature[i]))
    return diff_all

window_size = 4
arr = np.array(output())
sliding_windows = as_strided(arr, shape=(len(arr) - window_size + 1, window_size), strides=(arr.strides[0], arr.strides[0]))
cumulative_sums = np.sum(sliding_windows, axis=1)
max_sum_index = np.argmax(cumulative_sums)
best_slice = sliding_windows[max_sum_index]
start_hour = max_sum_index
end_hour = start_hour + window_size
final_result = f"Hours {start_hour}-{end_hour} is the best time for irrigation."

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='log.log',
    filemode='a'
)

config = {
    "mqtt_settings": {
        "MQTT_BROKER_ADDRESS": "192.168...",
        "MQTT_BROKER_PORT": 1883,
        "MQTT_CLIENT_ID": "...",
        "MQTT_USERNAME": "...",
        "MQTT_PASSWORD": "...",
        "MQTT_FACE_TOPIC": "v1/.../telemetry"
    }
}

message_status = {}

queued_messages = set()

pending_messages = 0

# Reconnection attempts
MAX_RECONNECT_ATTEMPTS = 3
RECONNECT_DELAY = 5  # seconds

def on_connect(client, userdata, flags, rc):
    global pending_messages
    if rc == 0:
        logging.info("Connected to MQTT Broker successfully.")
        publish_images(client)
    else:
        logging.error(f"Failed to connect to MQTT Broker. Return code: {rc}.")
        if rc == 1:
            logging.error("Connection refused - incorrect protocol version.")
        elif rc == 2:
            logging.error("Connection refused - invalid client identifier.")
        elif rc == 3:
            logging.error("Connection refused - server unavailable.")
        elif rc == 4:
            logging.error("Connection refused - bad username or password.")
        elif rc == 5:
            logging.error("Connection refused - not authorized.")
        else:
            logging.error("Connection failed for an unknown reason.")
        # Attempt to reconnect
        reconnect(client)

def on_publish(client, userdata, mid):
    global pending_messages
    if mid in message_status:
        message_info = message_status.pop(mid)
        logging.info(f"✅ Message for '{message_info['filename']}' with MID {mid} published successfully to topic '{message_info['topic']}'.")
    else:
        logging.info(f"✅ Message with MID {mid} published successfully. No matching file info found.")
    pending_messages -= 1
    if pending_messages == 0:
        logging.info("All messages published. Disconnecting.")
        client.disconnect()

def on_disconnect(client, userdata, rc, properties=None, reason=None):
    
    global pending_messages
    if rc != 0:
        logging.warning(f"⚠️ Disconnected from MQTT Broker unexpectedly. Return code: {rc}. Properties: {properties}. Reason: {reason}.")
        reconnect(client)
    else:
        logging.info("Disconnected from MQTT Broker cleanly.")

def reconnect(client):
    global pending_messages
    attempt = 0
    while attempt < MAX_RECONNECT_ATTEMPTS:
        attempt += 1
        logging.info(f"Reconnection attempt {attempt}/{MAX_RECONNECT_ATTEMPTS}...")
        try:
            client.reconnect()
            logging.info("Reconnected successfully.")
            return
        except Exception as e:
            logging.error(f"Reconnection attempt {attempt} failed: {e}")
            time.sleep(RECONNECT_DELAY)
    logging.error("❌ Max reconnection attempts reached. Aborting.")
    client.disconnect()

def publish_images(client):
    global message_status, pending_messages, queued_messages, final_result
    try:
        payload = {
            "suggestion": final_result
        }

        topic = config['mqtt_settings']['MQTT_FACE_TOPIC']
        payload_str = json.dumps(payload)
        payload_size = len(payload_str) / 1024  # Size in KB
        logging.info(f"⏳ Attempting to publish '{final_result}' to topic '{topic}' (Payload size: {payload_size:.2f} KB).")
        
        
        result, mid = client.publish(topic, payload_str, qos=1)
        
        if result == paho.MQTT_ERR_SUCCESS:
            message_status[mid] = {'filename': final_result, 'topic': topic}
            queued_messages.add(final_result)
            pending_messages += 1
            logging.info(f"Message for '{final_result}' queued successfully with MID {mid}.")
        else:
            logging.error(f"❌ Failed to queue message for '{final_result}'. Result code: {result}.")
            
        time.sleep(3)  # Increased to 3 seconds
        
    except Exception as e:
        logging.error(f"❌ An error occurred while processing or publishing '{final_result}': {e}")
 
if __name__ == "__main__":
    client = paho.Client(paho.CallbackAPIVersion.VERSION1, client_id=config['mqtt_settings']['MQTT_CLIENT_ID'])
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    client.username_pw_set(
        config['mqtt_settings']['MQTT_USERNAME'],
        config['mqtt_settings']['MQTT_PASSWORD']
    )
    
    # Set keep-alive to 120 seconds
    try:
        client.connect(
            config['mqtt_settings']['MQTT_BROKER_ADDRESS'],
            config['mqtt_settings']['MQTT_BROKER_PORT'],
            keepalive=120
        )
    except Exception as e:
        logging.error(f"❌ Failed to connect to MQTT broker: {e}")
        exit(1)

    client.loop_start()
    
    last_ping = time.time()
    while client.is_connected() or pending_messages > 0:
        if time.time() - last_ping > 60:
            try:
                client.ping()
                logging.info("Sent keep-alive ping to broker.")
                last_ping = time.time()
            except Exception as e:
                logging.error(f"Failed to send keep-alive ping: {e}")
        time.sleep(1)
    
    client.loop_stop()
    client.disconnect()
