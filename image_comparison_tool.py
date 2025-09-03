import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import random
from typing import List, Tuple, Dict, Any

# Configuration Constants
DEFAULT_SIGNIFICANCE_THRESHOLD = 30.0  # RGB Euclidean distance threshold for significant defects

# Quality Grade Thresholds (pass rate percentages)
# To modify quality standards, change these values:
EXCELLENT_THRESHOLD = 95.0    # 95%+ pass rate = EXCELLENT
GOOD_THRESHOLD = 87.5         # 87.5%+ pass rate = GOOD  
ACCEPTABLE_THRESHOLD = 75.0   # 75%+ pass rate = ACCEPTABLE
# Below 75% = FAIL

# Quality Grade Names
GRADE_EXCELLENT = "EXCELLENT"
GRADE_GOOD = "GOOD"
GRADE_ACCEPTABLE = "ACCEPTABLE"
GRADE_FAIL = "FAIL"


class ImageComparisonTool:
    """
    Class for checking and comparing images for visual defects and differences
    """
    
    def __init__(self, reference_image_path: str, test_image_path: str):
        """
        Initialize the VideoImageChecker
        
        Args:
            reference_image_path: Path to reference (good) image
            test_image_path: Path to test image (potentially defective)
        """
        self.reference_image_path = reference_image_path
        self.test_image_path = test_image_path
        self.reference_image = None
        self.test_image = None
        self.test_points = []
        self.comparison_results = []
        self.significance_threshold = DEFAULT_SIGNIFICANCE_THRESHOLD  # Configurable threshold
        
    def set_significance_threshold(self, threshold: float):
        """
        Set the significance threshold for defect detection
        
        Args:
            threshold: RGB Euclidean distance threshold (default: 30.0)
        """
        if threshold <= 0:
            raise ValueError("Threshold must be positive")
        self.significance_threshold = threshold
        print(f"Significance threshold set to: {threshold}")
        
    def get_significance_threshold(self) -> float:
        """
        Get the current significance threshold
        
        Returns:
            Current threshold value
        """
        return self.significance_threshold
        
    def load_images(self) -> bool:
        """
        Load both images into memory
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load images in color format
            self.reference_image = cv2.imread(self.reference_image_path, cv2.IMREAD_COLOR)
            self.test_image = cv2.imread(self.test_image_path, cv2.IMREAD_COLOR)
            
            if self.reference_image is None or self.test_image is None:
                print("Error: Cannot load images - check file paths")
                return False
                
            # Convert BGR to RGB for proper matplotlib display
            self.reference_image = cv2.cvtColor(self.reference_image, cv2.COLOR_BGR2RGB)
            self.test_image = cv2.cvtColor(self.test_image, cv2.COLOR_BGR2RGB)
            
            print(f"Reference image loaded: {self.reference_image.shape}")
            print(f"Test image loaded: {self.test_image.shape}")
            
            return True
            
        except Exception as e:
            print(f"Error loading images: {e}")
            return False
    
    def generate_test_points(self, num_points: int = 8, method: str = 'random', custom_points: list = None) -> List[Tuple[int, int]]:
        """
        Generate test points on the image for pixel comparison
        
        Args:
            num_points: Number of test points to generate (default: 8)
            method: Method for point selection ('random', 'grid', 'strategic', 'custom')
            custom_points: List of (x,y) tuples for custom method
            
        Returns:
            List of (x, y) coordinate tuples
        """
        if self.reference_image is None:
            print("Error: Reference image not loaded")
            return []
            
        height, width = self.reference_image.shape[:2]
        points = []
        
        if method == 'custom' and custom_points:
            # Use user-provided custom points
            valid_points = []
            for x, y in custom_points:
                if 0 <= x < width and 0 <= y < height:
                    valid_points.append((x, y))
                else:
                    print(f"Warning: Point ({x},{y}) is outside image bounds ({width}x{height}), skipping")
            points = valid_points
            
        elif method == 'random':
            # Generate random points with margin from edges
            for _ in range(num_points):
                x = random.randint(10, width - 10)
                y = random.randint(10, height - 10)
                points.append((x, y))
                
        elif method == 'grid':
            # Generate points in a uniform grid pattern
            cols = int(np.sqrt(num_points))
            rows = int(np.ceil(num_points / cols))
            
            for i in range(rows):
                for j in range(cols):
                    if len(points) >= num_points:
                        break
                    x = int((j + 1) * width / (cols + 1))
                    y = int((i + 1) * height / (rows + 1))
                    points.append((x, y))
                    
        elif method == 'strategic':
            # Test corners and strategic central points
            margin = 50
            candidate_points = [
                (margin, margin),                       # Top-left corner (with margin)
                (width - margin, margin),               # Top-right corner (with margin)
                (margin, height - margin),              # Bottom-left corner (with margin)
                (width - margin, height - margin),      # Bottom-right corner (with margin)
                (width // 2, height // 2),              # Center point
                (width // 4, height // 4),              # Upper-left quarter
                (3 * width // 4, height // 4),          # Upper-right quarter
                (width // 2, 3 * height // 4)           # Lower center
            ]
            points = candidate_points[:num_points]
            
        self.test_points = points
        print(f"Generated {len(points)} test points using '{method}' method")
        return points
    
    def compare_pixels(self) -> List[Dict[str, Any]]:
        """
        Compare RGB values at test points between reference and test images
        
        Returns:
            List of dictionaries containing comparison results for each point
        """
        if not self.test_points:
            print("Error: No test points generated")
            return []
            
        if self.reference_image is None or self.test_image is None:
            print("Error: Images not loaded")
            return []
            
        results = []
        
        for i, (x, y) in enumerate(self.test_points):
            # Extract RGB values at test point
            ref_pixel = self.reference_image[y, x]
            test_pixel = self.test_image[y, x]
            
            # Calculate per-channel differences
            r_diff = int(test_pixel[0]) - int(ref_pixel[0])
            g_diff = int(test_pixel[1]) - int(ref_pixel[1])
            b_diff = int(test_pixel[2]) - int(ref_pixel[2])
            
            # Calculate Euclidean distance (total difference)
            total_diff = np.sqrt(r_diff**2 + g_diff**2 + b_diff**2)
            
            # Create result dictionary
            result = {
                'point_id': i + 1,
                'coordinates': (x, y),
                'reference_rgb': tuple(map(int, ref_pixel)),
                'test_rgb': tuple(map(int, test_pixel)),
                'rgb_difference': (r_diff, g_diff, b_diff),
                'total_difference': total_diff,
                'is_significant': total_diff > self.significance_threshold  # Use configurable threshold
            }
            
            results.append(result)
            
        self.comparison_results = results
        print(f"Compared {len(results)} pixel points")
        return results
    
    def _calculate_quality_grade(self, pass_rate: float) -> tuple[str, str]:
        """
        Calculate quality grade and description based on pass rate
        
        Args:
            pass_rate: Pass rate percentage (0-100)
            
        Returns:
            tuple: (grade, description)
        """
        if pass_rate >= EXCELLENT_THRESHOLD:
            return GRADE_EXCELLENT, "No significant pixel defects detected. Image is suitable for production use."
        elif pass_rate >= GOOD_THRESHOLD:
            return GRADE_GOOD, "Minor pixel defects detected but within acceptable limits. Image quality is good."
        elif pass_rate >= ACCEPTABLE_THRESHOLD:
            return GRADE_ACCEPTABLE, "Some pixel defects detected but still within acceptable range. Consider monitoring."
        else:
            return GRADE_FAIL, "Significant pixel defects detected. Image quality is below acceptable standards."
    
    def visualize_comparison(self, save_path: str = None):
        """
        Create visual comparison of images with test points and results
        
        Args:
            save_path: Optional path to save the visualization
        """
        if self.reference_image is None or self.test_image is None:
            print("Error: Images not loaded for visualization")
            return
            
        if not self.comparison_results:
            print("Error: No comparison results to visualize")
            return
            
        # Create 2x2 subplot layout
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Video Image Quality Comparison Report', fontsize=16, fontweight='bold')
        
        # Plot 1: Reference image with test points
        axes[0, 0].imshow(self.reference_image)
        axes[0, 0].set_title('Reference Image (Good Quality)', fontsize=12)
        axes[0, 0].axis('off')
        
        # Mark test points on reference image
        for i, (x, y) in enumerate(self.test_points):
            axes[0, 0].plot(x, y, 'go', markersize=8)
            axes[0, 0].annotate(f'{i+1}', (x, y), xytext=(5, 5), 
                              textcoords='offset points', color='white', 
                              fontweight='bold', fontsize=10)
        
        # Plot 2: Test image with colored test points
        axes[0, 1].imshow(self.test_image)
        axes[0, 1].set_title('Test Image (Under Analysis)', fontsize=12)
        axes[0, 1].axis('off')
        
        # Mark test points with color coding (red = significant difference)
        for i, (x, y) in enumerate(self.test_points):
            color = 'ro' if self.comparison_results[i]['is_significant'] else 'go'
            axes[0, 1].plot(x, y, color, markersize=8)
            axes[0, 1].annotate(f'{i+1}', (x, y), xytext=(5, 5), 
                              textcoords='offset points', color='white', 
                              fontweight='bold', fontsize=10)
        
        # Plot 3: Bar chart of differences
        point_labels = [f'P{i+1}' for i in range(len(self.comparison_results))]
        differences = [result['total_difference'] for result in self.comparison_results]
        
        colors = ['red' if d > self.significance_threshold else 'green' for d in differences]
        bars = axes[1, 0].bar(point_labels, differences, color=colors, alpha=0.7)
        axes[1, 0].set_title('Pixel Difference Values', fontsize=12)
        axes[1, 0].set_ylabel('Total RGB Difference')
        axes[1, 0].set_xlabel('Test Points')
        axes[1, 0].axhline(y=self.significance_threshold, color='orange', linestyle='--', 
                          label=f'Significance Threshold ({self.significance_threshold})', linewidth=2)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, diff in zip(bars, differences):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 1,
                          f'{diff:.1f}', ha='center', va='bottom', fontsize=9)
        
        # Plot 4: Summary table
        axes[1, 1].axis('tight')
        axes[1, 1].axis('off')
        
        # Create summary table data
        table_data = []
        for result in self.comparison_results:
            status = "FAIL" if result['is_significant'] else "PASS"
            table_data.append([
                f"P{result['point_id']}",
                f"({result['coordinates'][0]}, {result['coordinates'][1]})",
                f"{result['total_difference']:.1f}",
                status
            ])
        
        # Add summary row
        significant_count = sum(1 for r in self.comparison_results if r['is_significant'])
        pass_rate = ((len(self.comparison_results) - significant_count) / 
                    len(self.comparison_results) * 100)
        
        table_data.append(["", "", "", ""])  # Separator row
        table_data.append(["SUMMARY", f"{significant_count} failures", 
                          f"{pass_rate:.1f}% pass", 
                          "PASS" if pass_rate >= 75 else "FAIL"])
        
        table = axes[1, 1].table(cellText=table_data,
                               colLabels=['Point', 'Location (X,Y)', 'Difference', 'Status'],
                               cellLoc='center',
                               loc='center',
                               cellColours=None)
        
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.8)
        axes[1, 1].set_title('Test Results Summary', fontsize=12)
        
        # Color code the summary row
        for i in range(4):
            if len(table_data) > len(self.comparison_results) + 1:
                table[(len(table_data), i)].set_facecolor('#f0f0f0')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to: {save_path}")
        
        # Close the figure to free memory
        plt.close()
    
    def generate_report(self, output_path: str = None) -> str:
        """
        Generate detailed text report of the comparison
        
        Args:
            output_path: Optional path to save the report file
            
        Returns:
            String containing the full report
        """
        if not self.comparison_results:
            return "No comparison results available"
            
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("VIDEO IMAGE QUALITY COMPARISON REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Reference Image: {os.path.basename(self.reference_image_path)}")
        report_lines.append(f"Test Image: {os.path.basename(self.test_image_path)}")
        report_lines.append("")
        
        # Executive Summary
        significant_failures = sum(1 for result in self.comparison_results 
                                 if result['is_significant'])
        total_points = len(self.comparison_results)
        pass_rate = ((total_points - significant_failures) / total_points) * 100
        
        report_lines.append("EXECUTIVE SUMMARY:")
        report_lines.append("-" * 40)
        report_lines.append(f"Total test points: {total_points}")
        report_lines.append(f"Points with significant defects: {significant_failures}")
        report_lines.append(f"Points passed: {total_points - significant_failures}")
        report_lines.append(f"Pass rate: {pass_rate:.1f}%")
        
        # Calculate quality grade
        grade, description = self._calculate_quality_grade(pass_rate)
        report_lines.append(f"Overall result: {grade}")
        report_lines.append("")
        
        # Detailed Results
        report_lines.append("DETAILED PIXEL ANALYSIS:")
        report_lines.append("-" * 80)
        
        for result in self.comparison_results:
            status = "FAIL (Significant defect)" if result['is_significant'] else "PASS"
            report_lines.append(f"Test Point {result['point_id']}:")
            report_lines.append(f"  Location (X,Y): ({result['coordinates'][0]}, {result['coordinates'][1]})")
            report_lines.append(f"  Reference RGB: {result['reference_rgb']}")
            report_lines.append(f"  Test RGB: {result['test_rgb']}")
            report_lines.append(f"  RGB Differences (R,G,B): {result['rgb_difference']}")
            report_lines.append(f"  Total Difference: {result['total_difference']:.2f}")
            report_lines.append(f"  Status: {status}")
            report_lines.append("")
        
        # Technical Details
        report_lines.append("TECHNICAL DETAILS:")
        report_lines.append("-" * 40)
        report_lines.append(f"Difference calculation: Euclidean distance in RGB space")
        report_lines.append(f"Significance threshold: {self.significance_threshold} (differences >= {self.significance_threshold} are flagged)")
        report_lines.append(f"Test point selection method: {getattr(self, '_last_method', 'unknown')}")
        report_lines.append("")
        
        # Recommendations
        report_lines.append("RECOMMENDATIONS:")
        report_lines.append("-" * 40)
        grade, description = self._calculate_quality_grade(pass_rate)
        
        # Add quality indicator icon
        if grade == GRADE_EXCELLENT:
            report_lines.append("✓ IMAGE QUALITY: EXCELLENT")
        elif grade == GRADE_GOOD:
            report_lines.append("✓ IMAGE QUALITY: GOOD")
        elif grade == GRADE_ACCEPTABLE:
            report_lines.append("⚠ IMAGE QUALITY: ACCEPTABLE")
        else:
            report_lines.append("✗ IMAGE QUALITY: FAIL")
            
        report_lines.append(f"  {description}")
        
        # Add specific recommendations based on grade
        if grade == GRADE_EXCELLENT:
            report_lines.append("  Recommended action: Continue with current process.")
        elif grade == GRADE_GOOD:
            report_lines.append("  Recommended action: Monitor quality trends.")
        elif grade == GRADE_ACCEPTABLE:
            report_lines.append("  Recommended action: Investigate potential causes and implement improvements.")
        else:
            report_lines.append("  Recommended action: Review and correct the imaging process immediately.")
            report_lines.append("  Significant pixel defects detected.")
            report_lines.append("  Immediate investigation and correction required.")
            report_lines.append("  Do not use for production without fixes.")
        
        report_text = "\n".join(report_lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"Report saved to: {output_path}")
        
        return report_text
    
    def run_full_analysis(self, num_points: int = 8, method: str = 'random', 
                         custom_points: list = None, save_visualization: bool = True, 
                         save_report: bool = True):
        """
        Run complete image comparison analysis
        
        Args:
            num_points: Number of test points (default: 8)
            method: Point selection method ('random', 'grid', 'strategic', 'custom')
            custom_points: List of (x,y) tuples for custom method
            save_visualization: Whether to save visualization chart
            save_report: Whether to save text report
        """
        print("Starting Video Image Quality Analysis...")
        print("=" * 50)
        
        # Store method for reporting
        self._last_method = method
        
        # Step 1: Load images
        if not self.load_images():
            print("❌ Analysis failed: Could not load images")
            return
        
        # Step 2: Generate test points
        self.generate_test_points(num_points, method, custom_points)
        if not self.test_points:
            print("❌ Analysis failed: Could not generate test points")
            return
        
        # Step 3: Compare pixels
        self.compare_pixels()
        if not self.comparison_results:
            print("❌ Analysis failed: Could not compare pixels")
            return
        
        # Step 4: Generate outputs
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create organized directory structure
        session_folder = f"reports/analysis_{timestamp}_{method}"
        os.makedirs(session_folder, exist_ok=True)
        
        # Create visualization
        if save_visualization:
            vis_path = f"{session_folder}/comparison_visualization_{timestamp}.png"
            self.visualize_comparison(vis_path)
        else:
            self.visualize_comparison()
        
        # Generate text report
        if save_report:
            report_path = f"{session_folder}/comparison_report_{timestamp}.txt"
            self.generate_report(report_path)
        
        # Print summary
        significant_count = sum(1 for r in self.comparison_results if r['is_significant'])
        pass_rate = ((len(self.comparison_results) - significant_count) / 
                    len(self.comparison_results) * 100)
        
        print("\n" + "=" * 50)
        print("ANALYSIS COMPLETE")
        print("=" * 50)
        print(f"✅ Test points analyzed: {len(self.comparison_results)}")
        print(f"{'❌' if significant_count > 0 else '✅'} Defects found: {significant_count}")
        print(f"📊 Pass rate: {pass_rate:.1f}%")
        
        # Use new quality grading system
        grade, description = self._calculate_quality_grade(pass_rate)
        grade_icons = {
            GRADE_EXCELLENT: "🌟",
            GRADE_GOOD: "✅", 
            GRADE_ACCEPTABLE: "⚠️",
            GRADE_FAIL: "❌"
        }
        print(f"{grade_icons.get(grade, '🏆')} Overall result: {grade}")
        
        if save_visualization or save_report:
            print(f"\n📁 Files saved in '{session_folder}/' directory")


if __name__ == "__main__":
    # Example usage
    print("Video Image Checker - Hardware Component Testing")
    print("=" * 50)
    
    # Define image paths
    reference_path = "images/ref_01.jpg"
    test_path = "images/test_01.jpg"
    
    # Check if images exist
    if os.path.exists(reference_path) and os.path.exists(test_path):
        # Create checker instance
        checker = VideoImageChecker(reference_path, test_path)
        
        # Run analysis with corner-based testing (recommended for hardware validation)
        checker.run_full_analysis(
            num_points=8, 
            method='strategic',
            save_visualization=True, 
            save_report=True
        )
    else:
        print("📝 Setup required:")
        print("   1. Place reference image at: images/ref_01.jpg")
        print("   2. Place test image at: images/test_01.jpg")
        print("   3. Run this script again")
        print("\nAlternatively, run demo.py to see system with sample images.")
