import os
import subprocess
import winreg
import sys
from typing import List
import platform

def find_python_paths() -> List[str]:
    """Find Python installation paths"""
    python_version = platform.python_version()[:3]  # Gets major.minor version (e.g., '3.12')
    possible_paths = [
        rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\Programs\Python\Python{python_version.replace('.', '')}",
        rf"C:\Python{python_version.replace('.', '')}",
        rf"C:\Program Files\Python{python_version.replace('.', '')}",
        rf"C:\Program Files (x86)\Python{python_version.replace('.', '')}"
    ]
    
    valid_paths = []
    for base_path in possible_paths:
        if os.path.exists(base_path):
            valid_paths.extend([
                base_path,
                os.path.join(base_path, 'Scripts')
            ])
    
    if not valid_paths:
        # If no paths found, use the current Python executable's location
        current_python = os.path.dirname(sys.executable)
        current_scripts = os.path.join(current_python, 'Scripts')
        valid_paths = [current_python, current_scripts]
    
    return valid_paths

def get_current_path() -> str:
    """Get the current PATH environment variable"""
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                            r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 
                            0, 
                            winreg.KEY_READ)
        path = winreg.QueryValueEx(key, 'Path')[0]
        winreg.CloseKey(key)
        return path
    except WindowsError:
        return os.environ.get('PATH', '')

def update_path_with_python() -> bool:
    """Add Python paths to system PATH if they're not already there"""
    try:
        # Get current PATH
        current_path = get_current_path()
        paths = current_path.split(';')
        
        # Get Python paths to add
        python_paths = find_python_paths()
        
        # Check which paths need to be added
        paths_to_add = [p for p in python_paths if p not in paths]
        
        if not paths_to_add:
            print(f"Python {platform.python_version()} paths are already in PATH!")
            return True
            
        # Add new paths
        new_path = current_path + ';' + ';'.join(paths_to_add)
        
        # Use setx command to update system PATH
        command = f'setx /M PATH "{new_path}"'
        
        print("Adding the following paths:")
        for path in paths_to_add:
            print(f"  - {path}")
        
        # Run command as administrator
        result = subprocess.run(command, 
                              shell=True,
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print(f"\nSuccessfully added Python {platform.python_version()} to PATH!")
            print("\nPlease restart your terminal for changes to take effect.")
            return True
        else:
            print("Failed to update PATH. Error:", result.stderr)
            return False
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    # Check if running as administrator
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
    if not is_admin:
        print("This script needs to be run as administrator!")
        print("Please run your terminal as administrator and try again.")
        sys.exit(1)
        
    print(f"Current Python version: {platform.python_version()}")
    update_path_with_python()
