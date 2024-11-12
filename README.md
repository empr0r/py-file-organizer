# Advanced File Organizer

A PyQt-based Python application designed to organize files within a specified directory into categorized folders based on their file types. The tool provides an interactive graphical user interface (GUI) to allow users to easily select directories and monitor file organization progress through a progress bar.

![FileOrganizer](https://github.com/user-attachments/assets/a479d470-427b-4b81-8887-ef95cdcd786f)

## Features

- **Automatic File Sorting**: Moves files to categorized folders based on extensions (e.g., Documents, Videos, Pictures).
- **Configurable Structure**: Reads configuration from `config.json` to determine file categories and target directories.
- **Progress Tracking**: Displays a progress bar to visualize the status of file organization.
- **Logging**: Logs all actions (moved, renamed, or skipped files) to `file_organizer.log`.
- **Customizable UI**: Styled with a modern look and feel.

## Installation


1. **Install the required Python package**:
   ```bash
   pip install PyQt5
   ```

2. **Run the Application**:
   ```bash
   python FileOrganizer.py
   ```

## How to Use

1. **Launch the application**.
2. **Select a directory** to organize by clicking on the "Browse" button.
3. **Click "Start Organizing"** to begin sorting the files.
4. Monitor the progress on the progress bar.
5. Upon completion, a message box will notify you that the task is complete.

## Configuration

The application relies on a `config.json` file for customization. If the file does not exist, it is created with default values upon the first run.

### Default Configuration Structure

```json
{
    "base_dir": "~/Downloads",
    "file_types": {
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".doc"],
        "Videos": [".mp4", ".mkv", ".mov", ".avi"],
        "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Music": [".mp3", ".wav", ".flac", ".aac"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Programs": [".exe", ".msi", ".sh", ".bat"],
        "MayaProjects": [".ma", ".mb", ".obj", ".fbx"]
    },
    "target_dirs": {
        "Documents": "~/Documents",
        "Videos": "~/Videos",
        "Pictures": "~/Pictures",
        "Music": "~/Music",
        "Archives": "~/Downloads/Archives",
        "Programs": "~/Downloads/Programs",
        "MayaProjects": "~/Documents/Maya"
    }
}
```

## Customization

- **Modify `config.json`** to adjust file type categories and target directories to your needs.
- **UI Customization**: Edit the `setStyleSheet` section in the `init_ui` method of the `FileOrganizerApp` class for personalized styling.

## Logging

All file movements and operations are logged to `file_organizer.log` with timestamps and details, making it easy to review what actions were taken.

## Example Use Cases

- **Organize your Downloads folder** to declutter various files into respective directories.
- **Sort project assets** like Maya files into dedicated project folders.
- **Easily identify unorganized files** that do not match any configured file type.

## Future Enhancements

- Add advanced filtering options for selecting specific file types.

## License

This project uses a MIT License. Feel free to read about it on the License page.

## Contributions

Contributions are welcome! Please fork the repository and create a pull request for any new features or improvements.

---

Happy organizing!
