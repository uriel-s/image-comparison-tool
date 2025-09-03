# Image Comparison Tool - Visual Defect Analysis

## Project Description

A Python tool for comparing two images to detect visual differences and defects.

Perfect for:

- 📸 Quality control - comparing before/after images
- 🔍 Defect detection - finding differences between images
- 📊 Analysis reports - getting detailed comparison results

The system compares:

- **Reference Image** - A known good image serving as the standard
- **Test Image** - An image being tested for defects

## Key Features

✅ Compare 8 pixels at different locations on the image  
✅ Support for color images (RGB)  
✅ Four test point selection methods (strategic/grid/random/custom)  
✅ Graphical visualization of results  
✅ Detailed reports with recommendations

## System Requirements

- Python 3.7+
- Python packages (see requirements.txt)

## Quick Start (Choose One)

🚀 **For beginners - Auto Demo:**

```bash
python demo.py
```

🎯 **For interactive use:**

```bash
python interactive_demo.py
```

💻 **For command line:**

```bash
python run_checker.py reference.jpg test.jpg
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Images

Place images in the `images/` directory:

- `reference_image.jpg` - Reference image
- `test_image.jpg` - Test image

## Detailed Usage Options

### 1. Auto Demo

```bash
python demo.py
```

Creates sample images and runs analysis with all 3 methods (strategic/grid/random).

### 2. Interactive Mode

```bash
python interactive_demo.py
```

Full control: choose images, methods, points, and output options.

### 3. Command Line Interface

```bash
# Basic usage
python run_checker.py reference.jpg test.jpg

# With specific options
python run_checker.py ref.jpg test.jpg --method strategic --threshold 25.0 --quiet
```

## Test Point Selection Methods

| Method         | Description           | Best For               |
| -------------- | --------------------- | ---------------------- |
| `strategic` ⭐ | Corners + key points  | Hardware validation    |
| `grid`         | Uniform coverage      | Overall quality check  |
| `random`       | Random sampling       | Unbiased testing       |
| `custom`       | User-specified points | Specific problem areas |

### Command Line Examples:

```bash
# Strategic (recommended)
python run_checker.py ref.jpg test.jpg --method strategic

# Custom points
python run_checker.py ref.jpg test.jpg --custom 100,100 200,200 300,300
```

## Getting Started

### Option 1: Try the Demo (Easiest) 🚀

```bash
python demo.py  # Creates sample images automatically
```

### Option 2: Use Your Images 🖼️

Place your images in `images/` folder or specify full paths. **Supported formats:** JPG, PNG, BMP, TIFF

### Option 3: Interactive Mode (Recommended) 🎯

```bash
python interactive_demo.py  # Choose everything step by step
```

## What You Get

### 📊 Visual Report

- Side-by-side image comparison
- Test points marked with color coding (🟢 pass / 🔴 fail)
- Bar chart of differences
- Summary table

### 📄 Text Report

Detailed analysis with:

- Pass/fail rate and overall grade
- Pixel-by-pixel RGB values and differences
- Recommendations based on quality level

## Understanding Results

### Significance Threshold

The default value **30** is used as threshold for significant defect (configurable via `--threshold` parameter):

- **< 30**: Small difference, likely normal
- **≥ 30**: Significant difference, possible defect

### Quality Grading System

The system uses a 4-tier quality assessment:

- 🌟 **EXCELLENT** (95%+ pass rate): No significant defects, suitable for production
- ✅ **GOOD** (87.5%+ pass rate): Minor defects within acceptable limits
- ⚠️ **ACCEPTABLE** (75%+ pass rate): Some defects detected, consider monitoring
- ❌ **FAIL** (< 75% pass rate): Significant defects, immediate action required

### Configurable Parameters

All thresholds can be customized by modifying constants in `video_checker.py`:

```python
# Defect detection sensitivity
DEFAULT_SIGNIFICANCE_THRESHOLD = 30.0  # Lower = more sensitive

# Quality grade thresholds (pass rate percentages)
EXCELLENT_THRESHOLD = 95.0    # 95%+ pass rate = EXCELLENT
GOOD_THRESHOLD = 87.5         # 87.5%+ pass rate = GOOD
ACCEPTABLE_THRESHOLD = 75.0   # 75%+ pass rate = ACCEPTABLE
```

## Project Structure

```
image_comparison_tool/
├── image_comparison_tool.py  # ⭐ Main analysis class
├── demo.py                  # 🚀 Auto demonstration  
├── interactive_demo.py      # 🎯 Interactive interface
├── run_checker.py           # 💻 Command line interface
├── simple_demo.py           # 📝 Simple example
├── create_test_images.py    # 🖼️ Test image generator
├── requirements.txt         # 📦 Dependencies
├── README.md               # 📖 This guide
├── images/                 # 🖼️ Input images
│   ├── reference_*.jpg
│   └── test_*.jpg
└── reports/                # 📊 Analysis outputs
    └── analysis_[timestamp]_[method]/
        ├── comparison_report.txt
        └── comparison_visualization.png
```## Troubleshooting

### Image Loading Error

```
Error: Cannot load images - check file paths
```

**Solution**: Verify images exist and are in supported format (JPG, PNG, BMP)

### Different Image Sizes

The system supports images of different sizes, but using same-sized images is recommended for more accurate results.

l use.
