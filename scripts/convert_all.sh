#!/bin/bash

# Batch Notebook Converter
# Converts all .ipynb files in the notebooks directory to interactive markdown

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
NOTEBOOKS_DIR="$PROJECT_ROOT/notebooks"
OUTPUT_DIR="$PROJECT_ROOT/docs/_notebooks"

echo "🚀 Converting all notebooks to interactive markdown..."
echo "📂 Input directory: $NOTEBOOKS_DIR"
echo "📁 Output directory: $OUTPUT_DIR"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Counter for converted files
converted_count=0

# Find and convert all .ipynb files
for notebook in "$NOTEBOOKS_DIR"/*.ipynb; do
    if [ -f "$notebook" ]; then
        # Get filename without extension
        filename=$(basename "$notebook" .ipynb)
        output_file="$OUTPUT_DIR/${filename}.md"
        
        echo "🔄 Converting: $filename"
        
        # Run conversion script
        python3 "$SCRIPT_DIR/convert_notebook.py" "$notebook" -o "$output_file"
        
        if [ $? -eq 0 ]; then
            echo "✅ Successfully converted: $filename"
            ((converted_count++))
        else
            echo "❌ Failed to convert: $filename"
        fi
        
        echo ""
    fi
done

echo "🎉 Conversion complete!"
echo "📊 Converted $converted_count notebook(s)"

if [ $converted_count -gt 0 ]; then
    echo ""
    echo "Next steps:"
    echo "1. Review the converted markdown files in docs/_notebooks/"
    echo "2. Edit reflection questions as needed"
    echo "3. Test the interactive experience locally"
    echo "4. Deploy to GitHub Pages"
fi
