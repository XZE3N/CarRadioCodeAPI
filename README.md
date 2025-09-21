# Car Radio Code API

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

A FastAPI-based service for decoding car radio security codes.  
Supports multiple manufacturers through a **plugin system** – each make has its own decoder package.

---

## 🚀 Features
- Decode car radio unlock codes for supported manufacturers.
- Plugin-based system: each manufacturer implements its own decoder in `decoders/<make>/decoder.py`.
- Central registry automatically loads all available decoders.
- Clean request/response schemas with **Pydantic models**.
- Custom exception handlers with helpful error messages.
- Auto-generated documentation via **Swagger UI** (`/docs`) and **ReDoc** (`/redoc`).

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/XZE3N/CarRadioCodeAPI.git
cd CarRadioCodeAPI

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # (Linux/macOS)
venv\Scripts\activate      # (Windows)

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the API

```bash
uvicorn main:app --reload
```

The API will be available at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  
- Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)  

---

## 📡 Usage

### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/decode" ^
  -H "accept: application/json" ^
  -H "Content-Type: application/json" ^
  -d "{ \"make\": \"Ford\", \"serial_number\": \"M123456\" }"
```

### Example Response

```json
{
  "make": "Ford",
  "unlock_code": "5807",
  "serial_number": "M123456"
}
```

If required fields are missing or invalid, the API will return a structured error:

```json
{
  "error": {
    "code": 400,
    "message": "Invalid Ford serial format (Expected format: M123456 or V123456)",
    "hint": "Check your request and try again"
  }
}
```

---

## 🛠️ Adding a New Decoder

1. Create a new package under `decoders/<make>/`.
2. Add a `decoder.py` file with a class extending `BaseDecoder`.
3. Implement the `decode()` and (optionally) `compute()` methods.
4. Register your decoder:
   ```python
   MyDecoder.register("mymake")
   ```
5. The new manufacturer will automatically appear in `/docs`.

---


## ✅ Supported Manufacturers
This list is generated automatically from the decoder registry:

- Ford
- Renault
- Dacia
- More manufacturers to come...

---

## 📂 Project Structure

```
car-radio-decoder/
│── decoders/               # Manufacturer decoders
│   ├── base.py              # BaseDecoder & registry
│   └── dacia/decoder.py     # Dacia implementation
│   ├── ford/decoder.py      # Ford implementation
│   └── renault/decoder.py   # Renault implementation
│
│── exceptions/                 # Custom exception handlers
│   └── handlers.py
│
│── models/                 # Pydantic schemas
│   └── schemas.py
│
│── main.py                  # FastAPI entrypoint
│── requirements.txt
└── README.md
```

---

## 🧑‍💻 Development Notes
- Uses **Python 3.9+** and **FastAPI**.
- Registry-based decoder discovery at startup.
- Also provides algorithms for decoding radio security codes for all supported manufacturers.
- For debugging: run `uvicorn main:app --reload --log-level debug`.

---

## 👋 Contributing
Contributions are welcome! Please open an issue or submit a pull request if you'd like to help improve this project.

---

## 📜 License
MIT License – free to use and modify.
