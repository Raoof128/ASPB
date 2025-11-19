# Azure Service Principal Secret Expiry Bot

**Prevent production outages by automatically detecting expiring Azure Service Principal credentials.**

This tool connects to your Azure Entra ID (formerly Azure AD), enumerates all Service Principals, checks their client secrets and certificates, and alerts you when any credential is about to expire.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Azure](https://img.shields.io/badge/azure-identity-0078D4)

---

## 🚀 Why This Matters

Service Principals are the non-human identities that power your automation, CI/CD pipelines, and backend services. Unlike user passwords, **service principal secrets expire silently**.

When a secret expires:
1. **Production breaks**: Applications relying on that SP suddenly fail authentication.
2. **Scramble ensues**: DevOps teams rush to identify *which* key expired and rotate it.
3. **Downtime**: Critical services remain down until the key is replaced.

This bot solves that problem by giving you a 30-day heads-up.

---

## ✨ Features

- **Automated Discovery**: Enumerates all Service Principals in your tenant.
- **Deep Inspection**: Checks both **Client Secrets** (passwords) and **Certificates** (keys).
- **Smart Severity**:
  - 🔴 **EXPIRED**: Credential is already dead.
  - 🟠 **CRITICAL**: Expires in < 30 days.
  - 🟡 **WARNING**: Expires in 30-60 days.
  - 🟢 **HEALTHY**: Good for > 60 days.
- **Flexible Reporting**: Outputs to Console Table, CSV, JSON, or Markdown.
- **Secure Auth**: Uses `DefaultAzureCredential` for seamless local (CLI) and cloud (Managed Identity) authentication.

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/sp-secret-bot.git
   cd sp-secret-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment (Optional):**
   Copy the example env file if you need to override default auth settings.
   ```bash
   cp .env.example .env
   ```

---

## 🔑 Azure Permissions

To scan Service Principals, the identity running this tool needs **Read** access to the directory.

### Required Graph API Permissions:
- `Application.Read.All` (Type: Application or Delegated)

### How to Authenticate:
The tool uses `DefaultAzureCredential`, which tries multiple methods in order:
1. **Environment Variables** (`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`)
2. **Azure CLI** (`az login`)
3. **Managed Identity** (if running in Azure)

**Quick Start (Local):**
1. Copy `.env.example` to `.env` and fill in your credentials (optional if using CLI).
2. Or simply run:
```bash
az login
# Ensure you are in the correct tenant
az account set --subscription <SUBSCRIPTION_ID>
```

---

## 🐳 Dev Container

This repository includes a `.devcontainer` configuration. If you use VS Code, you can open the folder in a container to get a pre-configured development environment with Python, Azure CLI, and all dependencies installed.

---

## 🏃 Usage

### Using Make (Recommended)
The project includes a `Makefile` for common tasks:
```bash
make install   # Install dependencies
make test      # Run tests
make lint      # Run linters
make run       # Run the bot
```

### Manual Usage
Run the bot as a module:

### 1. Basic Scan (Console Table)
```bash
python3 -m sp_secret_bot.main scan
```

### 2. Scan & Save to CSV
```bash
python3 -m sp_secret_bot.main scan --output report.csv
```

### 3. JSON Output (for automation)
```bash
python3 -m sp_secret_bot.main scan --format json --output secrets.json
```

### 4. Critical Only (Quiet Mode)
Only show secrets expiring in the next 30 days or already expired.
```bash
python3 -m sp_secret_bot.main scan --critical-only
```

---

## 📊 Sample Output

### Console Output
```text
+--------------------------------+--------------------------------------+----------+-------------+------------+
| Service Principal              | App ID                               | Type     |   Days Left | Severity   |
+================================+======================================+==========+=============+============+
| CI/CD Pipeline Runner          | a1b2c3d4-e5f6-7890-1234-567890abcdef | Password |           5 | CRITICAL   |
+--------------------------------+--------------------------------------+----------+-------------+------------+
| Legacy Billing App             | f1e2d3c4-b5a6-0987-4321-fedcba098765 | Password |         -12 | EXPIRED    |
+--------------------------------+--------------------------------------+----------+-------------+------------+
| Backup Service                 | 98765432-10ab-cdef-1234-567890abcdef | Key      |          45 | WARNING    |
+--------------------------------+--------------------------------------+----------+-------------+------------+
```

### JSON Output
```json
[
    {
        "Service Principal": "CI/CD Pipeline Runner",
        "App ID": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "Secret Type": "Password",
        "Key ID": "uuid-key-id",
        "Expiry Date": "2023-12-01T12:00:00+00:00",
        "Days Remaining": 5,
        "Severity": "CRITICAL"
    }
]
```

---

## 🧪 Running Tests

Run the unit test suite to verify logic:

```bash
python3 -m unittest discover tests
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Submit a Pull Request

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
