import unittest
from datetime import datetime, timedelta, timezone

from sp_secret_bot.scanner import SecretScanner


class TestSecretScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = SecretScanner()

    def test_severity_expired(self):
        self.assertEqual(self.scanner.determine_severity(-1), "EXPIRED")
        self.assertEqual(self.scanner.determine_severity(-100), "EXPIRED")

    def test_severity_critical(self):
        self.assertEqual(self.scanner.determine_severity(0), "CRITICAL")
        self.assertEqual(self.scanner.determine_severity(30), "CRITICAL")

    def test_severity_warning(self):
        self.assertEqual(self.scanner.determine_severity(31), "WARNING")
        self.assertEqual(self.scanner.determine_severity(60), "WARNING")

    def test_severity_healthy(self):
        self.assertEqual(self.scanner.determine_severity(61), "HEALTHY")
        self.assertEqual(self.scanner.determine_severity(365), "HEALTHY")

    def test_scan_logic(self):
        # Mock SP data
        now = datetime.now(timezone.utc)
        expired_date = (now - timedelta(days=5)).isoformat().replace("+00:00", "Z")
        critical_date = (now + timedelta(days=10)).isoformat().replace("+00:00", "Z")
        healthy_date = (now + timedelta(days=100)).isoformat().replace("+00:00", "Z")

        mock_sps = [
            {
                "id": "sp1",
                "appId": "app1",
                "displayName": "Expired SP",
                "passwordCredentials": [{"keyId": "k1", "endDateTime": expired_date}],
            },
            {
                "id": "sp2",
                "appId": "app2",
                "displayName": "Critical SP",
                "keyCredentials": [{"keyId": "k2", "endDateTime": critical_date}],
            },
            {
                "id": "sp3",
                "appId": "app3",
                "displayName": "Healthy SP",
                "passwordCredentials": [{"keyId": "k3", "endDateTime": healthy_date}],
            },
        ]

        risks = self.scanner.scan_service_principals(mock_sps)

        self.assertEqual(len(risks), 3)

        # Check Expired
        self.assertEqual(risks[0].sp_name, "Expired SP")
        self.assertEqual(risks[0].severity, "EXPIRED")

        # Check Critical
        self.assertEqual(risks[1].sp_name, "Critical SP")
        self.assertEqual(risks[1].severity, "CRITICAL")

        # Check Healthy
        self.assertEqual(risks[2].sp_name, "Healthy SP")
        self.assertEqual(risks[2].severity, "HEALTHY")


if __name__ == "__main__":
    unittest.main()
