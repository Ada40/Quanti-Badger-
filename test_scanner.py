"""
Tests for the Quanti-Badger Device Scanner
"""

import os
import tempfile
import shutil
from pathlib import Path
import sys

# Add parent directory to path to import scanner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scanner import FileScanner


class TestFileScanner:
    """Test suite for FileScanner class."""
    
    def setup_test_environment(self):
        """Create a temporary directory structure for testing."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create test files
        self.test_files = {
            'document.txt': b'This is a test document',
            'image.jpg': b'\xff\xd8\xff\xe0' + b'\x00' * 100,  # Fake JPEG header
            'data.pdf': b'%PDF-1.4' + b'\x00' * 200,
            '.hidden': b'hidden file',
            'large_file.dat': b'\x00' * (110 * 1024 * 1024),  # 110 MB - too large
            'empty.txt': b'',  # Empty file
        }
        
        for filename, content in self.test_files.items():
            filepath = os.path.join(self.test_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(content)
        
        return self.test_dir
    
    def cleanup_test_environment(self):
        """Remove temporary test directory."""
        if hasattr(self, 'test_dir') and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_scanner_initialization(self):
        """Test that scanner initializes correctly."""
        scanner = FileScanner()
        assert scanner.current_user is not None
        assert scanner.platform is not None
        assert len(scanner.scan_directories) >= 0
        print("✓ Scanner initialization test passed")
    
    def test_scan_finds_files(self):
        """Test that scanner finds files in specified directory."""
        test_dir = self.setup_test_environment()
        
        try:
            scanner = FileScanner(scan_directories=[test_dir])
            results = scanner.scan()
            
            # Should find only valid files (not hidden, not empty, not too large)
            assert isinstance(results, list)
            
            # Check that valid files are found
            found_names = [f['name'] for f in results]
            assert 'document.txt' in found_names
            assert 'image.jpg' in found_names
            assert 'data.pdf' in found_names
            
            # Check that invalid files are excluded
            assert '.hidden' not in found_names  # Hidden file
            assert 'empty.txt' not in found_names  # Empty file
            assert 'large_file.dat' not in found_names  # Too large
            
            print(f"✓ Scan test passed - found {len(results)} valid files")
        finally:
            self.cleanup_test_environment()
    
    def test_filter_by_extension(self):
        """Test filtering files by extension."""
        test_dir = self.setup_test_environment()
        
        try:
            scanner = FileScanner(scan_directories=[test_dir])
            scanner.scan(extensions={'.txt'})
            
            # Should only find .txt files
            found_extensions = [f['extension'] for f in scanner.owned_files]
            assert all(ext == '.txt' for ext in found_extensions)
            
            print("✓ Extension filter test passed")
        finally:
            self.cleanup_test_environment()
    
    def test_get_summary(self):
        """Test summary statistics."""
        test_dir = self.setup_test_environment()
        
        try:
            scanner = FileScanner(scan_directories=[test_dir])
            scanner.scan()
            summary = scanner.get_summary()
            
            assert 'total_files' in summary
            assert 'total_size_mb' in summary
            assert 'file_types' in summary
            assert 'platform' in summary
            assert 'user' in summary
            assert summary['total_files'] > 0
            
            print("✓ Summary test passed")
        finally:
            self.cleanup_test_environment()
    
    def test_filter_by_type(self):
        """Test filtering results by file type."""
        test_dir = self.setup_test_environment()
        
        try:
            scanner = FileScanner(scan_directories=[test_dir])
            scanner.scan()
            
            txt_files = scanner.filter_by_type('.txt')
            assert all(f['extension'] == '.txt' for f in txt_files)
            
            print("✓ Filter by type test passed")
        finally:
            self.cleanup_test_environment()
    
    def test_get_largest_files(self):
        """Test getting largest files."""
        test_dir = self.setup_test_environment()
        
        try:
            scanner = FileScanner(scan_directories=[test_dir])
            scanner.scan()
            
            top_files = scanner.get_largest_files(n=2)
            assert len(top_files) <= 2
            
            # Verify files are sorted by size
            if len(top_files) > 1:
                assert top_files[0]['size'] >= top_files[1]['size']
            
            print("✓ Largest files test passed")
        finally:
            self.cleanup_test_environment()
    
    def test_file_info_structure(self):
        """Test that file info has correct structure."""
        test_dir = self.setup_test_environment()
        
        try:
            scanner = FileScanner(scan_directories=[test_dir])
            results = scanner.scan()
            
            if results:
                file_info = results[0]
                required_keys = ['path', 'name', 'size', 'size_mb', 'extension', 
                               'modified', 'owner', 'available_to_sell']
                
                for key in required_keys:
                    assert key in file_info, f"Missing key: {key}"
                
                assert file_info['available_to_sell']
                
                print("✓ File info structure test passed")
        finally:
            self.cleanup_test_environment()


def run_all_tests():
    """Run all tests."""
    test_suite = TestFileScanner()
    
    tests = [
        test_suite.test_scanner_initialization,
        test_suite.test_scan_finds_files,
        test_suite.test_filter_by_extension,
        test_suite.test_get_summary,
        test_suite.test_filter_by_type,
        test_suite.test_get_largest_files,
        test_suite.test_file_info_structure,
    ]
    
    print("\n" + "="*60)
    print("Running Quanti-Badger Scanner Tests")
    print("="*60 + "\n")
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
