#!/usr/bin/env python3
"""
Simple test script for Kid Cam Game PC
Tests basic functionality without requiring a camera
"""

import pygame
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import pygame
        print("✅ Pygame imported successfully")
    except ImportError as e:
        print(f"❌ Pygame import failed: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import mediapipe
        print("✅ MediaPipe imported successfully")
    except ImportError as e:
        print(f"❌ MediaPipe import failed: {e}")
        return False
    
    try:
        from src.utils.camera import CameraManager
        print("✅ CameraManager imported successfully")
    except ImportError as e:
        print(f"❌ CameraManager import failed: {e}")
        return False
    
    try:
        from src.ui.main_menu import MainMenu
        print("✅ MainMenu imported successfully")
    except ImportError as e:
        print(f"❌ MainMenu import failed: {e}")
        return False
    
    try:
        from src.game_manager import GameManager
        print("✅ GameManager imported successfully")
    except ImportError as e:
        print(f"❌ GameManager import failed: {e}")
        return False
    
    try:
        from src.games.face_fun import FaceFunGame
        from src.games.color_hunt import ColorHuntGame
        from src.games.motion_magic import MotionMagicGame
        print("✅ All game modules imported successfully")
    except ImportError as e:
        print(f"❌ Game modules import failed: {e}")
        return False
    
    return True

def test_pygame_init():
    """Test pygame initialization"""
    print("\n🧪 Testing Pygame initialization...")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test Window")
        print("✅ Pygame initialized successfully")
        
        # Test basic drawing
        screen.fill((100, 150, 200))
        pygame.draw.circle(screen, (255, 255, 255), (400, 300), 50)
        pygame.display.flip()
        
        print("✅ Basic drawing test passed")
        
        # Clean up
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Pygame test failed: {e}")
        return False

def test_menu_creation():
    """Test main menu creation"""
    print("\n🧪 Testing menu creation...")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((1024, 768))
        
        from src.ui.main_menu import MainMenu
        menu = MainMenu(screen)
        
        print("✅ MainMenu created successfully")
        
        # Test menu drawing
        menu.update()
        menu.draw()
        pygame.display.flip()
        
        print("✅ Menu drawing test passed")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Menu test failed: {e}")
        return False

def test_camera_manager():
    """Test camera manager (without actual camera)"""
    print("\n🧪 Testing camera manager...")
    
    try:
        from src.utils.camera import CameraManager
        camera = CameraManager()
        
        print("✅ CameraManager created successfully")
        
        # Test initialization (will fail without camera, but shouldn't crash)
        result = camera.initialize()
        if result:
            print("✅ Camera initialized (camera detected)")
            camera.cleanup()
        else:
            print("⚠️ Camera not available (expected in test environment)")
        
        return True
        
    except Exception as e:
        print(f"❌ Camera manager test failed: {e}")
        return False

def run_visual_test():
    """Run a visual test of the menu"""
    print("\n🎮 Running visual test...")
    print("A window should open showing the game menu.")
    print("Press any key or close the window to continue.")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Kid Cam Game PC - Visual Test")
        clock = pygame.time.Clock()
        
        from src.ui.main_menu import MainMenu
        menu = MainMenu(screen)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    selected = menu.handle_click(event.pos)
                    if selected:
                        print(f"✅ Button click detected: {selected}")
                        running = False
            
            menu.update()
            screen.fill((135, 206, 235))
            menu.draw()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        print("✅ Visual test completed")
        return True
        
    except Exception as e:
        print(f"❌ Visual test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎮 Kid Cam Game PC - Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Pygame Test", test_pygame_init),
        ("Menu Test", test_menu_creation),
        ("Camera Test", test_camera_manager),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The game should work correctly.")
        
        # Ask if user wants to run visual test
        try:
            response = input("\n🎨 Would you like to run the visual test? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                run_visual_test()
        except KeyboardInterrupt:
            print("\n👋 Test suite interrupted by user")
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
