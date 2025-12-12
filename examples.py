"""
Example usage of the Quanti-Badger Scanner library.
This demonstrates how to use the scanner programmatically in your own applications.
"""

from scanner import FileScanner


def example_basic_scan():
    """Example 1: Basic scan of default directories."""
    print("Example 1: Basic Scan")
    print("-" * 50)
    
    scanner = FileScanner()
    files = scanner.scan()
    summary = scanner.get_summary()
    
    print(f"Found {summary['total_files']} files")
    print(f"Total size: {summary['total_size_mb']} MB")
    print(f"File types: {summary['file_types']}")
    print()


def example_filter_by_extension():
    """Example 2: Scan for specific file types."""
    print("Example 2: Filter by File Type")
    print("-" * 50)
    
    scanner = FileScanner()
    
    # Scan only for PDF and Word documents
    scanner.scan(extensions={'.pdf', '.docx', '.doc'})
    
    print(f"Found {len(scanner.owned_files)} document files")
    for file in scanner.owned_files[:5]:  # Show first 5
        print(f"  - {file['name']} ({file['size_mb']} MB)")
    print()


def example_custom_directories():
    """Example 3: Scan custom directories."""
    print("Example 3: Scan Custom Directories")
    print("-" * 50)
    
    import os
    from pathlib import Path
    
    custom_dirs = [
        os.path.join(str(Path.home()), "Projects"),
        os.path.join(str(Path.home()), "Work"),
    ]
    
    scanner = FileScanner(scan_directories=custom_dirs)
    scanner.scan()
    
    summary = scanner.get_summary()
    print(f"Scanned directories: {summary['scanned_directories']}")
    print(f"Files found: {summary['total_files']}")
    print()


def example_filter_results():
    """Example 4: Filter scan results."""
    print("Example 4: Filter Results")
    print("-" * 50)
    
    scanner = FileScanner()
    scanner.scan()
    
    # Get all PDF files
    pdf_files = scanner.filter_by_type('.pdf')
    print(f"PDF files: {len(pdf_files)}")
    
    # Get largest files
    largest = scanner.get_largest_files(n=5)
    print(f"\nTop 5 largest files:")
    for i, file in enumerate(largest, 1):
        print(f"  {i}. {file['name']} - {file['size_mb']} MB")
    print()


def example_json_export():
    """Example 5: Export results as JSON."""
    print("Example 5: JSON Export")
    print("-" * 50)
    
    import json
    
    scanner = FileScanner()
    scanner.scan()
    
    # Get summary and files
    data = {
        'summary': scanner.get_summary(),
        'files': scanner.owned_files[:3]  # First 3 files
    }
    
    print(json.dumps(data, indent=2))
    print()


def example_specific_use_case():
    """Example 6: Find sellable media files."""
    print("Example 6: Find Sellable Media Files")
    print("-" * 50)
    
    scanner = FileScanner()
    
    # Scan for media files
    media_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mp3', '.wav'}
    scanner.scan(extensions=media_extensions)
    
    # Group by type
    images = []
    videos = []
    audio = []
    
    for file in scanner.owned_files:
        ext = file['extension'].lower()
        if ext in {'.jpg', '.jpeg', '.png', '.gif'}:
            images.append(file)
        elif ext in {'.mp4', '.avi', '.mov'}:
            videos.append(file)
        elif ext in {'.mp3', '.wav', '.flac'}:
            audio.append(file)
    
    print(f"Images: {len(images)}")
    print(f"Videos: {len(videos)}")
    print(f"Audio: {len(audio)}")
    print()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("QUANTI-BADGER SCANNER - USAGE EXAMPLES")
    print("="*60 + "\n")
    
    try:
        example_basic_scan()
        example_filter_by_extension()
        example_custom_directories()
        example_filter_results()
        example_json_export()
        example_specific_use_case()
    except Exception as e:
        print(f"Note: Some examples may not produce output if directories are empty.")
        print(f"Error: {e}")
    
    print("="*60)
    print("Examples complete!")
    print("="*60)
