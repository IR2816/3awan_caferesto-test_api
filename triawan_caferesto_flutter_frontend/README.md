# triawan_caferesto_flutter_frontend

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

## Running the app locally (connecting to the FastAPI backend)

1. Start the backend API (3awan-caferesto-api). From the repo root or the backend folder run:

	 - Activate your Python venv and start uvicorn (for a device on the same LAN use --host 0.0.0.0):

		 ```powershell
		 cd "d:\UTS Mobile Platform\3awan-caferesto-api"
		 .\venv\Scripts\activate
		 .\venv\Scripts\uvicorn app.main:app --reload --host 127.0.0.1
		 ```

	 If you want to test from a physical mobile device on the same Wi‑Fi network, use:

		 ```powershell
		 .\venv\Scripts\uvicorn app.main:app --reload --host 0.0.0.0
		 ```

2. Configure the frontend API base for the device: open `lib/services/api_service.dart` and set `deviceIp` to your PC's IPv4 address (e.g. `192.168.1.42`).

3. From the Flutter project folder run:

	 ```powershell
	 cd "d:\UTS Mobile Platform\triawan_caferesto_flutter_frontend"
	 flutter pub get
	 flutter run
	 ```

Notes:
- For Android emulator: the app will connect to `http://10.0.2.2:8000/api` automatically.
- For iOS simulator: the app uses `http://127.0.0.1:8000/api`.
- For web: the app uses `http://localhost:8000/api`.
- For a physical device, use the `deviceIp` value plus `:8000/api` and make sure the backend is started with `--host 0.0.0.0`.

