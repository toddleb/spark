"""
~/prizym/spark/scripts/1_setup_spark.py
Creates basic file structure and environment
"""

import os
import sys
import subprocess
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(os.path.expanduser("~/prizym/spark"))

# Directory structure
DIRECTORIES = {
    "ai": {
        "models": {},
        "router": {},
        "utils": {}
    },
    "core": {
        "registries": {},
        "loopback": {},
        "timeline": {},
        "security": {}
    },
    "generators": {},
    "templates": {
        "backend": {
            "fastapi": {},
            "database": {}
        },
        "frontend": {
            "nextjs": {},
            "react": {}
        }
    },
    "tests": {
        "test_models": {},
        "test_router": {},
        "test_generators": {}
    }
}

def create_structure(base_path: Path, structure: dict):
    """Create directory structure"""
    for name, substructure in structure.items():
        path = base_path / name
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {path}")
        
        # Create __init__.py
        init_file = path / "__init__.py"
        init_file.touch()
        print(f"Created file: {init_file}")
        
        if substructure:
            create_structure(path, substructure)

def setup_virtual_environment():
    """Create and configure virtual environment"""
    venv_path = PROJECT_ROOT / "venv"
    
    # Create venv if it doesn't exist
    if not venv_path.exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("Created virtual environment")
    
    # Determine pip path
    pip_path = str(venv_path / "bin" / "pip") if os.name != "nt" else str(venv_path / "Scripts" / "pip")
    
    # Install required packages
    requirements = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "asyncpg",
        "python-dotenv",
        "langchain-openai",
        "anthropic",
        "pytest",
        "pytest-asyncio"
    ]
    
    for package in requirements:
        subprocess.run([pip_path, "install", package], check=True)
        print(f"Installed {package}")

def create_env_file():
    """Create .env file with default settings"""
    env_content = """# Database configuration
DB_NAME=spark_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# AI API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
MIXTRAL_API_KEY=your_mixtral_key
"""
    
    env_file = PROJECT_ROOT / ".env"
    env_file.write_text(env_content)
    print("Created .env file")

def main():
    """Main setup function"""
    print("🚀 Starting environment setup...")
    
    # Create project structure
    print("\nCreating directory structure...")
    create_structure(PROJECT_ROOT, DIRECTORIES)
    
    # Setup virtual environment
    print("\nSetting up virtual environment...")
    setup_virtual_environment()
    
    # Create .env file
    print("\nCreating environment file...")
    create_env_file()
    
    print("\n✅ Environment setup complete!")
    print("\nNext steps:")
    print("1. Update .env with your credentials")
    print("2. Run the code setup script: python 2_setup_code.py")
    print("3. Run the test setup script: python 3_setup_tests.py")

if __name__ == "__main__":
    main()
