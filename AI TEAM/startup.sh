#!/usr/bin/env bash
set -e
# App Service Free/Linux lacks ODBC Driver 18, which pyodbc needs for Azure SQL.
# Install it at container start if it is missing, then launch the app.
if ! odbcinst -q -d 2>/dev/null | grep -qi 'odbc driver 18'; then
  echo '[startup] installing msodbcsql18 ...'
  apt-get update -y >/dev/null 2>&1 || true
  apt-get install -y --no-install-recommends curl gnupg ca-certificates >/dev/null 2>&1 || true
  curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg 2>/dev/null || true
  printf 'deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/ubuntu/22.04/prod jammy main\n' > /etc/apt/sources.list.d/mssql-release.list 2>/dev/null || true
  apt-get update -y >/dev/null 2>&1 || true
  ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev >/dev/null 2>&1 || echo '[startup] ODBC install failed; app will not reach Azure SQL'
fi
export PYTHONUNBUFFERED=1
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000