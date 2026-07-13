## Local development

> **Prerequisite:** Required Azure infra must be provisioned first — see [InfraSetup.md](InfraSetup.md).

1. Install Python 3.11 and the [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server) for your OS.
2. Create a virtual environment: `python -m venv myenv`
3. Activate it:
   - Windows (PowerShell): `myenv\Scripts\Activate.ps1`
   - Windows (cmd.exe): `myenv\Scripts\activate.bat`
   - macOS/Linux: `source myenv/bin/activate`
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in `SQL_CONNECTION_STRING` and `JWT_SECRET_KEY`.
6. Run: `uvicorn app.main:app --reload --env-file .env`
7. Visit `http://localhost:8000` → redirects to `/login`.

Tables (`Users`, `UserData`) are created automatically on startup if they don't exist.

