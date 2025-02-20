# 🚀 FastAPI UV Workspace Template

A modern, production-ready template for building scalable Python applications with FastAPI, GraphQL, and UV package manager.

## ✨ Features

- **📦 UV Package Management**: Modern, fast Python package management
- **🏗️ Workspace Structure**: Monorepo setup with multiple packages
- **🔍 Type Safety**: Full mypy type checking integration
- **🧪 Testing**: Pytest setup with coverage reporting
- **📊 GraphQL**: Strawberry GraphQL integration
- **🐳 Docker**: Production-ready containerization
- **🔄 CI/CD**: GitHub Actions workflow ready
- **📝 Code Quality**: Ruff for linting and formatting

## 🏛️ Project Structure

```
.
├── app/                    # Main FastAPI application
│   └── main.py            # Application entry point
├── packages/              # Workspace packages
│   └── crawler/           # Example crawler package
├── docker/                # Docker configuration
├── .venv/                 # Virtual environment (UV managed)
├── pyproject.toml         # Project configuration
├── uv.lock               # UV lock file
└── Makefile              # Development commands
```

## 🛠️ Tech Stack

- **FastAPI**: Modern web framework
- **UV**: Fast Python package manager
- **Strawberry**: GraphQL framework
- **Docker**: Containerization
- **Pytest**: Testing framework
- **Mypy**: Static type checking
- **Ruff**: Fast Python linter
- **Make**: Build automation

## 🚦 Getting Started

### Prerequisites

- Python 3.13+
- Docker
- Make

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fastapi-uv-workspace

# Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
make install
```

### Development Commands

```bash
# Start development server
make up

# Run tests
make run-tests

# Type checking
make type-check

# Format code
make format

# Build Docker image
make build
```

## 📋 API Examples

### GraphQL API

```graphql
# Query domains
query {
    getDomains
}

# Response
{
    "data": {
        "getDomains": ["domain1", "domain2"]
    }
}
```

### REST API

```bash
# Health check
curl http://localhost:8000/health
```

## 🏗️ Workspace Management

### Adding New Packages

1. Create new directory in `packages/`
2. Add package configuration:

```toml
# packages/newpackage/pyproject.toml
[project]
name = "newpackage"
version = "0.1.0"
dependencies = []
```

3. Update root `pyproject.toml`:

```toml
[tool.uv.packages]
newpackage = { path = "packages/newpackage" }
```

## 🐳 Docker

```bash
# Build and run
docker compose up --build

# Production build
docker build -t fastapi-app:prod .
```

## 📝 Configuration

### UV Settings

```toml
# pyproject.toml
[tool.uv]
python = "3.13"
```

## 🧪 Testing

```bash
# Run all tests with coverage
make run-tests

# Test specific package
cd packages/crawler && pytest
```

## 📚 Best Practices

- Use type hints everywhere
- Follow PEP 8 style guide
- Write tests for new features
- Keep packages focused and minimal
- Document public APIs

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📜 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- FastAPI team
- Astral (UV) team
- Strawberry GraphQL team

---
Built with ❤️ using FastAPI and UV
