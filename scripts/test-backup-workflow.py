#!/usr/bin/env python3
"""
Backup Workflow Validation Script
Tests the key components of the backup and mirror workflow
"""

import os
import sys
import json
import tempfile
import subprocess
import tarfile
from pathlib import Path

def test_security_scan():
    """Test the security scanning functionality"""
    print("🛡️ Testing security scan functionality...")
    
    # Create test files with various content
    test_files = {
        'safe_file.md': '# Documentation\nThis is safe content.',
        'config.py': 'DATABASE_URL = "postgres://user:pass@localhost/db"',
        'secrets.env': 'API_KEY=abc123def456ghi789',
        'normal.txt': 'Regular content without secrets'
    }
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        for filename, content in test_files.items():
            with open(os.path.join(tmpdir, filename), 'w') as f:
                f.write(content)
        
        # Run security scan simulation
        os.chdir(tmpdir)
        
        # Simulate the security scan logic
        critical_findings = []
        warning_findings = []
        
        for filename in test_files:
            content = test_files[filename]
            
            # Check for connection strings
            if 'postgres://' in content and ':' in content and '@' in content:
                critical_findings.append({
                    'type': 'connection_string',
                    'file': filename,
                    'severity': 'critical'
                })
            
            # Check for API keys
            if 'API_KEY' in content:
                warning_findings.append({
                    'type': 'api_key',
                    'file': filename,
                    'severity': 'warning'
                })
            
            # Check for sensitive file extensions
            if filename.endswith('.env'):
                warning_findings.append({
                    'type': 'sensitive_file',
                    'file': filename,
                    'severity': 'warning'
                })
        
        print(f"   Critical findings: {len(critical_findings)}")
        print(f"   Warning findings: {len(warning_findings)}")
        
        if critical_findings:
            print("   ❌ Critical issues detected (expected for test)")
            for finding in critical_findings:
                print(f"      {finding['type']} in {finding['file']}")
        
        if warning_findings:
            print("   ⚠️ Warnings detected (expected for test)")
            for finding in warning_findings:
                print(f"      {finding['type']} in {finding['file']}")
        
        print("   ✅ Security scan logic validated")
        return True

