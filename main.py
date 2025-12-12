"""
Main application entry point for Quanti-Badger Device Scanner.
Provides CLI interface for scanning user's devices for files available to sell.
"""

import argparse
import json
import sys
from scanner import FileScanner


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def print_scan_results(scanner: FileScanner, output_format: str = 'text'):
    """
    Print scan results in the specified format.
    
    Args:
        scanner: FileScanner instance with completed scan
        output_format: Output format ('text' or 'json')
    """
    files = scanner.owned_files
    summary = scanner.get_summary()
    
    if output_format == 'json':
        output = {
            'summary': summary,
            'files': files
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n" + "="*60)
        print("QUANTI-BADGER DEVICE SCANNER")
        print("="*60)
        print(f"\nPlatform: {summary['platform']}")
        print(f"User: {summary['user']}")
        print(f"\nScanned directories:")
        for dir in summary['scanned_directories']:
            print(f"  - {dir}")
        
        print(f"\n{'='*60}")
        print("SCAN SUMMARY")
        print("="*60)
        print(f"Total files available to sell: {summary['total_files']}")
        print(f"Total size: {summary['total_size_mb']} MB")
        
        if summary['file_types']:
            print(f"\nFile types found:")
            for ext, count in sorted(summary['file_types'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {ext or '(no extension)'}: {count} files")
        
        if files:
            print(f"\n{'='*60}")
            print("YOUR FILES AVAILABLE TO SELL")
            print("="*60)
            
            # Show first 20 files
            for i, file in enumerate(files[:20], 1):
                print(f"\n{i}. {file['name']}")
                print(f"   Path: {file['path']}")
                print(f"   Size: {format_size(file['size'])}")
                print(f"   Type: {file['extension'] or 'no extension'}")
                print(f"   Modified: {file['modified']}")
            
            if len(files) > 20:
                print(f"\n... and {len(files) - 20} more files")
                print(f"\nUse --output json to see all files or --top N to see largest files")
        else:
            print("\nNo files found that meet the criteria for selling.")
            print("Files must be:")
            print("  - Owned by you")
            print("  - Readable")
            print("  - Between 1 byte and 100 MB")
            print("  - Not hidden or system files")


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='Quanti-Badger: Scan your devices for files you own and can sell.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan default directories
  python main.py
  
  # Scan specific directories
  python main.py --directories ~/Documents ~/Downloads
  
  # Filter by file types
  python main.py --extensions .pdf .txt .docx
  
  # Get top 10 largest files
  python main.py --top 10
  
  # Output as JSON
  python main.py --output json
        """
    )
    
    parser.add_argument(
        '--directories',
        nargs='+',
        help='Directories to scan (default: user Documents, Downloads, Desktop, etc.)'
    )
    
    parser.add_argument(
        '--extensions',
        nargs='+',
        help='Filter by file extensions (e.g., .pdf .txt .docx)'
    )
    
    parser.add_argument(
        '--output',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--top',
        type=int,
        metavar='N',
        help='Show only the top N largest files'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize scanner
        print("Initializing scanner...", file=sys.stderr)
        scanner = FileScanner(scan_directories=args.directories)
        
        # Prepare extensions filter
        extensions = None
        if args.extensions:
            extensions = set(ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions)
        
        # Perform scan
        print("Scanning directories for your files...", file=sys.stderr)
        scanner.scan(extensions=extensions)
        
        # Filter to top N if requested
        if args.top:
            scanner.owned_files = scanner.get_largest_files(args.top)
        
        # Print results
        print_scan_results(scanner, args.output)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
