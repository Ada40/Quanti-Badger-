"""
Cross-Platform Device Scanner
Scans user's devices to identify files they own and are available to sell.
"""

import os
import platform
import pathlib
from typing import List, Dict, Set
from datetime import datetime
import getpass

# Import pwd for Unix-like systems (not available on Windows)
try:
    import pwd
    PWD_AVAILABLE = True
except ImportError:
    PWD_AVAILABLE = False


class FileScanner:
    """Scanner that identifies user-owned files across platforms."""
    
    def __init__(self, scan_directories: List[str] = None):
        """
        Initialize the file scanner.
        
        Args:
            scan_directories: List of directories to scan. If None, uses default user directories.
        """
        self.current_user = getpass.getuser()
        self.platform = platform.system()
        self.scan_directories = scan_directories or self._get_default_directories()
        self.owned_files = []
        
    def _get_default_directories(self) -> List[str]:
        """Get default directories to scan based on platform."""
        home = str(pathlib.Path.home())
        
        # Common user directories across platforms
        default_dirs = [
            os.path.join(home, "Documents"),
            os.path.join(home, "Downloads"),
            os.path.join(home, "Desktop"),
        ]
        
        # Platform-specific directories
        if self.platform == "Windows":
            default_dirs.extend([
                os.path.join(home, "Pictures"),
                os.path.join(home, "Videos"),
                os.path.join(home, "Music"),
            ])
        elif self.platform == "Darwin":  # macOS
            default_dirs.extend([
                os.path.join(home, "Pictures"),
                os.path.join(home, "Movies"),
                os.path.join(home, "Music"),
            ])
        elif self.platform == "Linux":
            default_dirs.extend([
                os.path.join(home, "Pictures"),
                os.path.join(home, "Videos"),
                os.path.join(home, "Music"),
            ])
        
        # Filter to only existing directories
        return [d for d in default_dirs if os.path.exists(d)]
    
    def _is_owned_by_user(self, filepath: str) -> bool:
        """
        Check if a file is owned by the current user.
        
        Args:
            filepath: Path to the file to check
            
        Returns:
            True if the file is owned by the current user, False otherwise
        """
        try:
            if self.platform == "Windows":
                # On Windows, check if user has write access
                return os.access(filepath, os.W_OK)
            else:
                # On Unix-like systems, check actual ownership
                if not PWD_AVAILABLE:
                    return os.access(filepath, os.W_OK)
                file_stat = os.stat(filepath)
                file_owner = pwd.getpwuid(file_stat.st_uid).pw_name
                return file_owner == self.current_user
        except (OSError, KeyError):
            return False
    
    def _is_available_to_sell(self, filepath: str) -> bool:
        """
        Determine if a file is available to sell.
        A file is available if:
        - User owns it
        - It's readable
        - It's not a system file
        - It has reasonable size (not empty, not too large)
        
        Args:
            filepath: Path to the file to check
            
        Returns:
            True if the file can be sold, False otherwise
        """
        try:
            # Check ownership
            if not self._is_owned_by_user(filepath):
                return False
            
            # Check readability
            if not os.access(filepath, os.R_OK):
                return False
            
            # Check file size (between 1 byte and 100 MB)
            size = os.path.getsize(filepath)
            if size == 0 or size > 100 * 1024 * 1024:
                return False
            
            # Exclude system and hidden files
            basename = os.path.basename(filepath)
            if basename.startswith('.') or basename.startswith('~'):
                return False
            
            return True
        except OSError:
            return False
    
    def scan(self, extensions: Set[str] = None) -> List[Dict]:
        """
        Scan directories for user-owned files available to sell.
        
        Args:
            extensions: Set of file extensions to include (e.g., {'.txt', '.pdf'})
                       If None, scans all files.
        
        Returns:
            List of dictionaries containing file information
        """
        self.owned_files = []
        
        for directory in self.scan_directories:
            if not os.path.exists(directory):
                continue
                
            try:
                for root, dirs, files in os.walk(directory):
                    # Skip hidden directories
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        
                        # Filter by extension if specified
                        if extensions:
                            _, ext = os.path.splitext(filename)
                            if ext.lower() not in extensions:
                                continue
                        
                        # Check if file is available to sell
                        if self._is_available_to_sell(filepath):
                            file_info = self._get_file_info(filepath)
                            self.owned_files.append(file_info)
            except (OSError, PermissionError):
                # Skip directories we can't access
                continue
        
        return self.owned_files
    
    def _get_file_info(self, filepath: str) -> Dict:
        """
        Get detailed information about a file.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Dictionary with file information
        """
        try:
            stat_info = os.stat(filepath)
            _, ext = os.path.splitext(filepath)
            
            return {
                'path': filepath,
                'name': os.path.basename(filepath),
                'size': stat_info.st_size,
                'size_mb': round(stat_info.st_size / (1024 * 1024), 2),
                'extension': ext,
                'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                'owner': self.current_user,
                'available_to_sell': True
            }
        except OSError:
            return {
                'path': filepath,
                'name': os.path.basename(filepath),
                'error': 'Could not read file information'
            }
    
    def get_summary(self) -> Dict:
        """
        Get summary statistics of the scan.
        
        Returns:
            Dictionary with summary information
        """
        if not self.owned_files:
            return {
                'total_files': 0,
                'total_size_mb': 0,
                'file_types': {}
            }
        
        total_size = sum(f.get('size', 0) for f in self.owned_files)
        file_types = {}
        
        for file in self.owned_files:
            ext = file.get('extension', 'unknown')
            file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            'total_files': len(self.owned_files),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'file_types': file_types,
            'scanned_directories': self.scan_directories,
            'platform': self.platform,
            'user': self.current_user
        }
    
    def filter_by_type(self, file_type: str) -> List[Dict]:
        """
        Filter owned files by file extension.
        
        Args:
            file_type: File extension to filter by (e.g., '.pdf', '.txt')
        
        Returns:
            List of files matching the extension
        """
        return [f for f in self.owned_files if f.get('extension', '').lower() == file_type.lower()]
    
    def get_largest_files(self, n: int = 10) -> List[Dict]:
        """
        Get the n largest files from the scan.
        
        Args:
            n: Number of files to return
        
        Returns:
            List of the largest files
        """
        return sorted(self.owned_files, key=lambda x: x.get('size', 0), reverse=True)[:n]
