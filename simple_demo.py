#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple demo - basic functionality test with minimal dependencies
"""

import os
from PIL import Image, ImageDraw
from image_comparison_tool import ImageComparisonTool


def create_simple_test_images():
    """Create simple test images for basic demonstration"""
    print("Creating simple test images...")
    
    # Create reference image
    width, height = 400, 300
    reference = Image.new('RGB', (width, height), (100, 150, 200))
    
    # Add simple shapes
    draw = ImageDraw.Draw(reference)
    draw.rectangle([50, 50, 100, 100], fill=(255, 0, 0))    # Red square
    draw.rectangle([150, 100, 200, 150], fill=(0, 255, 0))  # Green square
    draw.rectangle([250, 150, 300, 200], fill=(0, 0, 255))  # Blue square
    
    reference.save('images/ref_simple.jpg')
    
    # Create test image with defects
    test = reference.copy()
    draw_test = ImageDraw.Draw(test)
    
    # Add defects
    draw_test.rectangle([60, 60, 80, 80], fill=(0, 0, 0))      # Black spot
    draw_test.rectangle([160, 110, 180, 130], fill=(255, 255, 255))  # White spot
    
    test.save('images/test_simple.jpg')
    print("✅ Simple test images created!")
    
    return 'images/ref_simple.jpg', 'images/test_simple.jpg'


def run_simple_demo():
    """Run a basic demonstration of the video checker"""
    print("=" * 50)
    print("🎮 SIMPLE VIDEO CHECKER DEMO")
    print("=" * 50)
    
    try:
        # Create test images
        ref_path, test_path = create_simple_test_images()
        
        # Run basic analysis
        print("\n🔍 Running basic analysis...")
        checker = ImageComparisonTool(ref_path, test_path)
        
        # Test with strategic method only
        checker.run_full_analysis(
            num_points=4, 
            method='strategic',
            save_visualization=True, 
            save_report=True
        )
        
        print("\n✅ Simple demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure all dependencies are installed.")


if __name__ == "__main__":
    os.makedirs('images', exist_ok=True)
    run_simple_demo()
