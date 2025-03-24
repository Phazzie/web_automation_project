import os
import shutil
import subprocess
from typing import Tuple

def get_python_path() -> str:
    """Get the correct Python executable path"""
    if os.name == 'nt':  # Windows
        return os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe')
    return os.path.join(os.getcwd(), '.venv', 'bin', 'python')

def run_command(cmd: list[str]) -> Tuple[bool, str]:
    """Run a command and return success status and output"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        return True, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def create_gitignore() -> None:
    """Create .gitignore file with appropriate contents"""
    gitignore_content = """# Python virtual environment
.venv/
venv/
ENV/

# Python byte-compiled files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/

# IDE settings
.idea/
.vscode/
*.swp
*.swo

# Environment variables
.env

# Logs
*.log

# Test cache
.pytest_cache/
.coverage
htmlcov/

# System files
.DS_Store
Thumbs.db
"""
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)

def setup_git() -> None:
    """Set up Git repository from scratch"""
    print("Starting Git setup...")
    
    # Remove existing .git directory if it exists
    if os.path.exists(".git"):
        print("Removing existing .git directory...")
        shutil.rmtree(".git", ignore_errors=True)
    
    # Initialize commands
    print("Initializing Git repository...")
    commands = [
        ["git", "init"],
        ["git", "config", "--local", "user.name", "phazzie"],
        ["git", "config", "--local", "user.email", "phazziezee@gmail.com"],
    ]
    
    # Create and add .gitignore
    print("Creating .gitignore...")
    create_gitignore()
    
    print("Adding project files...")
    commands.extend([
        ["git", "add", ".gitignore"],
        ["git", "add", "README.md"],
        ["git", "add", "MVP_ROADMAP.md"],
        ["git", "add", "REFACTORING_GUIDE.md"],
        ["git", "add", "REFACTORING_STATUS.md"],
        ["git", "add", "app.py"],
        ["git", "add", "tools/*.py"],
    ])
    
    # Execute commands
    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        success, output = run_command(cmd)
        if not success:
            print(f"Error running {' '.join(cmd)}: {output}")
            return
        if output:
            print(output)
    
    # Show status
    print("\nChecking Git status...")
    success, status = run_command(["git", "status"])
    if success:
        print("\nCurrent status:")
        print(status)
    
    print("\nGit setup complete!")

if __name__ == "__main__":
    setup_git()
