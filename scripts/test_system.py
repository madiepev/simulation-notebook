#!/usr/bin/env python3
"""
Test script for the interactive notebook template system
"""

import os
import sys
import json
from pathlib import Path

def test_converted_notebook():
    """Test that the converted notebook has the expected structure"""
    notebook_path = "docs/_notebooks/01-basic-fine-tuning.md"
    
    if not os.path.exists(notebook_path):
        print("❌ Converted notebook not found")
        return False
    
    with open(notebook_path, 'r') as f:
        content = f.read()
    
    # Check for required elements
    checks = [
        ("Frontmatter", "layout: notebook" in content),
        ("Code cells", "code-cell" in content),
        ("Reflection questions", "reflection-question" in content),
        ("Cell IDs", "data-cell-id" in content),
        ("Run buttons", "run-button" in content or "Run" in content),
        ("Output areas", "code-output" in content)
    ]
    
    all_passed = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    return all_passed

def test_file_structure():
    """Test that all required files exist"""
    required_files = [
        "docs/_config.yml",
        "docs/_layouts/notebook.html",
        "docs/_layouts/default.html",
        "docs/assets/notebook.css",
        "docs/assets/notebook.js",
        "docs/index.md",
        "scripts/convert_notebook.py",
        "scripts/convert_all.sh"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_exist = False
    
    return all_exist

def main():
    print("🧪 Testing Interactive Notebook Template System\n")
    
    print("📁 Testing file structure...")
    structure_ok = test_file_structure()
    
    print("\n📓 Testing converted notebook...")
    notebook_ok = test_converted_notebook()
    
    print(f"\n📊 Test Results:")
    print(f"File structure: {'✅ PASS' if structure_ok else '❌ FAIL'}")
    print(f"Notebook conversion: {'✅ PASS' if notebook_ok else '❌ FAIL'}")
    
    if structure_ok and notebook_ok:
        print("\n🎉 All tests passed!")
        print("\nNext steps:")
        print("1. Run 'cd docs && jekyll serve' to test locally")
        print("2. Push to GitHub to deploy via GitHub Pages")
        print("3. Visit your GitHub Pages URL to see the interactive notebooks")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
