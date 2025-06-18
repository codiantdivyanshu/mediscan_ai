🧠 MediScan AI

MediScan AI is an AI-powered medical prescription and document analyzer built with **FastAPI**. It extracts text from prescriptions using OCR, parses important health data, allows PDF conversion, stores results in a database, and integrates with LLMs via Groq API to answer health-related queries.

🚀 Features

- 📤 Upload prescription images (JPEG, PNG, PDF)
- 🔍 OCR-based text extraction using Tesseract
- 🧾 NLP-based parsing of medical data (patient info, medicines, instructions)
- 🧠 Ask questions about the prescription using Groq’s LLM
- 📄 Convert structured data into downloadable PDF
- 🗂️ Store parsed records in a database
- 🔐 JWT-based authentication with FastAPI
- 🔑 API key environment support via `.env`



📁 Project Structure



mediscan\_ai/
├── app/
│   ├── api/                # Routes
│   ├── models/             # DB models & schemas
│   ├── services/           # OCR, AI, DB, Auth services
│   ├── utils/              # Helper functions
│   └── main.py             # FastAPI entrypoint
├── uploads/                # Uploaded files (optional)
├── .env                    # Environment variables (GROQ\_API\_KEY, etc.)
├── README.md
└── mediscan.db             # SQLite database (optional)


 🛠️ Tech Stack

- Backend: FastAPI
- AI Integration: Groq API (e.g., LLaMA models)
- OCR: Tesseract (via `pytesseract`)
- Auth: FastAPI JWT
- Database: SQLAlchemy + SQLite (async)
- PDF: FPDF for report generation

 🔐 Environment Variables

Create a .env file with:

env
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_jwt_secret_key




▶️ Getting Started
 1. Clone the repo

bash
git clone https://github.com/divyanshugupta068/mediscan_ai.git
cd mediscan_ai


2. Create and activate virtual environment

bash
python3 -m venv venv
source venv/bin/activate

3. Install dependencies

bash
pip install -r requirements.txt


4. Set environment variables

Update .env with your API keys.

5. Run the FastAPI server

bash
uvicorn app.main:app --reload


6. Access the app

 API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
 Health Check: [http://localhost:8000/health](http://localhost:8000/health)

 📌 API Endpoints Summary

| Method | Endpoint            | Description                 |
| ------ | ------------------- | --------------------------- |
| GET    | health              | Server status check         |
| POST   | upload              | Upload & process file       |
| POST   | extract-text        | OCR text extraction         |
| POST   | parse-text          | NLP-based text parsing      |
| POST   | convert-text-to-pdf | Generate a prescription PDF |
| POST   | save-prescription   | Save record to DB           |
| POST   | ask                 | Query LLM for answers       |
| GET    | routes              | List all routes             |


🔒 Authentication (JWT)

To access protected routes (if any), obtain a JWT token via login (WIP).



📚 Sample Prescription (Example Output)

json
{
  "patient": { "name": "John Doe", "age": "35", "gender": "Male" },
  "doctor_name": "Dr. A. Kumar",
  "date_issued": "2024-12-01",
  "medicines": [
    { "name": "Paracetamol", "dosage": "500mg", "frequency": "2x1", "duration": "5 days", "instructions": "After meals" }
  ],
  "notes": "Stay hydrated and get rest"
}

 📌 Future Plans

🌐 Build Streamlit/React UI frontend
📱 Add Flutter mobile support
🔁 Improve parsing with medical LLMs
🧾 Prescription history and QR sharing



👤 Author

Divyanshu Gupta
GitHub: [divyanshugupta068](https://github.com/divyanshugupta068)


📄 License

This project is licensed under the [MIT License](LICENSE).
