#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple demo script for video image testing system
"""

import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import os
from image_comparison_tool import ImageComparisonTool


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
    # Change colors in several locations
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
    print("Sample images created successfully!")
    
    return 'images/reference_image.jpg', 'images/test_image.jpg'


def run_demo():
    """
    Run demonstration of the video image checking system
    """
    print("=" * 60)
    print("🎥 Video Image Checker - DEMONSTRATION")
    print("=" * 60)
    
    # Create directories if they don't exist
    os.makedirs('images', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Create sample images
    ref_path, test_path = create_sample_images()
    
    # Run the tests
    print("\n🔍 Starting image analysis...")
    checker = ImageComparisonTool(ref_path, test_path)
    
    # Test with different methods
    methods = ['strategic', 'grid', 'random']
    
    for method in methods:
        print(f"\n📊 Testing with '{method}' method...")
        checker.run_full_analysis(
            num_points=8, 
            method=method, 
            save_visualization=True, 
            save_report=True
        )
    
    print("\n✅ Demonstration completed!")
    print("📁 Reports and visualizations saved in 'reports/' directory")


if __name__ == "__main__":
    run_demo()
