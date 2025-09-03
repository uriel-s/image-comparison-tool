#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Streamlit GUI for Image Comparison Tool
A web-based graphical interface for comparing images and detecting defects.

Usage:
    streamlit run streamlit_gui.py

Features:
- Upload reference and test images
- Select analysis method (strategic/grid/random/custom)
- Adjust significance threshold  
- View results with interactive charts
- Download reports
"""

import streamlit as st
import tempfile
import os
import shutil
from datetime import datetime
import base64
from PIL import Image
import pandas as pd
import sys

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from image_comparison_tool import ImageComparisonTool

def main():
    # Page configuration
    st.set_page_config(
        page_title="Image Comparison Tool",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title and description
    st.title("🔍 Image Comparison Tool")
    st.markdown("**Professional visual defect detection with RGB pixel analysis**")
    st.markdown("---")
    
    # Sidebar for controls
    st.sidebar.header("⚙️ Configuration")
    
    # Analysis method selection
    method = st.sidebar.selectbox(
        "🎯 Analysis Method",
        ["strategic", "grid", "random", "custom"],
        index=0,
        help="Strategic: corners + key points, Grid: uniform coverage, Random: unbiased sampling"
    )
    
    # Threshold adjustment
    threshold = st.sidebar.slider(
        "⚖️ Significance Threshold",
        min_value=10.0,
        max_value=100.0,
        value=30.0,
        step=5.0,
        help="Lower values = more sensitive detection"
    )
    
    # Number of test points
    num_points = st.sidebar.number_input(
        "📍 Number of Test Points",
        min_value=8,
        max_value=20,
        value=8,
        help="Must be at least 8 points for assignment compliance"
    )
    
    # Custom points input (if custom method selected)
    custom_points = None
    if method == "custom":
        st.sidebar.subheader("📌 Custom Points")
        st.sidebar.markdown("Enter coordinates as: x1,y1 x2,y2 x3,y3...")
        custom_input = st.sidebar.text_area(
            "Custom Points (space-separated)",
            placeholder="100,100 200,200 300,300 400,400 500,500 600,600 700,700 800,800",
            help="Enter exactly 8 coordinate pairs"
        )
        
        if custom_input.strip():
            try:
                points = []
                pairs = custom_input.strip().split()
                for pair in pairs:
                    x, y = map(int, pair.split(','))
                    points.append((x, y))
                custom_points = points[:8]  # Limit to 8 points
                st.sidebar.success(f"✅ {len(custom_points)} custom points loaded")
            except:
                st.sidebar.error("❌ Invalid format. Use: x,y x,y x,y...")
    
    # Main content area
    col1, col2 = st.columns(2)
    
    # File upload section
    with col1:
        st.subheader("📸 Reference Image")
        ref_file = st.file_uploader(
            "Upload reference (good) image",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            key="ref_upload",
            help="The known good image to compare against"
        )
        
        if ref_file:
            ref_image = Image.open(ref_file)
            st.image(ref_image, caption=f"Reference: {ref_file.name}", use_column_width=True)
    
    with col2:
        st.subheader("🔬 Test Image")
        test_file = st.file_uploader(
            "Upload test image",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            key="test_upload",
            help="The image to be tested for defects"
        )
        
        if test_file:
            test_image = Image.open(test_file)
            st.image(test_image, caption=f"Test: {test_file.name}", use_column_width=True)
    
    # Analysis section
    st.markdown("---")
    
    if ref_file and test_file:
        # Analysis button
        if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
            run_analysis(ref_file, test_file, method, threshold, num_points, custom_points)
    else:
        st.info("👆 Please upload both reference and test images to begin analysis")
    
    # Information section
    st.markdown("---")
    with st.expander("ℹ️ About This Tool"):
        st.markdown("""
        ### How It Works:
        1. **Upload Images**: Select reference (good) and test images
        2. **Choose Method**: Pick how to select test points on the images
        3. **Set Threshold**: Adjust sensitivity for defect detection
        4. **Run Analysis**: Compare RGB values at selected pixel locations
        5. **Review Results**: See visual comparison and detailed report
        
        ### Analysis Methods:
        - **Strategic** ⭐: Tests corners and key points (recommended for hardware)
        - **Grid**: Uniform coverage across the image
        - **Random**: Unbiased random sampling
        - **Custom**: User-defined pixel locations
        
        ### Quality Grades:
        - 🌟 **EXCELLENT** (95%+ pass rate): No significant defects
        - ✅ **GOOD** (87.5%+ pass rate): Minor defects within limits
        - ⚠️ **ACCEPTABLE** (75%+ pass rate): Some defects detected
        - ❌ **FAIL** (<75% pass rate): Significant defects found
        """)


def run_analysis(ref_file, test_file, method, threshold, num_points, custom_points):
    """Run the image comparison analysis"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Create temporary files
        status_text.text("📁 Preparing files...")
        progress_bar.progress(10)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            ref_path = os.path.join(temp_dir, "reference.jpg")
            test_path = os.path.join(temp_dir, "test.jpg")
            
            with open(ref_path, "wb") as f:
                f.write(ref_file.getbuffer())
            with open(test_path, "wb") as f:
                f.write(test_file.getbuffer())
            
            progress_bar.progress(30)
            
            # Initialize analyzer
            status_text.text("🔧 Initializing analyzer...")
            checker = ImageComparisonTool(ref_path, test_path)
            checker.set_significance_threshold(threshold)
            
            progress_bar.progress(50)
            
            # Run analysis
            status_text.text("🔍 Analyzing images...")
            checker.run_full_analysis(
                num_points=num_points,
                method=method,
                custom_points=custom_points,
                save_visualization=True,
                save_report=True
            )
            
            progress_bar.progress(80)
            
            # Display results
            status_text.text("📊 Displaying results...")
            display_results(checker)
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        st.error("Please check your images and try again.")


