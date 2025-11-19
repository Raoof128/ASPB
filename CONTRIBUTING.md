# Contributing to Azure Service Principal Secret Bot

Thank you for your interest in contributing! We welcome bug reports, feature requests, and pull requests.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/sp-secret-bot.git
   cd sp-secret-bot
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   make install
   ```

## Code Standards

We enforce high code quality standards. Before submitting a PR, please run:

```bash
make format
make lint
make test
```

- **Formatting**: We use `black` and `isort`.
- **Type Hinting**: All code must be fully typed and pass `mypy`.
- **Testing**: New features must include unit tests.

## Pull Request Process

1. Create a new branch for your feature (`git checkout -b feature/amazing-feature`).
2. Commit your changes with clear messages.
3. Push to the branch.
4. Open a Pull Request.
5. Ensure CI checks pass.

## Reporting Bugs

Please use the GitHub Issue Tracker to report bugs. Include:
- Steps to reproduce
- Expected vs actual behavior
- Environment details
