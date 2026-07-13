# Troubleshooting Guide

## SQL Server Firewall / IP Whitelisting

### Local Development

When testing locally, whitelist your local machine's IP address in the Azure SQL Server firewall rules. Without this, connections will be blocked by the firewall.

### After Deployment

When running after deployment, make sure the web app's outbound IP address is whitelisted in the Azure SQL Server firewall rules.

If this is not configured, the app will fail with an error similar to the one below. The client IP address needed for whitelisting can be extracted from this error message.

**Example error:**

```
2026-07-13T07:01:41.1595106Z pyodbc.ProgrammingError: ('42000', "[42000] [Microsoft][ODBC Driver 18 for SQL Server][SQL Server]Cannot open server 'kaninipro-server-dev' requested by the login. Client with IP address '20.219.117.158' is not allowed to access the server. To enable access, use the Azure Management Portal or run sp_set_firewall_rule on the master database to create a firewall rule for this IP address or address range. It may take up to five minutes for this change to take effect. (40615) (SQLDriverConnect)")
```

### Fix

1. Copy the client IP address from the error message (e.g. `20.219.117.158`).
2. Go to the Azure Portal → SQL Server (e.g. `kaninipro-server-dev`) → **Networking** (or **Firewalls and virtual networks**).
3. Add a new firewall rule for that IP address (or address range).
4. Save and wait up to 5 minutes for the change to take effect.
