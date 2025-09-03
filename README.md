# 🎥 Image Comparison Tool

Professional video quality analysis tool for detecting defects in images.

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)
**Easy way:** Double-click `start.bat`

**Manual way:**
```bash
python -m streamlit run gui/streamlit_gui.py
```
Then open: http://localhost:8501

### Option 2: Interactive Terminal
```bash
python tools/interactive_tool.py
```
Step-by-step guided interface in terminal

### Option 3: Command Line
```bash
python tools/cli_tool.py images/ref_01.jpg images/test_01.jpg
```

## 🔧 Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run any of the interfaces above

## 📊 Features

- **Multiple Analysis Methods**: Strategic, Grid, Random point selection
- **Visual Results**: Charts, graphs, and comparison images
- **Report Generation**: Automatic PDF and text reports
- **Flexible Interfaces**: Web GUI, interactive terminal, and command line
- **Professional Output**: Detailed analysis with pass/fail results

## 🎯 Usage Examples

**Web Interface:**
- Upload reference and test images
- Select analysis parameters
- View interactive results
- Download reports

**Interactive Terminal:**
- Step-by-step guided process
- Choose images interactively
- Configure analysis settings
- View results in terminal

**Command Line:**
```bash
# Basic usage
python tools/cli_tool.py ref.jpg test.jpg

# With specific parameters
python tools/cli_tool.py ref.jpg test.jpg --method strategic --points 8 --threshold 30.0

# Custom points
python tools/cli_tool.py ref.jpg test.jpg --method custom --custom 100,100 200,200 300,300
```

## 📈 Analysis Methods

- **Strategic**: Focuses on important image areas
- **Grid**: Systematic grid-based sampling
- **Random**: Random point selection
- **Custom**: User-defined points

## 🎨 Results

The tool generates:
- Visual comparison charts
- Detailed analysis reports
- Pass/fail determinations
- Statistical summaries

---

## 📁 Project Structure

```
image_comparison_tool/
├── src/                          # Core source code
│   └── image_comparison_tool.py  # Main analysis engine
├── gui/                          # Graphical interfaces
│   └── streamlit_gui.py          # Web-based GUI (recommended)
├── tools/                        # Command line utilities
│   ├── cli_tool.py               # Command line interface
│   ├── interactive_tool.py       # Interactive terminal interface
│   ├── demo.py                   # Demo and examples
│   └── create_test_images.py     # Test image generator
├── images/                       # Sample images
│   ├── ref_01.jpg - ref_04.jpg   # Reference images
│   └── test_01.jpg - test_04.jpg # Test images
├── reports/                      # Analysis reports
├── requirements.txt              # Dependencies
├── start.bat                     # Easy GUI launcher (just double-click!)
└── README.md                     # This file
```

Created by: Professional Development Team
Last Updated: September 2024
