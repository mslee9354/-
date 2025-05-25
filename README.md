# 고잉티콘


## Guard Post Entry Control

This example provides a basic guard post entry control system.

### Components

- `server/`: Python server using Flask and a simple Tkinter GUI. It evaluates entry requests with the KoAlpaca model (if available).
- `mobile_app/`: Flutter client for scanning QR codes and sending purpose/destination text to the server.

### Setup

1. Install Python dependencies:

```bash
pip install -r server/requirements.txt
```

2. (Optional) Download the KoAlpaca model to use in `server/server.py`.
3. Run the server:

```bash
python server/server.py
```

4. Build the Flutter app inside `mobile_app/` and run on a device.

### QR Code Generation

Use `server/make_qr.py` to generate QR codes containing person information.

```bash
python server/make_qr.py
```

This creates `person_qr.png` with encoded JSON of the person data.
