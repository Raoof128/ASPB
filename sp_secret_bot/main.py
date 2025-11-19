import argparse
import logging
import sys
from typing import List

from dotenv import load_dotenv

from .azure_client import AzureClient
from .report import ReportGenerator
from .scanner import SecretRisk, SecretScanner
from .utils import setup_logging


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Azure Service Principal Secret Expiry Bot")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan for expiring secrets")
    scan_parser.add_argument(
        "--format",
        choices=["json", "csv", "markdown", "table"],
        default="table",
        help="Output format",
    )
    scan_parser.add_argument("--output", help="Output file path (e.g., report.csv)")
    scan_parser.add_argument(
        "--critical-only",
        action="store_true",
        help="Only show expired or critical secrets (<= 30 days)",
    )
    scan_parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    return parser.parse_args()


def run_scan(args: argparse.Namespace, logger: logging.Logger) -> None:
    """Executes the scan logic."""
    client = AzureClient()
    if not client.authenticate():
        logger.error("Authentication failed. Exiting.")
        sys.exit(1)

    sps = client.get_all_service_principals()
    scanner = SecretScanner()
    risks: List[SecretRisk] = scanner.scan_service_principals(sps)

    if args.critical_only:
        risks = [r for r in risks if r.severity in ["CRITICAL", "EXPIRED"]]

    reporter = ReportGenerator()

    # Always print to console if format is table or no output file is specified
    if args.format == "table" or not args.output:
        reporter.print_console(risks, critical_only=False)

    if args.output:
        if args.format == "csv" or args.output.endswith(".csv"):
            reporter.export_csv(risks, args.output)
        elif args.format == "json" or args.output.endswith(".json"):
            reporter.export_json(risks, args.output)
        elif args.format == "markdown" or args.output.endswith(".md"):
            reporter.export_markdown(risks, args.output)
        else:
            logger.warning("Unknown output format inferred. Defaulting to CSV.")
            reporter.export_csv(risks, args.output)


def main() -> None:
    """Main entry point."""
    # Load environment variables from .env file if present
    load_dotenv()

    args = parse_args()

    if not args.command:
        print("Error: No command specified.\n")
        parse_args().print_help()  # This is a bit hacky to show help, but works
        sys.exit(1)

    logger = setup_logging(args.verbose)

    if args.command == "scan":
        run_scan(args, logger)


if __name__ == "__main__":
    main()
