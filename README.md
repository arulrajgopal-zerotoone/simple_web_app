# Simple Web App

FastAPI + Jinja2 app on a single Azure App Service, backed by Azure SQL Database.

## Layout

```
app/
  main.py            FastAPI app, page routes, startup table creation
  database.py        SQLAlchemy engine/session (reads SQL_CONNECTION_STRING)
  models.py          Users, UserData ORM models
  schemas.py         Pydantic request/response models
  security.py        bcrypt password hashing + JWT helpers
  deps.py            auth dependencies (cookie-based session)
  routers/auth.py    /api/auth/signup, /login, /logout
  routers/records.py /api/records ... (CRUD, scoped to current user)
  templates/         login.html, signup.html, insert.html, dashboard.html
  static/            app.js, style.css
sql/schema.sql        reference DDL (tables are also auto-created at startup)
startup.sh             App Service startup command: installs msodbcsql18, runs gunicorn
.github/workflows/deploy.yml   CI/CD to Azure App Service
```

## How auth and data isolation work

- Passwords are hashed with bcrypt (`passlib`) — never stored in plain text.
- On signup/login, the server issues a JWT (HS256) and sets it as an `httponly`,
  `secure`, `samesite=lax` cookie (`access_token`). The browser sends it automatically
  on subsequent requests; there's no token handling needed in the frontend JS.
- Every `/api/records/*` route depends on `get_current_user`, which decodes the
  cookie and loads the `User` row. All queries filter by `user_id == current_user.user_id`,
  so one user can never see or modify another user's rows.



## Infrastructure - will be provisioned via Terraform

See [InfraSetup.md](InfraSetup.md) for the infrastructure setup steps — this is a
prerequisite before deploying this app.

| Resource | Name |
|---|---|
| Resource group | `rg-webapp-dev` |
| App Service | `kaninipro-webapp-dev` (Linux, `PYTHON|3.11`, plan `kaninipro-plan-dev` / B1) |
| Azure SQL server | `kaninipro-server-dev.database.windows.net` |
| Azure SQL database | `kaninipro-database-dev` |
| Key Vault | `kaninipro-kv-dev` |


The Web App already has `SQL_CONNECTION_STRING` set as an app setting pointing to a
Key Vault reference (`@Microsoft.KeyVault(SecretUri=...)`) resolved via its system-assigned
managed identity — the connection string is never stored in this repo or in GitHub secrets.


## Deployment secrets (GitHub Actions)

Configure these repository secrets (`Settings → Secrets and variables → Actions`):

| Secret | Purpose |
|---|---|
| `AZURE_CLIENT_ID` | Service principal used by `azure/login` |
| `AZURE_CLIENT_SECRET` | Service principal secret |
| `AZURE_TENANT_ID` | Azure AD tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Target subscription |
| `JWT_SECRET_KEY` | Signing key for session JWTs (generate with `python -c "import secrets; print(secrets.token_urlsafe(48))"`) |


The service principal needs `Contributor` (or narrower `Website Contributor`) on
`rg-webapp-dev` to run `az webapp config set` / `config appsettings set` and deploy.

`.github/workflows/deploy.yml`:
1. Builds and zips the app.
2. Logs in to Azure with the service principal.
3. Sets the App Service startup command to `startup.sh`.
4. Sets the `JWT_SECRET_KEY` app setting (the only secret not already in Key Vault).
5. Zip-deploys to `kaninipro-webapp-dev`.

`SCM_DO_BUILD_DURING_DEPLOYMENT=true` is already set on the Web App (see Terraform),
so Oryx runs `pip install -r requirements.txt` during deployment.

## ODBC driver (pyodbc + msodbcsql18)

The built-in Linux Python image on App Service does not ship `msodbcsql18`. `startup.sh`
is set as the site's startup command and installs it via `apt-get` on first boot of each
container instance, then launches the app with:

```
gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app
```

## Suggested follow-up

Consider moving `JWT_SECRET_KEY` into the same `kaninipro-kv-dev` Key Vault (as a
second secret + Key Vault reference app setting, mirroring `sql-connection-string`)
instead of setting it directly as a GitHub Actions app setting.
