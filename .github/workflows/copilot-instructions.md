# Copilot Instructions for Espartan

## Big Picture Architecture
- **Monorepo Structure**: Contains `App`, `Master/backend`, `Master/frontend`, `Worker-*` directories. `App` is a React Native application using the Expo framework. `Master/backend` is a Python/FastAPI API server. `Master/frontend` is a React web application. `Worker-*` are various MicroPython applications for ESP32-based devices.
- **App**: React Native app for end-user interaction and data visualization.
- **Master/backend**: Python/FastAPI server for handling API requests and business logic.
- **Master/frontend**: React web app for device management.
- **Worker-* Applications**: MicroPython applications for ESP32 devices, handling sensor data collection and communication with the backend.

## Tips for AI Agents
- Most logic is provided by the `espark` library, which is an open-source library for managing ESP32 devices and their interactions with backend services.
- Respect the separation between core logic, device-specific implementations, and frontend UI.
- Follow the established folder structures and naming conventions for consistency.
