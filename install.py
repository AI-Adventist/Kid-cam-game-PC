#!/usr/bin/env python3
"""
Installation script for Kid Cam Game PC
Helps users install dependencies and set up the game
"""

import subprocess
import sys
import os
import platform

def print_header():
    """Print welcome header"""
    print("🎮📷 Kid Cam Game PC - Installation Script")
    print("=" * 50)
    print("This script will help you install the game and its dependencies.")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python {version.major}.{version.minor} is not supported.")
        print("   Please install Python 3.7 or newer.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def check_pip():
    """Check if pip is available"""
    print("\n📦 Checking pip...")
    
    try:
        import pip
        print("✅ pip is available!")
        return True
    except ImportError:
        print("❌ pip is not available.")
        print("   Please install pip first.")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n📥 Installing dependencies...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    try:
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print("❌ Failed to install dependencies:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_camera():
    """Check if camera is available"""
    print("\n📷 Checking camera availability...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("✅ Camera detected and accessible!")
            cap.release()
            return True
        else:
            print("⚠️ Camera not detected or not accessible.")
            print("   The game will still run, but camera features won't work.")
            return False
            
    except ImportError:
        print("⚠️ OpenCV not available for camera test.")
        return False
    except Exception as e:
        print(f"⚠️ Camera test failed: {e}")
        return False

def run_test():
    """Run the test script"""
    print("\n🧪 Running tests...")
    
    if not os.path.exists("test_game.py"):
        print("⚠️ test_game.py not found, skipping tests.")
        return True
    
    try:
        result = subprocess.run([sys.executable, "test_game.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only for now)"""
    if platform.system() != "Windows":
        return
    
    print("\n🖥️ Creating desktop shortcut...")
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Kid Cam Game PC.lnk")
        target = os.path.join(os.getcwd(), "main.py")
        wDir = os.getcwd()
        icon = target
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        
        print("✅ Desktop shortcut created!")
        
    except ImportError:
        print("⚠️ Cannot create shortcut (winshell not available)")
    except Exception as e:
        print(f"⚠️ Could not create shortcut: {e}")

def print_instructions():
    """Print final instructions"""
    print("\n" + "=" * 50)
    print("🎉 Installation Complete!")
    print()
    print("To start the game:")
    print("  python main.py")
    print()
    print("Or run the test first:")
    print("  python test_game.py")
    print()
    print("Game Controls:")
    print("  • ESC - Exit games or quit")
    print("  • SPACE - Pause/Resume")
    print("  • Mouse - Navigate menus")
    print()
    print("Make sure your camera is connected and working!")
    print("Have fun playing! 🎮📷")

def main():
    """Main installation process"""
    print_header()
    
    # Check system requirements
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Install dependencies
    print("\n" + "=" * 30)
    response = input("📥 Install dependencies now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        if not install_dependencies():
            print("❌ Installation failed!")
            return False
    else:
        print("⚠️ Skipping dependency installation.")
        print("   You can install them later with: pip install -r requirements.txt")
    
    # Check camera
    check_camera()
    
    # Run tests
    print("\n" + "=" * 30)
    response = input("🧪 Run tests now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        run_test()
    
    # Create shortcut (Windows only)
    if platform.system() == "Windows":
        response = input("🖥️ Create desktop shortcut? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            create_desktop_shortcut()
    
    # Final instructions
    print_instructions()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Installation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Installation error: {e}")
        print("Please try installing manually with: pip install -r requirements.txt")
