#!/bin/bash
# Azure App Service (Linux, Python) startup command.
# The built-in PYTHON|3.11 image does not ship msodbcsql18, which pyodbc
# needs to talk to Azure SQL. Install it once per container instance, then
# launch the app with gunicorn + uvicorn workers.
set -e

if ! odbcinst -q -d -n "ODBC Driver 18 for SQL Server" > /dev/null 2>&1; then
  echo "Installing msodbcsql18..."
  curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - > /dev/null 2>&1
  curl -sSL https://packages.microsoft.com/config/debian/11/prod.list -o /etc/apt/sources.list.d/mssql-release.list
  apt-get update -qq
  ACCEPT_EULA=Y apt-get install -y -qq msodbcsql18 unixodbc-dev
else
  echo "msodbcsql18 already installed."
fi

exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 --timeout 120 app.main:app
