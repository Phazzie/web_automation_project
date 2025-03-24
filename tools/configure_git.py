import subprocess
from typing import Tuple
import sys

def run_git_command(args: list[str]) -> Tuple[bool, str]:
    """Run a git command and return success status and output"""
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False
        )
        return True, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def configure_git() -> None:
    """Configure git with user details"""
    # Set user name
    success, output = run_git_command([
        'git', 'config', '--global', 'user.name', 'Phazzie'  # Corrected capitalization
    ])
    if not success:
        print(f"Failed to set user name: {output}")
        sys.exit(1)

    # Set user email
    success, output = run_git_command([
        'git', 'config', '--global', 'user.email', 'phazziezee@gmail.com'
    ])
    if not success:
        print(f"Failed to set user email: {output}")
        sys.exit(1)

    # Verify configuration
    success, name = run_git_command(['git', 'config', '--global', 'user.name'])
    success, email = run_git_command(['git', 'config', '--global', 'user.email'])
    
    print(f"""Git configuration successful:
User Name: {name}
User Email: {email}""")

if __name__ == "__main__":
    configure_git()
