# Espartan

Espartan is a central management portal for ESP32-based smart thermostats, open-door sensors, and mailbox sensors. It provides a user-friendly interface to provision, monitor, and control multiple devices from a single dashboard. It consists of a Python/FastAPI backend, MicroPython-based applications for the ESP32 devices, and a React frontend. It relies on the [espark](https://github.com/ayltai/espark) library for seamless communication between the frontend, backend, and the devices.

## Features

- **Device Provisioning**: Easily add new ESP32 devices to the system through a simple web interface.
- **Telemetry Collection**: Collect and visualise telemetry data from connected devices in real-time.
- **Remote Control**: Adjust thermostat settings and monitor door sensor status remotely.

## Hardware Requirements

### Smart Thermostat

- ESP32-C3 development board
- SHT20 temperature and humidity sensor
- Self-locking relay module
- Voltage divider for voltage measurement
- Battery

### Open-Door Sensor

- ESP32-C3 development board
- Magnetic reed switch
- Active buzzer
- LD2420 human presence sensor
- PIR motion sensor
- Battery

## Project Structure

```
Espartan/
├── App/                # Mobile app (React Native)
│
├── Master/
│   ├── backend/           # FastAPI backend (Python)
│   │   ├── src/
│   │   │   ├── data/         # Models, repositories
│   │   │   ├── routers/      # API endpoints
│   │   │   ├── schedules/    # Scheduled tasks
│   │   │   ├── services/     # Business logic
│   │   │   ├── strategies/   # Device control strategies
│   │   │   ├── utils/        # Utility functions
│   │   │   └── main.py       # Application entry point
│   │   │
│   │   ├── tests/            # Unit tests
│   │   └── Dockerfile        # Backend containerisation
│   │
│   └── frontend/          # React frontend (TypeScript)
│       ├── public/           # Static assets
│       └── src/
│           └── index.tsx     # Application entry point
│
├── Worker-Door/        # ESP32 door sensor application (MicroPython)
│   ├── src/
│   │   ├── configs.py        # Application- and device-specific configurations
│   │   ├── secrets.py        # Credentials and sensitive information
│   │   └── worker_node.py    # Core application logic
│   │
│   ├── main.py            # Application entry point
│   └── tests/             # Unit tests
│
├── Worker-Mail/        # ESP32 mailbox sensor application (MicroPython)
│   ├── src/
│   │   ├── configs.py        # Application- and device-specific configurations
│   │   ├── secrets.py        # Credentials and sensitive information
│   │   └── worker_node.py    # Core application logic
│   │
│   ├── main.py            # Application entry point
│   └── tests/             # Unit tests
│
└── Worker-Thermostat/  # ESP32 thermostat application (MicroPython)
    ├── src/
    │   ├── configs.py        # Application- and device-specific configurations
    │   ├── secrets.py        # Credentials and sensitive information
    │   └── worker_node.py    # Core application logic
    │
    ├── main.py            # Application entry point
    └── tests/             # Unit tests
```

## Development Workflows

### Master Backend

- **Install dependencies:**  
  ```sh
  cd Master/backend
  make venv
  source venv/bin/activate
  make upgrade
  ```
- **Run server:**  
  ```sh
  make
  ```
- **Configuration:**  
  Edit `.env` config files in `Master/backend` as needed.

### Master Frontend

- **Install dependencies:**  
  ```sh
  cd Master/frontend
  pnpm i
  ```
- **Start development server:**  
  ```sh
  pnpm start
  ```

### Worker Nodes (ESP32 Devices)

- **Install dependencies (only for development):**  
  ```sh
  cd Worker-Door  # or cd Worker-Thermostat
  make venv
  source venv/bin/activate
  make upgrade
  ```
- **Configuration:**  
  Adjust config files in `src/configs.py` as needed.
- **Flashing firmware:**
  ```sh
  make flash
  ```
- **Deployment:**
  ```sh
  make deploy
  ```

### Docker Deployment

- **Build backend container:**
  ```
  cd Master
  make build
  ```
- **Run backend container:**
  ```sh
  make docker
  ```
- **Publish image:**
  ```sh
  make publish
  ```
  