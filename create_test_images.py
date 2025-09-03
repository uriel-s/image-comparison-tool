#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create test images with controlled differences for testing the video checker
"""

import numpy as np
from PIL import Image, ImageDraw
import os

def create_test_images_with_defects():
    """
    Create reference and test images with controlled defects to test all quality grades
    """
    print("Creating test images with controlled defects...")
    
    # Ensure images directory exists
    os.makedirs('images', exist_ok=True)
    
    # Create reference image
    width, height = 800, 600
    reference = Image.new('RGB', (width, height), (50, 100, 150))  # Blue-gray background
    
    draw_ref = ImageDraw.Draw(reference)
    
    # Add colored sections to reference image
    # Top section - light blue
    draw_ref.rectangle([0, 0, width, 150], fill=(100, 150, 200))
    
    # Left section - green
    draw_ref.rectangle([0, 150, 200, height], fill=(50, 180, 80))
    
    # Right section - red
    draw_ref.rectangle([600, 150, width, height], fill=(200, 60, 70))
    
    # Center section - yellow
    draw_ref.rectangle([200, 200, 600, 400], fill=(220, 200, 50))
    
    # Add some geometric shapes
    draw_ref.ellipse([300, 250, 500, 350], fill=(150, 100, 250))  # Purple circle
    
    reference.save('images/reference_defect_test.jpg')
    print("✓ Reference image created: images/reference_defect_test.jpg")
    
    # Create test image with various types of defects
    test = reference.copy()
    draw_test = ImageDraw.Draw(test)
    
    # Type 1: Complete color change (major defect)
    draw_test.rectangle([100, 50, 200, 100], fill=(0, 0, 0))  # Black spot on light blue
    print("  Added: Major defect - black spot")
    
    # Type 2: Partial color shift (medium defect) 
    draw_test.rectangle([650, 200, 750, 300], fill=(255, 255, 255))  # White spot on red
    print("  Added: Medium defect - white spot")
    
    # Type 3: Subtle color changes (minor defects)
    draw_test.rectangle([250, 250, 300, 300], fill=(180, 130, 280))  # Slight purple change
    draw_test.rectangle([400, 280, 450, 330], fill=(170, 120, 230))  # Another slight change
    print("  Added: Minor defects - subtle color shifts")
    
    # Type 4: Noise/corruption in specific areas
    pixels = test.load()
    
    # Add noise in top-left corner
    for x in range(50, 100):
        for y in range(100, 130):
            if (x + y) % 3 == 0:  # Add noise every 3rd pixel
                r, g, b = pixels[x, y]
                pixels[x, y] = (
                    min(255, max(0, r + 60)),  # Significant red increase
                    min(255, max(0, g - 40)),  # Green decrease
                    b  # Keep blue the same
                )
    print("  Added: Noise pattern in corner")
    
    # Type 5: Line defects (simulate screen lines)
    for x in range(300, 500):
        y = 180
        pixels[x, y] = (255, 0, 255)  # Bright magenta line
        pixels[x, y + 1] = (255, 0, 255)
    print("  Added: Line defect")
    
    test.save('images/test_defect_test.jpg')
    print("✓ Test image created: images/test_defect_test.jpg")
    
    return 'images/reference_defect_test.jpg', 'images/test_defect_test.jpg'

def create_gradient_test_images():
    """
    Create images with gradient differences to test edge cases
    """
    print("\nCreating gradient test images...")
    
    width, height = 400, 300
    
    # Reference - smooth gradient
    reference = Image.new('RGB', (width, height))
    pixels_ref = reference.load()
    
    for y in range(height):
        for x in range(width):
            # Create RGB gradients
            r = int(255 * x / width)
            g = int(255 * y / height) 
            b = int(255 * (x + y) / (width + height))
            pixels_ref[x, y] = (r, g, b)
    
    reference.save('images/reference_gradient.jpg')
    
    # Test - gradient with steps/banding
    test = Image.new('RGB', (width, height))
    pixels_test = test.load()
    
    for y in range(height):
        for x in range(width):
            # Create stepped gradients (quantization artifacts)
            r = int((255 * x / width) // 32) * 32  # Quantize to 32-level steps
            g = int((255 * y / height) // 32) * 32
            b = int((255 * (x + y) / (width + height)) // 32) * 32
            pixels_test[x, y] = (r, g, b)
    
    test.save('images/test_gradient.jpg')
    print("✓ Gradient images created: reference_gradient.jpg & test_gradient.jpg")
    
    return 'images/reference_gradient.jpg', 'images/test_gradient.jpg'

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 TEST IMAGE GENERATOR")
    print("=" * 60)
    
    # Create defect test images
    ref_path1, test_path1 = create_test_images_with_defects()
    
    # Create gradient test images  
    ref_path2, test_path2 = create_gradient_test_images()
    
    print("\n" + "=" * 60)
    print("✅ Test image creation completed!")
    print("=" * 60)
    print("Image pairs created:")
    print(f"1. Defect Test: {ref_path1} vs {test_path1}")
    print(f"2. Gradient Test: {ref_path2} vs {test_path2}")
    print("\nYou can now test these with the video checker!")
