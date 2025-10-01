# GUI
Practice GUI with PyQt6

## Description
A basic PyQt6 application demonstrating:
- **Threading**: Background tasks using QThread without blocking the UI
- **Multiple Layouts**: QVBoxLayout, QHBoxLayout, and QGridLayout
- **Interactive Elements**: Buttons, input fields, progress bars, and text displays

## Requirements
- Python 3.8+
- PyQt6

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kimho912/GUI.git
cd GUI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

## Features

### Multiple Layouts
- **Horizontal Layout**: Row of buttons demonstrating QHBoxLayout
- **Grid Layout**: 3x3 grid of buttons with input field demonstrating QGridLayout
- **Vertical Layout**: Main container organizing all sections using QVBoxLayout

### Threading
- Start background tasks that run in separate threads
- Progress bar showing task completion
- Start/Stop controls for task management
- Non-blocking UI during task execution

### Interactive Elements
- Click buttons to log messages
- Enter custom task names in the input field
- Monitor task progress in real-time
- View timestamped status logs