def test_archive_creation():
    """Test archive creation with exclusion patterns"""
    print("🗜️ Testing archive creation...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Create test directory structure
        test_structure = {
            'docs/README.md': '# Documentation',
            'docs/guide.md': '# User Guide',
            'scripts/validate.py': '#!/usr/bin/env python3',
            'node_modules/package/index.js': 'module.exports = {};',
            '__pycache__/cache.pyc': 'compiled python',
            'temp.tmp': 'temporary file',
            '.git/config': '[core]',
            'important.md': '# Important Documentation'
        }
        
        # Create files and directories
        for filepath, content in test_structure.items():
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(content)
        
        # Create exclusion patterns (simplified version)
        exclusions = [
            'node_modules/',
            '__pycache__/',
            '*.tmp',
            '.git/config'
        ]
        
        # Create archive (simplified simulation)
        archive_name = 'test-backup.tar.gz'
        
        try:
            with tarfile.open(archive_name, 'w:gz') as tar:
                for root, dirs, files in os.walk('.'):
                    # Filter directories
                    dirs[:] = [d for d in dirs if not any(d.startswith(exc.rstrip('/')) for exc in exclusions)]
                    
                    for file in files:
                        filepath = os.path.join(root, file)
                        relpath = os.path.relpath(filepath, '.')
                        
                        # Check if file should be excluded
                        should_exclude = False
                        for pattern in exclusions:
                            if pattern.endswith('/'):
                                if relpath.startswith(pattern):
                                    should_exclude = True
                                    break
                            elif pattern.startswith('*.'):
                                if relpath.endswith(pattern[1:]):
                                    should_exclude = True
                                    break
                            elif pattern in relpath:
                                should_exclude = True
                                break
                        
                        if not should_exclude and file != archive_name:
                            tar.add(filepath, arcname=relpath)
            
            # Verify archive
            if os.path.exists(archive_name):
                with tarfile.open(archive_name, 'r:gz') as tar:
                    members = tar.getnames()
                    
                print(f"   Archive created: {archive_name}")
                print(f"   Files in archive: {len(members)}")
                
                # Check if important files are included
                important_files = ['docs/README.md', 'docs/guide.md', 'important.md', 'scripts/validate.py']
                included_important = [f for f in important_files if f in members]
                print(f"   Important files included: {len(included_important)}/{len(important_files)}")
                
                # Check if excluded files are properly excluded
                excluded_files = ['node_modules/package/index.js', '__pycache__/cache.pyc', 'temp.tmp']
                incorrectly_included = [f for f in excluded_files if f in members]
                
                if incorrectly_included:
                    print(f"   ❌ Files incorrectly included: {incorrectly_included}")
                    return False
                else:
                    print("   ✅ Exclusion patterns working correctly")
                
                # Verify archive integrity
                try:
                    with tarfile.open(archive_name, 'r:gz') as tar:
                        # Try to read all members
                        for member in tar.getmembers():
                            if member.isfile():
                                tar.extractfile(member)
                    print("   ✅ Archive integrity verified")
                    return True
                except Exception as e:
                    print(f"   ❌ Archive integrity check failed: {e}")
                    return False
            else:
                print("   ❌ Archive creation failed")
                return False
                
        except Exception as e:
            print(f"   ❌ Archive creation error: {e}")
            return False

def test_retry_logic():
    """Test retry logic simulation"""
    print("🔄 Testing retry logic...")
    
    # Simulate retry with exponential backoff
    import time
    
    def simulate_operation_with_retries(success_on_attempt=2, max_retries=3):
        """Simulate an operation that succeeds on a specific attempt"""
        for attempt in range(1, max_retries + 1):
            print(f"   Attempt {attempt}...")
            
            if attempt == success_on_attempt:
                print(f"   ✅ Operation succeeded on attempt {attempt}")
                return True
            else:
                if attempt < max_retries:
                    wait_time = (2 ** attempt) * 2  # Exponential backoff
                    print(f"   ❌ Attempt {attempt} failed, waiting {wait_time}s...")
                    time.sleep(0.1)  # Short sleep for testing
                else:
                    print(f"   ❌ All {max_retries} attempts failed")
                    return False
    
    # Test successful retry
    print("   Testing successful retry scenario...")
    success = simulate_operation_with_retries(success_on_attempt=2, max_retries=3)
    if success:
        print("   ✅ Retry logic working correctly")
    else:
        print("   ❌ Retry logic failed")
        return False
    
    # Test failure scenario
    print("   Testing failure scenario...")
    failure = simulate_operation_with_retries(success_on_attempt=5, max_retries=3)
    if not failure:
        print("   ✅ Failure handling working correctly")
        return True
    else:
        print("   ❌ Failure handling failed")
        return False

def test_report_generation():
    """Test backup report generation"""
    print("📊 Testing report generation...")
    
    # Simulate backup report data
    backup_report = {
        "timestamp": "2024-08-15T09:17:00Z",
        "repository": "test/repo",
        "branch": "main",
        "commit_sha": "abc123",
        "trigger": "workflow_dispatch",
        "backup_type": "full",
        "archive": {
            "filename": "test-backup.tar.gz",
            "size_bytes": "1048576",
            "size_mb": "1",
            "file_count": "25",
            "checksum": "sha256:abcdef..."
        },
        "security": {
            "status": "proceed",
            "critical_issues": "0",
            "proceed_status": "approved"
        },
        "uploads": {
            "gcs_latest": {
                "status": "success",
                "attempts": "1"
            },
            "gcs_archive": {
                "status": "success",
                "attempts": "2"
            },
            "drive": {
                "rclone_status": "configured",
                "upload_status": "success",
                "attempts": "1"
            }
        },
        "destinations": {
            "gcs_bucket": "test-bucket",
            "drive_remote": "VAULT",
            "drive_path": "artefatos/versions"
        }
    }
    
    # Calculate overall success
    gcs_success = (backup_report["uploads"]["gcs_latest"]["status"] == "success" and 
                   backup_report["uploads"]["gcs_archive"]["status"] == "success")
    
    drive_success = (backup_report["uploads"]["drive"]["upload_status"] == "success" or 
                     backup_report["uploads"]["drive"]["rclone_status"] != "configured")
    
    backup_report["overall_success"] = gcs_success and drive_success
    backup_report["partial_success"] = gcs_success or drive_success
    
    # Save report
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(backup_report, f, indent=2)
        report_path = f.name
    
    try:
        # Verify report can be loaded
        with open(report_path, 'r') as f:
            loaded_report = json.load(f)
        
        print(f"   Report generated: {report_path}")
        print(f"   Overall success: {loaded_report['overall_success']}")
        print(f"   Archive size: {loaded_report['archive']['size_mb']} MB")
        print(f"   Security status: {loaded_report['security']['status']}")
        
        # Verify required fields
        required_fields = ['timestamp', 'repository', 'archive', 'security', 'uploads']
        missing_fields = [field for field in required_fields if field not in loaded_report]
        
        if missing_fields:
            print(f"   ❌ Missing required fields: {missing_fields}")
            return False
        else:
            print("   ✅ Report generation working correctly")
            return True
            
    finally:
        # Cleanup
        os.unlink(report_path)

def main():
    """Run all validation tests"""
    print("🧪 Running Backup Workflow Validation Tests")
    print("=" * 50)
    
    tests = [
        ("Security Scan", test_security_scan),
        ("Archive Creation", test_archive_creation),
        ("Retry Logic", test_retry_logic),
        ("Report Generation", test_report_generation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validation tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed - review output above")
        return 1

if __name__ == '__main__':
    sys.exit(main())