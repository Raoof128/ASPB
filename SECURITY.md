# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a vulnerability:

1. **Do NOT open a public issue.**
2. Email the maintainers directly at `security@example.com`.
3. Include details about the vulnerability and steps to reproduce.

We will acknowledge your report within 48 hours and provide a timeline for a fix.

## Credentials Safety

This tool handles sensitive information (Service Principal credentials).
- It **never** logs full secrets or certificates.
- It **never** sends data to third-party services (other than Microsoft Graph API).
- Ensure your environment variables (`AZURE_CLIENT_SECRET`) are secured.
