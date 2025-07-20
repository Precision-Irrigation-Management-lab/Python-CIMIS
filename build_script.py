#!/usr/bin/env python3
"""
Build and deployment script for the Python CIMIS Client library.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"🔨 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ {description} failed!")
        print(f"Error: {result.stderr}")
        return False
    else:
        print(f"✅ {description} completed successfully!")
        if result.stdout.strip():
            print(f"Output: {result.stdout}")
        return True


def clean_build_dirs():
    """Clean build directories."""
    print("🧹 Cleaning build directories...")
    
    dirs_to_clean = ['build', 'dist', 'python_cimis.egg-info']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    print("✅ Build directories cleaned!")


def install_build_dependencies():
    """Install build dependencies."""
    return run_command(
        "pip install --upgrade pip setuptools wheel build twine",
        "Installing build dependencies"
    )


def run_tests():
    """Run the test suite."""
    if not os.path.exists("tests"):
        print("⚠️  No tests directory found, skipping tests")
        return True
    
    print("🧪 Running tests...")
    
    # Install pytest if not available
    subprocess.run("pip install pytest", shell=True, capture_output=True)
    
    return run_command("python -m pytest tests/ -v", "Running test suite")


def build_package():
    """Build the package."""
    return run_command("python -m build", "Building package")


def check_package():
    """Check the built package."""
    return run_command("python -m twine check dist/*", "Checking package")


def upload_to_testpypi():
    """Upload to TestPyPI."""
    print("\n📦 Uploading to TestPyPI...")
    print("Note: You'll need to enter your TestPyPI credentials")
    
    return run_command(
        "python -m twine upload --repository testpypi dist/*",
        "Uploading to TestPyPI"
    )


def upload_to_pypi():
    """Upload to PyPI."""
    print("\n📦 Uploading to PyPI...")
    print("Note: You'll need to enter your PyPI credentials")
    
    response = input("Are you sure you want to upload to PyPI? (y/N): ")
    if response.lower() != 'y':
        print("❌ PyPI upload cancelled")
        return False
    
    return run_command(
        "python -m twine upload dist/*",
        "Uploading to PyPI"
    )


def install_locally():
    """Install the package locally for testing."""
    return run_command("pip install -e .", "Installing package locally")


def main():
    """Main build script."""
    print("🚀 Python CIMIS Client - Build Script")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        print("Available commands:")
        print("  clean       - Clean build directories")
        print("  deps        - Install build dependencies")
        print("  test        - Run tests")
        print("  build       - Build package")
        print("  check       - Check package")
        print("  local       - Install locally for development")
        print("  testpypi    - Upload to TestPyPI")
        print("  pypi        - Upload to PyPI")
        print("  all         - Run full build process")
        print("\nUsage: python build_script.py <command>")
        return
    
    if command == "clean":
        clean_build_dirs()
        
    elif command == "deps":
        install_build_dependencies()
        
    elif command == "test":
        run_tests()
        
    elif command == "build":
        if not build_package():
            sys.exit(1)
            
    elif command == "check":
        if not check_package():
            sys.exit(1)
            
    elif command == "local":
        if not install_locally():
            sys.exit(1)
            
    elif command == "testpypi":
        if not upload_to_testpypi():
            sys.exit(1)
            
    elif command == "pypi":
        if not upload_to_pypi():
            sys.exit(1)
            
    elif command == "all":
        steps = [
            (clean_build_dirs, "Clean build directories"),
            (install_build_dependencies, "Install build dependencies"),
            (run_tests, "Run tests"),
            (lambda: build_package(), "Build package"),
            (lambda: check_package(), "Check package"),
        ]
        
        print("🔄 Running full build process...")
        
        for step_func, step_name in steps:
            result = step_func()
            if result is False:
                print(f"❌ Build process failed at: {step_name}")
                sys.exit(1)
            result = step_func()
            if result is False:
                print(f"❌ Build process failed at: {step_name}")
                sys.exit(1)
        
        print("\n🎉 Build process completed successfully!")
        print("\nNext steps:")
        print("  - Test the package: python build_script.py local")
        print("  - Upload to TestPyPI: python build_script.py testpypi")
        print("  - Upload to PyPI: python build_script.py pypi")
        
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
