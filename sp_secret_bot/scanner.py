import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from .utils import calculate_days_remaining, parse_iso_date


@dataclass
class SecretRisk:
    sp_name: str
    app_id: str
    sp_object_id: str
    secret_id: str
    secret_type: str  # 'Password' or 'Key'
    expiry_date: datetime
    days_remaining: int
    severity: str


class SecretScanner:
    """
    Scans service principals for expiring secrets.
    """

    def __init__(self):
        self.logger = logging.getLogger("SPSecretBot.Scanner")

    def determine_severity(self, days: int) -> str:
        if days < 0:
            return "EXPIRED"
        elif days <= 30:
            return "CRITICAL"
        elif days <= 60:
            return "WARNING"
        else:
            return "HEALTHY"

    def scan_service_principals(self, service_principals: List[Dict[str, Any]]) -> List[SecretRisk]:
        """
        Analyzes a list of service principals and returns a list of risks.
        """
        self.logger.info("Analyzing secrets for expiration risks...")
        risks = []

        for sp in service_principals:
            sp_name = sp.get("displayName", "Unknown")
            app_id = sp.get("appId", "Unknown")
            sp_id = sp.get("id", "Unknown")

            # Check Password Credentials (Client Secrets)
            for cred in sp.get("passwordCredentials", []):
                self._process_credential(sp_name, app_id, sp_id, cred, "Password", risks)

            # Check Key Credentials (Certificates)
            for cred in sp.get("keyCredentials", []):
                self._process_credential(sp_name, app_id, sp_id, cred, "Certificate", risks)

        # Sort by days remaining (ascending)
        risks.sort(key=lambda x: x.days_remaining)

        self.logger.info(f"Analysis complete. Found {len(risks)} credentials.")
        return risks

    def _process_credential(
        self,
        sp_name: str,
        app_id: str,
        sp_id: str,
        cred: Dict[str, Any],
        c_type: str,
        risks: List[SecretRisk],
    ):
        end_date_str = cred.get("endDateTime")
        key_id = cred.get("keyId")

        if not end_date_str:
            return

        expiry_date = parse_iso_date(end_date_str)
        if not expiry_date:
            return

        days = calculate_days_remaining(expiry_date)
        severity = self.determine_severity(days)

        # We generally only care about non-healthy ones for the main report,
        # but the prompt implies listing all or filtering.
        # Let's collect all and let the reporter filter.

        risk = SecretRisk(
            sp_name=sp_name,
            app_id=app_id,
            sp_object_id=sp_id,
            secret_id=key_id,
            secret_type=c_type,
            expiry_date=expiry_date,
            days_remaining=days,
            severity=severity,
        )
        risks.append(risk)
