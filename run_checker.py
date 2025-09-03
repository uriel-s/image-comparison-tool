#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command-line interface for video image checker
Usage examples:
  python run_checker.py ref.jpg test.jpg
  python run_checker.py ref.jpg test.jpg --method strategic --points 8
  python run_checker.py ref.jpg test.jpg --custom 100,100 200,200 300,300
"""

import argparse
import sys
import os
from image_comparison_tool import ImageComparisonTool


def parse_custom_points(point_strings):
    """
    Parse custom point coordinates from command line
    
    Args:
        point_strings: List of strings in format "x,y"
        
    Returns:
        List of (x,y) tuples
    """
    points = []
    for point_str in point_strings:
        try:
            x, y = map(int, point_str.split(','))
            points.append((x, y))
        except ValueError:
            print(f"❌ Invalid point format: {point_str}. Use format: x,y")
            sys.exit(1)
    return points


def main():
    """
    Main command line interface
    """
    parser = argparse.ArgumentParser(
        description="Video Image Checker - Compare images for defects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s reference.jpg test.jpg
  %(prog)s reference.jpg test.jpg --method strategic --points 8
  %(prog)s reference.jpg test.jpg --method grid --no-save
  %(prog)s ref.jpg test.jpg --custom 100,100 200,200 300,300 400,400
        """
    )
    
    # Required arguments
    parser.add_argument('reference', help='Path to reference (good) image')
    parser.add_argument('test', help='Path to test image to check')
    
    # Optional arguments
    parser.add_argument('--method', '-m', 
                       choices=['random', 'grid', 'strategic', 'custom'],
                       default='strategic',
                       help='Test point selection method (default: strategic)')
    
    parser.add_argument('--points', '-p', type=int, default=8,
                       help='Number of test points (must be 8 for assignment compliance, default: 8)')
    
    parser.add_argument('--custom', nargs='+', metavar='X,Y',
                       help='Custom point coordinates (format: x,y x,y ...)')
    
    parser.add_argument('--no-save', action='store_true',
                       help="Don't save visualization and report files")
    
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Quiet mode - minimal output')
    
    parser.add_argument('--threshold', '-t', type=float, default=30.0,
                       help='Significance threshold for defects (default: 30.0)')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.reference):
        print(f"❌ Reference image not found: {args.reference}")
        sys.exit(1)
        
    if not os.path.exists(args.test):
        print(f"❌ Test image not found: {args.test}")
        sys.exit(1)
    
    # Handle custom points
    custom_points = None
    if args.method == 'custom':
        if not args.custom:
            print("❌ Custom method requires --custom points")
            sys.exit(1)
        custom_points = parse_custom_points(args.custom)
        args.points = len(custom_points)
    elif args.custom:
        print("⚠️  --custom specified but method is not 'custom', ignoring custom points")
    
    # Validate point count - must be exactly 8 for assignment requirements
    if args.points != 8 and not args.custom:
        print("⚠️  Assignment requires exactly 8 test points. Using 8 points instead.")
        args.points = 8
    
    if not args.quiet:
        print("🎥 Video Image Checker - Command Line Mode")
        print("=" * 50)
        print(f"📁 Reference: {args.reference}")
        print(f"📁 Test: {args.test}")
        print(f"🎯 Method: {args.method}")
        print(f"📍 Points: {args.points}")
        if custom_points:
            print(f"📌 Custom points: {custom_points}")
        print(f"⚖️  Threshold: {args.threshold}")
    
    # Create checker and run analysis
    try:
        checker = ImageComparisonTool(args.reference, args.test)
        
        # Set custom threshold if specified
        if hasattr(checker, 'set_significance_threshold'):
            checker.set_significance_threshold(args.threshold)
        
        # Run analysis
        checker.run_full_analysis(
            num_points=args.points,
            method=args.method,
            custom_points=custom_points,
            save_visualization=not args.no_save,
            save_report=not args.no_save
        )
        
        # Print results summary
        if not args.quiet and checker.comparison_results:
            significant_count = sum(1 for r in checker.comparison_results 
                                  if r['is_significant'])
            pass_rate = ((len(checker.comparison_results) - significant_count) / 
                        len(checker.comparison_results) * 100)
            
            print("\n" + "=" * 50)
            print("📊 FINAL SUMMARY")
            print("=" * 50)
            print(f"Total points tested: {len(checker.comparison_results)}")
            print(f"Significant defects: {significant_count}")
            print(f"Pass rate: {pass_rate:.1f}%")
            print(f"Overall result: {'✅ PASS' if pass_rate >= 75 else '❌ FAIL'}")
            
            if not args.no_save:
                print(f"\n📁 Reports saved in 'reports/' directory")
        
    except Exception as e:
        if not args.quiet:
            print(f"❌ Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
