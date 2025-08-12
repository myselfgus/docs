#!/usr/bin/env python3
"""
VOITHER Documentation Link Checker
Simple script to validate internal links in markdown files
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
import argparse

def find_markdown_files(directory):
    """Find all markdown files in directory"""
    md_files = []
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories, build directories, and raw folder (unprocessed backups)
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['build', 'dist', 'node_modules', 'raw']]
        
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    return md_files

def extract_links(content, file_path):
    """Extract internal links from markdown content"""
    # Pattern for markdown links: [text](link)
    link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    links = []
    
    for match in re.finditer(link_pattern, content):
        text = match.group(1)
        url = match.group(2)
        
        # Skip external URLs and anchors
        if url.startswith(('http://', 'https://', '#', 'mailto:')):
            continue
            
        links.append({
            'text': text,
            'url': url,
            'line': content[:match.start()].count('\n') + 1
        })
    
    return links

def check_file_exists(link_url, base_path):
    """Check if a linked file exists"""
    # Handle different link formats
    if link_url.startswith('./'):
        link_url = link_url[2:]  # Remove ./
    elif link_url.startswith('/'):
        link_url = link_url[1:]  # Remove leading /
    
    # Remove anchor if present
    if '#' in link_url:
        link_url = link_url.split('#')[0]
    
    # Skip empty links (pure anchors)
    if not link_url:
        return True
    
    # Build full path
    full_path = os.path.join(base_path, link_url)
    
    return os.path.exists(full_path)

def validate_documentation_links(directory):
    """Validate all internal links in documentation"""
    md_files = find_markdown_files(directory)
    errors = []
    total_links = 0
    valid_links = 0
    
    print(f"🔍 Checking links in {len(md_files)} markdown files...")
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            errors.append(f"❌ Error reading {md_file}: {e}")
            continue
        
        # Get relative path for display
        rel_path = os.path.relpath(md_file, directory)
        links = extract_links(content, md_file)
        
        if not links:
            continue
            
        print(f"  📄 {rel_path} ({len(links)} links)")
        
        for link in links:
            total_links += 1
            base_path = os.path.dirname(md_file)
            
            if check_file_exists(link['url'], base_path):
                valid_links += 1
                print(f"    ✅ Line {link['line']}: {link['url']}")
            else:
                error_msg = f"    ❌ Line {link['line']}: {link['url']} -> File not found"
                errors.append(f"{rel_path}:{link['line']} - {link['url']}")
                print(error_msg)
    
    # Summary
    print(f"\n📊 Link Validation Summary:")
    print(f"  📄 Files checked: {len(md_files)}")
    print(f"  🔗 Total links: {total_links}")
    print(f"  ✅ Valid links: {valid_links}")
    print(f"  ❌ Broken links: {len(errors)}")
    
    if errors:
        print(f"\n💥 Broken Links Found:")
        for error in errors:
            print(f"  ❌ {error}")
        return False
    else:
        print(f"\n🎉 All links are valid!")
        return True

def check_required_files(directory):
    """Check if required documentation files exist"""
    required_files = [
        'README.md',  # Root level
        'docs/TABLE_OF_CONTENTS.md',  # In docs folder
        'docs/DOCUMENTATION_INDEX.md',  # In docs folder
        'docs/CONTRIBUTING.md'  # In docs folder
    ]
    
    missing_files = []
    
    print(f"\n📋 Checking required files...")
    
    for required_file in required_files:
        file_path = os.path.join(directory, required_file)
        if os.path.exists(file_path):
            print(f"  ✅ {required_file}")
        else:
            print(f"  ❌ {required_file} - Missing")
            missing_files.append(required_file)
    
    if missing_files:
        print(f"\n💥 Missing Required Files:")
        for file in missing_files:
            print(f"  ❌ {file}")
        return False
    else:
        print(f"\n🎉 All required files present!")
        return True

def main():
    parser = argparse.ArgumentParser(description='Validate VOITHER documentation links')
    parser.add_argument('directory', nargs='?', default='.', 
                        help='Directory to check (default: current directory)')
    parser.add_argument('--quick', action='store_true',
                        help='Quick check - skip detailed link validation')
    parser.add_argument('--auto-fix', action='store_true',
                        help='Automatically fix common link issues')
    
    args = parser.parse_args()
    
    directory = os.path.abspath(args.directory)
    
    if not os.path.exists(directory):
        print(f"❌ Directory not found: {directory}")
        sys.exit(1)
    
    print(f"🔍 VOITHER Documentation Validator")
    print(f"📁 Directory: {directory}")
    if args.auto_fix:
        print(f"🔧 Auto-fix mode: Enabled")
    print("=" * 50)
    
    # Auto-fix common issues if requested
    if args.auto_fix:
        print("🔧 Attempting to auto-fix common link issues...")
        auto_fix_common_issues(directory)
        print("✅ Auto-fix completed\n")
    
    # Check required files
    required_files_ok = check_required_files(directory)
    
    if not args.quick:
        # Check links
        links_ok = validate_documentation_links(directory)
        
        overall_success = required_files_ok and links_ok
    else:
        overall_success = required_files_ok
    
    print("=" * 50)
    
    if overall_success:
        print("🎉 Documentation validation passed!")
        sys.exit(0)
    else:
        print("⚠️  WARNING: Documentation validation found issues - action recommended")
        print("📋 This is a warning only - workflow will continue")
        print("✅ Documentation validation completed (non-blocking)")
        sys.exit(0)

def auto_fix_common_issues(directory):
    """Auto-fix common link issues in documentation"""
    import glob
    import re
    
    md_files = glob.glob(os.path.join(directory, "**/*.md"), recursive=True)
    fixes_applied = 0
    
    for md_file in md_files:
        # Skip raw backup files
        if "raw/" in md_file or "/raw/" in md_file:
            continue
            
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix common link patterns based on repository structure
            # Fix paths that should point to guides/research/
            content = re.sub(r'\]\(\.\.?/templates/', '](guides/research/', content)
            content = re.sub(r'\]\(\.\.?/research/(?!README\.md)', '](guides/research/', content)
            
            # Fix paths for moved architecture files
            content = re.sub(r'\]\(\.\.?/architecture/VOITHER_BUILD_FOCUSED_APPROACH\.md', '](docs/architecture/VOITHER_BUILD_FOCUSED_APPROACH.md', content)
            content = re.sub(r'\]\(\.\.?/architecture/AI_NATIVE_A2A_ECOSYSTEM_BLUEPRINT\.md', '](docs/architecture/AI_NATIVE_A2A_ECOSYSTEM_BLUEPRINT.md', content)
            
            # Fix relative path inconsistencies for voither-system
            content = re.sub(r'\]\(\.\.?/voither-system/', '](docs/voither-system/', content)
            
            # Fix core-concepts paths that should now be in docs/core-concepts/
            content = re.sub(r'\]\(\.\.?/core-concepts/(?!med_frameworks\.md|15-dimensions\.md|emergence_enabled_ee\.md|autoagency\.md|med_core\.md|apothecary_engine\.md)', '](docs/core-concepts/', content)
            
            # Fix reengine paths
            content = re.sub(r'\]\(\.\.?/reengine/', '](docs/reengine/', content)
            
            # Fix database paths
            content = re.sub(r'\]\(\.\.?/database/', '](docs/database/', content)
            
            # Fix pipelines paths
            content = re.sub(r'\]\(\.\.?/pipelines/', '](docs/pipelines/', content)
            
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixes_applied += 1
                rel_path = os.path.relpath(md_file, directory)
                print(f"🔧 Auto-fixed links in: {rel_path}")
        
        except Exception as e:
            print(f"⚠️ Could not process {md_file}: {e}")
    
    if fixes_applied > 0:
        print(f"✅ Applied {fixes_applied} automatic link fixes")
    else:
        print("ℹ️ No common link issues found to auto-fix")

if __name__ == '__main__':
    main()