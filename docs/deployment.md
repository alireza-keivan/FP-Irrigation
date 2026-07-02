# Deployment Guide

## Overview

The Smart Irrigation Decision Support System is designed as a modular application that can be deployed in parks, municipalities, agricultural environments, or any large green space requiring intelligent irrigation planning.

The deployment architecture separates sensing, communication, data processing, and visualization into independent layers, making the system easy to maintain and expand.

---

# Deployment Architecture

```text
Environmental Sensors
(Milesight LoRaWAN Devices)
            │
            ▼
      LoRaWAN Gateway
            │
            ▼
       MQTT Broker
            │
            ▼
Smart Irrigation Application
(Python)
            │
      ┌─────┴─────┐
      ▼           ▼
 Decision Engine  Dashboard
      │
      ▼
 Irrigation Recommendations
```

---

# Hardware Requirements

## Sensor Layer

The platform is designed to work with environmental sensors capable of measuring conditions relevant to irrigation planning.

Typical deployments include:

* Soil moisture sensors
* Air temperature sensors
* Relative humidity sensors
* Water level sensors (optional)

Sensor communication is performed using the LoRaWAN protocol.

---

## Gateway

A LoRaWAN gateway receives sensor data and forwards it to the MQTT broker.

Responsibilities include:

* Receiving sensor packets
* Forwarding data to the local network
* Providing reliable communication between field devices and the application

---

## Server

The application can run on:

* Ubuntu Server
* Windows
* Raspberry Pi
* Edge computers
* Virtual machines
* Cloud instances

Python 3.10+ is recommended.

---

# Software Requirements

Required software components include:

* Python
* MQTT Broker (e.g., Mosquitto)
* Pandas
* NumPy
* Matplotlib
* Jupyter Notebook (development and analysis)

Additional dependencies are listed in `requirements.txt`.

---

# Deployment Steps

## 1. Clone the Repository

```bash
git clone https://github.com/alireza-keivan/FP-Irrigation.git
cd FP-Irrigation
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure the MQTT Broker

Update the MQTT configuration in the configuration files:

* Broker IP Address
* Port
* Username (if required)
* Password (if required)
* MQTT Topics

---

## 5. Connect Sensor Network

Verify that environmental sensor data is successfully reaching the MQTT broker through the LoRaWAN gateway.

Typical data includes:

* Soil moisture
* Air temperature
* Relative humidity

---

## 6. Start the Application

Launch the data acquisition and processing pipeline.

The system will:

* Receive sensor measurements
* Validate incoming data
* Preprocess observations
* Analyze environmental conditions
* Generate irrigation recommendations

---

## 7. Monitor Results

Operators can review:

* Environmental conditions
* Irrigation priorities
* Historical trends
* Recommendation summaries

through the monitoring dashboard.

---

# Directory Layout

```text
FP-Irrigation/

assets/
configs/
data/
docs/
notebooks/
results/
src/

README.md
requirements.txt
```

---

# Scalability

The architecture supports expansion without major software changes.

Examples include:

* Additional LoRaWAN sensors
* Multiple gateways
* Multiple parks
* Larger environmental datasets
* Additional decision rules
* New visualization modules

The modular design allows each component to evolve independently.

---

# Security Considerations

For production deployments, it is recommended to:

* Secure MQTT communication using authentication.
* Restrict broker access to trusted devices.
* Validate incoming sensor data.
* Perform regular backups of collected datasets.
* Monitor gateway connectivity and sensor health.

---

# Maintenance

Routine maintenance includes:

* Monitoring sensor connectivity
* Validating environmental data quality
* Updating software dependencies
* Reviewing decision rules as operational requirements evolve
* Inspecting MQTT communication logs

---

# Future Deployment Improvements

The current architecture can be extended with:

* Docker-based deployment
* Kubernetes orchestration
* Cloud-hosted dashboards
* Automated irrigation controller integration
* Real-time alert notifications
* Remote device management
* Edge computing on Raspberry Pi or NVIDIA Jetson
* Web-based administration panel

These improvements can be integrated while preserving the existing modular architecture.
