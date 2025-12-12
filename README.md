# Quanti-Badger Device Scanner

A cross-platform tool that scans a user's devices to identify files they own and are available to sell. The scanner only shows files that belong to the current user and meet specific criteria for selling.

## Features

- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **User Ownership Verification**: Only shows files owned by the current user
- **Smart File Filtering**: Automatically excludes:
  - Hidden files (starting with `.` or `~`)
  - System files
  - Empty files
  - Files larger than 100 MB
  - Files without read permissions
- **Multiple Output Formats**: Text or JSON output
- **File Type Filtering**: Scan for specific file extensions
- **Detailed Statistics**: Get summaries of files found, sizes, and types

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ada40/Quanti-Badger-.git
cd Quanti-Badger-
```

2. Ensure you have Python 3.7 or higher:
```bash
python --version
```

No additional dependencies required! The scanner uses only Python standard library.

## Usage

### Basic Scan

Scan default user directories (Documents, Downloads, Desktop, etc.):

```bash
python main.py
```

### Scan Specific Directories

```bash
python main.py --directories ~/Documents ~/Pictures
```

### Filter by File Type

Scan only for specific file extensions:

```bash
python main.py --extensions .pdf .txt .docx
```

### Get Top Largest Files

Show only the N largest files:

```bash
python main.py --top 10
```

### JSON Output

Output results in JSON format for integration with other tools:

```bash
python main.py --output json
```

### Combined Options

```bash
python main.py --directories ~/Documents --extensions .pdf --top 5 --output json
```

## How It Works

### File Ownership Verification

- **Windows**: Checks if the user has write access to the file
- **Unix/Linux/macOS**: Compares the file owner with the current user

### File Availability Criteria

A file is considered "available to sell" if:
1. The current user owns it
2. It's readable
3. It's between 1 byte and 100 MB in size
4. It's not a hidden or system file

## Example Output

```
============================================================
QUANTI-BADGER DEVICE SCANNER
============================================================

Platform: Linux
User: john

Scanned directories:
  - /home/john/Documents
  - /home/john/Downloads
  - /home/john/Desktop

============================================================
SCAN SUMMARY
============================================================
Total files available to sell: 42
Total size: 156.78 MB

File types found:
  .pdf: 15 files
  .txt: 12 files
  .docx: 8 files
  .jpg: 7 files

============================================================
YOUR FILES AVAILABLE TO SELL
============================================================

1. project_report.pdf
   Path: /home/john/Documents/project_report.pdf
   Size: 2.45 MB
   Type: .pdf
   Modified: 2025-12-10T14:30:00

...
```

## Testing

Run the test suite to verify the scanner works correctly:

```bash
python test_scanner.py
```

## API Usage

You can also use the scanner as a Python module:

```python
from scanner import FileScanner

# Initialize scanner
scanner = FileScanner()

# Scan for all files
results = scanner.scan()

# Scan for specific file types
pdf_files = scanner.scan(extensions={'.pdf', '.docx'})

# Get summary statistics
summary = scanner.get_summary()
print(f"Found {summary['total_files']} files")

# Filter results
txt_files = scanner.filter_by_type('.txt')

# Get largest files
largest = scanner.get_largest_files(n=10)
```

## Privacy & Security

- **Local Only**: All scanning happens locally on your device
- **No Data Transmission**: No files or file information is sent anywhere
- **User-Owned Only**: Only files you own are scanned
- **Permission Respecting**: Files you don't have permission to read are automatically excluded

## License

This project is open source and available for use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
