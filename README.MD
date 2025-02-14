# Spark AI Workflow Project

## Project Overview
Spark is an advanced AI workflow management system designed to create flexible, extensible AI-powered workflows.

## Features
- Modular AI model registry
- Workflow type management
- Async-first architecture
- Comprehensive logging
- Extensible phase-based execution

## Prerequisites
- Python 3.10+
- pip
- virtualenv (recommended)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/spark-ai-workflow.git
cd spark-ai-workflow
```

### 2. Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Database Configuration
DB_NAME=spark_db
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run the Project
```bash
# Run the main application
python main.py

# Optional: Specify log level
python main.py --log-level DEBUG
```

### 6. Running Tests
```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_models/
```

## Project Structure
- `ai/`: AI model implementations
- `core/`: Core system components
  - `registries/`: Model and workflow registries
  - `timeline/`: Execution tracking
- `tests/`: Test suite

## Development Tools
- Code Formatting: `black .`
- Import Sorting: `isort .`
- Type Checking: `mypy .`

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Specify your license]

## Contact
[Your contact information]
