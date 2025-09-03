#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interactive demo script for video image testing system with user input
"""

import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import os
from datetime import datetime
from image_comparison_tool import ImageComparisonTool


def get_user_choice():
    """
    Get user's choice for testing method
    
    Returns:
        tuple: (method, custom_points)
    """
    print("\n" + "=" * 50)
    print("🎯 SELECT TESTING METHOD")
    print("=" * 50)
    print("1. Random - 8 random pixels")
    print("2. Grid - 8 pixels in uniform grid")
    print("3. Strategic - 8 pixels at corners and strategic points")
    print("4. Custom - You specify exact pixel locations")
    print("5. All methods - Run all 3 automatic methods")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                return 'random', None
            elif choice == '2':
                return 'grid', None
            elif choice == '3':
                return 'strategic', None
            elif choice == '4':
                return 'custom', get_custom_points()
            elif choice == '5':
                return 'all', None
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            exit()


def get_custom_points():
    """
    Get custom pixel locations from user
    
    Returns:
        list: List of (x, y) tuples
    """
    print("\n📍 CUSTOM PIXEL LOCATIONS")
    print("-" * 30)
    print("Enter 8 pixel coordinates in format: x,y")
    print("Example: 100,150")
    print("(Note: Coordinates should be within image bounds)")
    
    points = []
    for i in range(8):
        while True:
            try:
                coord_str = input(f"Point {i+1} (x,y): ").strip()
                x, y = map(int, coord_str.split(','))
                
                if x < 0 or y < 0:
                    print("❌ Coordinates must be positive numbers")
                    continue
                    
                points.append((x, y))
                break
                
            except ValueError:
                print("❌ Invalid format. Use: x,y (example: 100,150)")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                exit()
    
    return points


def get_number_of_points():
    """
    Ask user how many test points they want (default 8)
    
    Returns:
        int: Number of test points
    """
    while True:
        try:
            choice = input("\nHow many test points? (1-20, default 8): ").strip()
            if not choice:
                return 8
            
            num = int(choice)
            if 1 <= num <= 20:
                return num
            else:
                print("❌ Please enter a number between 1 and 20")
                
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            exit()


def get_image_paths():
    """
    Get image paths from user - either existing files or create samples
    
    Returns:
        tuple: (reference_path, test_path)
    """
    print("\n📸 SELECT IMAGES TO COMPARE")
    print("=" * 40)
    print("1. Use existing sample images (auto-generated)")
    print("2. Specify your own image files")
    print("3. Browse and select from images/ folder")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                # Create or use existing sample images
                ref_path = "images/reference_image.jpg"
                test_path = "images/test_image.jpg"
                
                if os.path.exists(ref_path) and os.path.exists(test_path):
                    print("✅ Using existing sample images")
                    return ref_path, test_path
                else:
                    print("Creating new sample images...")
                    return create_sample_images()
                    
            elif choice == '2':
                # Get custom file paths
                return get_custom_image_paths()
                
            elif choice == '3':
                # Browse images folder
                return browse_images_folder()
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            exit()


def get_custom_image_paths():
    """
    Get custom image file paths from user
    
    Returns:
        tuple: (reference_path, test_path)
    """
    print("\n📁 SPECIFY IMAGE FILE PATHS")
    print("-" * 30)
    print("Enter full paths to your images:")
    
    while True:
        try:
            ref_path = input("Reference image path (good image): ").strip()
            if not ref_path:
                print("❌ Reference path cannot be empty")
                continue
                
            if not os.path.exists(ref_path):
                print(f"❌ File not found: {ref_path}")
                continue
                
            # Check if it's an image file
            valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
            if not any(ref_path.lower().endswith(ext) for ext in valid_extensions):
                print(f"❌ Invalid image format. Supported: {', '.join(valid_extensions)}")
                continue
                
            break
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            exit()
    
    while True:
        try:
            test_path = input("Test image path (image to check): ").strip()
            if not test_path:
                print("❌ Test path cannot be empty")
                continue
                
            if not os.path.exists(test_path):
                print(f"❌ File not found: {test_path}")
                continue
                
            # Check if it's an image file
            if not any(test_path.lower().endswith(ext) for ext in valid_extensions):
                print(f"❌ Invalid image format. Supported: {', '.join(valid_extensions)}")
                continue
                
            break
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            exit()
    
    print(f"✅ Selected images:")
    print(f"   📁 Reference: {ref_path}")
    print(f"   📁 Test: {test_path}")
    
    return ref_path, test_path


def browse_images_folder():
    """
    Browse and select images from the images/ folder
    
    Returns:
        tuple: (reference_path, test_path)
    """
    print("\n📂 BROWSE IMAGES FOLDER")
    print("-" * 30)
    
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print("❌ No images/ folder found. Created empty folder.")
        print("Please add your images to the images/ folder and try again.")
        return get_image_paths()
    
    # Get all image files in images folder
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_files = []
    
    for file in os.listdir(images_dir):
        if any(file.lower().endswith(ext) for ext in valid_extensions):
            image_files.append(file)
    
    if not image_files:
        print("❌ No image files found in images/ folder.")
        print("Please add your images and try again.")
        return get_image_paths()
    
    print(f"Found {len(image_files)} image file(s):")
    for i, file in enumerate(image_files, 1):
        file_path = os.path.join(images_dir, file)
        file_size = os.path.getsize(file_path)
        print(f"{i:2d}. {file} ({file_size // 1024} KB)")
    
    # Select reference image
    while True:
        try:
            ref_choice = input(f"\nSelect reference image (1-{len(image_files)}): ").strip()
            ref_idx = int(ref_choice) - 1
            
            if 0 <= ref_idx < len(image_files):
                ref_path = os.path.join(images_dir, image_files[ref_idx])
                break
            else:
                print(f"❌ Invalid choice. Please enter 1-{len(image_files)}")
                
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            exit()
    
    # Select test image
    while True:
        try:
            test_choice = input(f"Select test image (1-{len(image_files)}): ").strip()
            test_idx = int(test_choice) - 1
            
            if 0 <= test_idx < len(image_files):
                test_path = os.path.join(images_dir, image_files[test_idx])
                break
            else:
                print(f"❌ Invalid choice. Please enter 1-{len(image_files)}")
                
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            exit()
    
    print(f"✅ Selected images:")
    print(f"   📁 Reference: {ref_path}")
    print(f"   📁 Test: {test_path}")
    
    return ref_path, test_path


def create_sample_images():
    """
    Create sample images for testing
    
    Returns:
        tuple: Paths to reference and test images
    """
    print("Creating sample images for demonstration...")
    
    # Create reference image
    width, height = 800, 600
    reference = Image.new('RGB', (width, height), (100, 150, 200))
    
    # Add shapes to reference image
    draw = ImageDraw.Draw(reference)
    
    # Colored rectangles
    draw.rectangle([100, 100, 200, 200], fill=(255, 0, 0))    # Red
    draw.rectangle([300, 150, 400, 250], fill=(0, 255, 0))    # Green
    draw.rectangle([500, 200, 600, 300], fill=(0, 0, 255))    # Blue
    draw.rectangle([200, 350, 350, 450], fill=(255, 255, 0))  # Yellow
    
    # Circles
    draw.ellipse([50, 400, 150, 500], fill=(255, 0, 255))     # Magenta
    draw.ellipse([600, 100, 700, 200], fill=(0, 255, 255))    # Cyan
    
    reference.save('images/reference_image.jpg')
    
    # Create test image with defects
    test = reference.copy()
    draw_test = ImageDraw.Draw(test)
    
    # Add "defects" - corrupted pixels
    draw_test.rectangle([120, 120, 140, 140], fill=(0, 0, 0))      # Black hole
    draw_test.rectangle([320, 170, 340, 190], fill=(255, 255, 255)) # White spot
    draw_test.rectangle([520, 220, 540, 240], fill=(128, 128, 128)) # Gray spot
    
    # Add noise at specific points
    pixels = test.load()
    noise_points = [(150, 150), (350, 200), (550, 250), (250, 400), (100, 450)]
    
    for x, y in noise_points:
        # Add random noise
        r, g, b = pixels[x, y]
        pixels[x, y] = (
            min(255, max(0, r + np.random.randint(-50, 51))),
            min(255, max(0, g + np.random.randint(-50, 51))),
            min(255, max(0, b + np.random.randint(-50, 51)))
        )
    
    test.save('images/test_image.jpg')
    print("✅ Sample images created successfully!")
    print(f"   📁 Reference: images/reference_image.jpg ({width}x{height})")
    print(f"   📁 Test: images/test_image.jpg ({width}x{height})")
    
    return 'images/reference_image.jpg', 'images/test_image.jpg'


def run_interactive_demo():
    """
    Run interactive demonstration of the video image checking system
    """
    print("=" * 70)
    print("🎥 VIDEO IMAGE CHECKER - INTERACTIVE MODE")
    print("=" * 70)
    
    # Create directories if they don't exist
    os.makedirs('images', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Get image paths from user
    ref_path, test_path = get_image_paths()
    
    # Get user preferences for testing method
    method, custom_points = get_user_choice()
    
    if method != 'custom':
        num_points = get_number_of_points()
    else:
        num_points = len(custom_points)
    
    # Ask about saving options
    print("\n💾 OUTPUT OPTIONS")
    print("-" * 20)
    save_viz = input("Save visualization chart? (y/n, default y): ").strip().lower()
    save_viz = save_viz not in ['n', 'no']
    
    save_report = input("Save text report? (y/n, default y): ").strip().lower()
    save_report = save_report not in ['n', 'no']
    
    # Run the analysis
    print("\n🔍 STARTING ANALYSIS...")
    print("=" * 30)
    
    checker = ImageComparisonTool(ref_path, test_path)
    
    if method == 'all':
        # Run all methods
        methods = ['strategic', 'grid', 'random']
        for test_method in methods:
            print(f"\n📊 Running analysis with '{test_method}' method...")
            checker.run_full_analysis(
                num_points=num_points, 
                method=test_method, 
                save_visualization=save_viz, 
                save_report=save_report
            )
    elif method == 'custom':
        # Use custom points
        print(f"\n📍 Running analysis with custom points: {custom_points}")
        checker.load_images()
        checker.test_points = custom_points
        checker.compare_pixels()
        
        # Generate outputs
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if save_viz:
            vis_path = f"reports/custom_visualization_{timestamp}.png"
            checker.visualize_comparison(vis_path)
        else:
            checker.visualize_comparison()
        
        if save_report:
            report_path = f"reports/custom_report_{timestamp}.txt"
            checker.generate_report(report_path)
        
        # Print summary
        significant_count = sum(1 for r in checker.comparison_results if r['is_significant'])
        pass_rate = ((len(checker.comparison_results) - significant_count) / 
                    len(checker.comparison_results) * 100)
        
        print(f"\n✅ Custom analysis completed!")
        print(f"📊 Pass rate: {pass_rate:.1f}%")
        print(f"🏆 Result: {'PASS' if pass_rate >= 75 else 'FAIL'}")
        
    else:
        # Run single method
        print(f"\n📊 Running analysis with '{method}' method...")
        checker.run_full_analysis(
            num_points=num_points, 
            method=method, 
            custom_points=custom_points,
            save_visualization=save_viz, 
            save_report=save_report
        )
    
    print("\n" + "=" * 50)
    print("✅ ANALYSIS COMPLETED!")
    
    if save_viz or save_report:
        print("📁 Output files saved in 'reports/' directory")
    
    print("\n🔄 Run the script again to test different images or methods!")


if __name__ == "__main__":
    try:
        run_interactive_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Please check your input and try again.")
