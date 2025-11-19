import json
import logging
from typing import List

import pandas as pd
from colorama import Fore, Style, init
from tabulate import tabulate

from .scanner import SecretRisk

# Initialize colorama
init(autoreset=True)


class ReportGenerator:
    """
    Generates reports in various formats (Console, CSV, JSON, Markdown).
    """

    def __init__(self):
        self.logger = logging.getLogger("SPSecretBot.Reporter")

    def _to_dict_list(self, risks: List[SecretRisk]) -> List[dict]:
        return [
            {
                "Service Principal": r.sp_name,
                "App ID": r.app_id,
                "Secret Type": r.secret_type,
                "Key ID": r.secret_id,
                "Expiry Date": r.expiry_date.isoformat(),
                "Days Remaining": r.days_remaining,
                "Severity": r.severity,
            }
            for r in risks
        ]

    def print_console(self, risks: List[SecretRisk], critical_only: bool = False):
        """Prints a formatted table to the console."""
        filtered_risks = (
            [r for r in risks if r.severity in ["CRITICAL", "EXPIRED"]] if critical_only else risks
        )

        if not filtered_risks:
            print(Fore.GREEN + "\nNo risks found matching criteria." + Style.RESET_ALL)
            return

        table_data = []
        for r in filtered_risks:
            color = Fore.WHITE
            if r.severity == "EXPIRED":
                color = Fore.RED
            elif r.severity == "CRITICAL":
                color = Fore.LIGHTRED_EX
            elif r.severity == "WARNING":
                color = Fore.YELLOW
            elif r.severity == "HEALTHY":
                color = Fore.GREEN

            row = [
                r.sp_name[:30],  # Truncate for display
                r.app_id,
                r.secret_type,
                r.days_remaining,
                f"{color}{r.severity}{Style.RESET_ALL}",
            ]
            table_data.append(row)

        headers = ["Service Principal", "App ID", "Type", "Days Left", "Severity"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="simple_grid"))

    def export_csv(self, risks: List[SecretRisk], filename: str):
        data = self._to_dict_list(risks)
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        self.logger.info(f"CSV report saved to {filename}")

    def export_json(self, risks: List[SecretRisk], filename: str):
        data = self._to_dict_list(risks)
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        self.logger.info(f"JSON report saved to {filename}")

    def export_markdown(self, risks: List[SecretRisk], filename: str):
        data = self._to_dict_list(risks)
        df = pd.DataFrame(data)
        md = df.to_markdown(index=False)

        with open(filename, "w") as f:
            f.write("# Azure Service Principal Secret Expiry Report\n\n")
            f.write(f"Generated on: {pd.Timestamp.now()}\n\n")
            f.write(md)
        self.logger.info(f"Markdown report saved to {filename}")
