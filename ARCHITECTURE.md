# Application Structure

## main.py - PyQt6 Application

### Architecture

```
MainWindow (QMainWindow)
├── Central Widget
    └── QVBoxLayout (main_layout)
        ├── Title Label
        ├── Horizontal Section (QWidget with QHBoxLayout)
        │   ├── Label: "Horizontal Layout:"
        │   ├── Button 1
        │   ├── Button 2
        │   └── Button 3
        ├── Grid Section (QWidget with QVBoxLayout containing QGridLayout)
        │   ├── Title: "Grid Layout:"
        │   └── Grid (3x3)
        │       ├── Input field (row 0, cols 1-2)
        │       └── 6 Grid Buttons (rows 1-2)
        ├── Threading Section (QWidget with QVBoxLayout)
        │   ├── Title: "Threading Controls:"
        │   ├── Buttons (QHBoxLayout)
        │   │   ├── Start Button
        │   │   └── Stop Button
        │   └── Progress Bar
        └── Status Section (QWidget with QVBoxLayout)
            ├── Title: "Status Log:"
            └── Text Edit (read-only)

WorkerThread (QThread)
├── Signals:
│   ├── progress (int)
│   ├── finished (str)
│   └── status (str)
└── Methods:
    ├── run() - Execute background task
    └── stop() - Gracefully stop thread
```

### Key Features

1. **Threading Implementation**
   - `WorkerThread` class extends `QThread`
   - Uses PyQt signals for thread-safe communication
   - Progress updates emitted during execution
   - Graceful shutdown mechanism

2. **Layout Types Demonstrated**
   - **QVBoxLayout**: Main container and section layouts
   - **QHBoxLayout**: Horizontal button row and control buttons
   - **QGridLayout**: 3x3 grid with input field

3. **Interactive Elements**
   - Buttons with click handlers
   - Text input field for custom task names
   - Progress bar showing task completion
   - Read-only text area for status logs
   - Enable/disable state management

4. **Thread Safety**
   - All GUI updates from thread use signals
   - Thread cleanup on window close
   - Start/Stop controls prevent race conditions

### Usage Flow

1. User clicks buttons → Messages logged to status
2. User enters task name in input field
3. User clicks "Start Background Task"
   - Creates WorkerThread with task name
   - Connects signals to UI updates
   - Starts thread execution
   - Updates progress bar (0-100%)
4. User can click "Stop Task" to cancel
5. On completion, "finished" signal updates UI

### Color Scheme

- Title: Bold 18px
- Horizontal section: Light gray (#f0f0f0)
- Grid section: Medium gray (#e0e0e0)
- Threading section: Gray (#d0d0d0)
- Status section: Dark gray (#c0c0c0)