def display_results(checker):
    """Display analysis results"""
    
    if not checker.comparison_results:
        st.error("No results to display")
        return
    
    # Calculate summary statistics
    significant_count = sum(1 for r in checker.comparison_results if r['is_significant'])
    total_points = len(checker.comparison_results)
    pass_rate = ((total_points - significant_count) / total_points) * 100
    
    # Get quality grade
    grade, description = checker._calculate_quality_grade(pass_rate)
    
    # Display summary
    st.subheader("📈 Analysis Results")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Test Points", total_points)
    with col2:
        st.metric("Defects Found", significant_count)
    with col3:
        st.metric("Pass Rate", f"{pass_rate:.1f}%")
    with col4:
        grade_emoji = {"EXCELLENT": "🌟", "GOOD": "✅", "ACCEPTABLE": "⚠️", "FAIL": "❌"}
        st.metric("Overall Grade", f"{grade_emoji.get(grade, '🏆')} {grade}")
    
    # Results table
    st.subheader("📋 Detailed Results")
    
    # Create DataFrame for better display
    df_data = []
    for result in checker.comparison_results:
        df_data.append({
            "Point": f"P{result['point_id']}",
            "Location (X,Y)": f"({result['coordinates'][0]}, {result['coordinates'][1]})",
            "Reference RGB": str(result['reference_rgb']),
            "Test RGB": str(result['test_rgb']),
            "Difference": f"{result['total_difference']:.1f}",
            "Status": "❌ FAIL" if result['is_significant'] else "✅ PASS"
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True)
    
    # Quality assessment
    st.subheader("🎯 Quality Assessment")
    grade_colors = {"EXCELLENT": "green", "GOOD": "blue", "ACCEPTABLE": "orange", "FAIL": "red"}
    st.markdown(f"**{grade_emoji.get(grade, '🏆')} Overall Result: {grade}**")
    st.info(description)
    
    # Find and display visualization
    reports_dir = "reports"
    if os.path.exists(reports_dir):
        # Find the latest report directory
        subdirs = [d for d in os.listdir(reports_dir) if os.path.isdir(os.path.join(reports_dir, d))]
        if subdirs:
            latest_dir = max(subdirs)
            viz_files = [f for f in os.listdir(os.path.join(reports_dir, latest_dir)) if f.endswith('.png')]
            
            if viz_files:
                viz_path = os.path.join(reports_dir, latest_dir, viz_files[0])
                st.subheader("📊 Visual Analysis")
                st.image(viz_path, caption="Detailed Comparison Chart", use_column_width=True)
                
                # Download button for visualization
                with open(viz_path, "rb") as file:
                    btn = st.download_button(
                        label="📥 Download Visualization",
                        data=file.read(),
                        file_name=f"comparison_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png"
                    )
            
            # Download button for text report
            txt_files = [f for f in os.listdir(os.path.join(reports_dir, latest_dir)) if f.endswith('.txt')]
            if txt_files:
                txt_path = os.path.join(reports_dir, latest_dir, txt_files[0])
                with open(txt_path, "r", encoding="utf-8") as file:
                    report_content = file.read()
                    st.download_button(
                        label="📥 Download Text Report",
                        data=report_content,
                        file_name=f"comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )


if __name__ == "__main__":
    main()
