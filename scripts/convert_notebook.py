#!/usr/bin/env python3
"""
Jupyter Notebook to Interactive Markdown Converter

Converts .ipynb files to markdown format for GitHub Pages interactive simulation.
Includes support for adding reflection questions after code cells.
"""

import json
import re
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class NotebookConverter:
    def __init__(self):
        self.cell_counter = 0
        self.question_counter = 0
        
    def convert_notebook(self, 
                        notebook_path: str, 
                        output_path: str = None,
                        title: str = None,
                        description: str = None,
                        difficulty: str = "beginner",
                        add_reflection_prompts: bool = True) -> str:
        """Convert a Jupyter notebook to interactive markdown format."""
        
        # Load notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Reset counters
        self.cell_counter = 0
        self.question_counter = 0
        
        # Extract title from filename if not provided
        if not title:
            title = Path(notebook_path).stem.replace('-', ' ').replace('_', ' ').title()
        
        # Generate markdown content
        markdown_content = self._generate_frontmatter(title, description, difficulty)
        markdown_content += self._convert_cells(notebook['cells'], add_reflection_prompts)
        
        # Write output
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"✅ Converted notebook saved to: {output_path}")
        
        return markdown_content
    
    def _generate_frontmatter(self, title: str, description: str = None, difficulty: str = "beginner") -> str:
        """Generate Jekyll frontmatter for the markdown file."""
        frontmatter = "---\n"
        frontmatter += "layout: notebook\n"
        frontmatter += f"title: \"{title}\"\n"
        
        if description:
            frontmatter += f"description: \"{description}\"\n"
        
        frontmatter += f"difficulty: {difficulty}\n"
        frontmatter += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
        frontmatter += "---\n\n"
        
        return frontmatter
    
    def _convert_cells(self, cells: List[Dict], add_reflection_prompts: bool) -> str:
        """Convert notebook cells to markdown format."""
        markdown = ""
        
        for i, cell in enumerate(cells):
            cell_type = cell.get('cell_type', 'code')
            
            if cell_type == 'markdown':
                markdown += self._convert_markdown_cell(cell)
                
            elif cell_type == 'code':
                self.cell_counter += 1
                markdown += self._convert_code_cell(cell, self.cell_counter)
                
                # Add reflection question prompt after code cells (if enabled)
                if add_reflection_prompts and self._should_add_reflection(cell, i, cells):
                    markdown += self._generate_reflection_template(cell)
                    
        return markdown
    
    def _convert_markdown_cell(self, cell: Dict) -> str:
        """Convert markdown cell."""
        source = ''.join(cell.get('source', []))
        
        # Clean up any HTML styling that might not work well
        source = self._clean_markdown(source)
        
        return f"{source}\n\n"
    
    def _convert_code_cell(self, cell: Dict, cell_number: int) -> str:
        """Convert code cell with interactive wrapper."""
        source = ''.join(cell.get('source', []))
        outputs = cell.get('outputs', [])
        
        # Generate cell ID
        cell_id = f"cell-{cell_number}"
        
        # Build code cell HTML
        code_cell = f'<div class="code-cell" data-cell-id="{cell_id}">\n'
        code_cell += '<div class="code-input">\n'
        code_cell += '```python\n'
        code_cell += source
        code_cell += '\n```\n'
        code_cell += '</div>\n'
        
        # Process outputs
        if outputs:
            output_type, output_content = self._process_outputs(outputs)
            code_cell += f'<div class="code-output" data-expected-output="{output_type}">\n'
            code_cell += f'<pre class="output-text">{output_content}</pre>\n'
            code_cell += '</div>\n'
        else:
            # Add empty output div for simulation
            code_cell += '<div class="code-output" data-expected-output="text">\n'
            code_cell += '<pre class="output-text">Ready to execute...</pre>\n'
            code_cell += '</div>\n'
        
        code_cell += '</div>\n\n'
        
        return code_cell
    
    def _process_outputs(self, outputs: List[Dict]) -> tuple:
        """Process notebook outputs and return (type, content)."""
        output_content = ""
        output_type = "text"
        
        for output in outputs:
            if output.get('output_type') == 'stream':
                text = ''.join(output.get('text', []))
                output_content += text
                
            elif output.get('output_type') == 'execute_result':
                data = output.get('data', {})
                if 'text/plain' in data:
                    text = ''.join(data['text/plain'])
                    output_content += text
                elif 'text/html' in data:
                    output_type = "html"
                    # For HTML output, we'll include it but mark it as such
                    output_content += ''.join(data['text/html'])
                    
            elif output.get('output_type') == 'display_data':
                data = output.get('data', {})
                if 'image/png' in data:
                    output_type = "image"
                    output_content = "[Image output - would display in actual execution]"
                elif 'text/html' in data:
                    output_type = "html"
                    output_content += ''.join(data['text/html'])
                    
            elif output.get('output_type') == 'error':
                output_type = "error"
                error_name = output.get('ename', 'Error')
                error_value = output.get('evalue', '')
                output_content += f"{error_name}: {error_value}"
        
        return output_type, output_content.strip()
    
    def _should_add_reflection(self, cell: Dict, index: int, all_cells: List[Dict]) -> bool:
        """Determine if a reflection question should be added after this cell."""
        source = ''.join(cell.get('source', []))
        
        # Add reflection after cells that:
        # 1. Have meaningful output
        # 2. Introduce new concepts
        # 3. Are not just imports or setup
        
        # Skip simple imports
        if re.match(r'^(import|from)\s+\w+', source.strip()):
            return False
            
        # Skip very short cells
        if len(source.strip()) < 20:
            return False
            
        # Skip cells that are just variable assignments
        if re.match(r'^\w+\s*=\s*.+$', source.strip()):
            return False
            
        # Add for cells with loops, functions, or data processing
        if any(keyword in source for keyword in ['def ', 'for ', 'while ', 'if ', 'print(', 'plt.', 'pd.', 'np.']):
            return True
            
        # Add for cells with outputs
        if cell.get('outputs'):
            return True
            
        return False
    
    def _generate_reflection_template(self, cell: Dict) -> str:
        """Generate a template reflection question for a code cell."""
        self.question_counter += 1
        source = ''.join(cell.get('source', []))
        
        # Generate contextual question based on code content
        question_text, options = self._generate_contextual_question(source)
        
        question_id = f"q{self.question_counter}"
        
        reflection = f'<div class="reflection-question" data-question-id="{question_id}">\n'
        reflection += '<h4>🤔 Reflection Question</h4>\n'
        reflection += f'<p>{question_text}</p>\n'
        reflection += '<div class="choices">\n'
        
        for i, option in enumerate(options):
            option_id = chr(ord('a') + i)
            reflection += f'<label><input type="radio" name="{question_id}" value="{option_id}"> {option}</label>\n'
        
        reflection += '</div>\n'
        reflection += f'<div class="answer" data-correct="a">\n'
        reflection += '<p><strong>Think about it:</strong> Consider what this code accomplishes and why it\'s structured this way.</p>\n'
        reflection += '</div>\n'
        reflection += '</div>\n\n'
        
        return reflection
    
    def _generate_contextual_question(self, source: str) -> tuple:
        """Generate contextual question based on code content."""
        source_lower = source.lower()
        
        # Default generic options
        options = [
            "This code performs data processing",
            "This code handles user input", 
            "This code implements error handling",
            "This code defines a new function"
        ]
        
        if 'import' in source_lower:
            question = "What is the primary purpose of this code block?"
            options = [
                "Import necessary libraries and modules",
                "Define new variables",
                "Process existing data",
                "Output results to the user"
            ]
            
        elif 'def ' in source_lower:
            question = "What does this function definition accomplish?"
            options = [
                "Creates a reusable block of code",
                "Imports external libraries",
                "Stores data in variables",
                "Displays output to the user"
            ]
            
        elif any(word in source_lower for word in ['print(', 'display(', 'show()']):
            question = "What is the main outcome of executing this code?"
            options = [
                "Displays output or results",
                "Saves data to a file", 
                "Imports new libraries",
                "Defines new variables"
            ]
            
        elif any(word in source_lower for word in ['for ', 'while ', 'loop']):
            question = "What programming concept is demonstrated here?"
            options = [
                "Iteration and looping",
                "Variable assignment",
                "Function definition",
                "Library importation"
            ]
            
        elif any(word in source_lower for word in ['if ', 'else', 'elif']):
            question = "What control structure is being used?"
            options = [
                "Conditional logic (if/else)",
                "Loop iteration",
                "Function definition",
                "Exception handling"
            ]
            
        else:
            question = "What is the primary purpose of this code?"
            
        return question, options
    
    def _clean_markdown(self, markdown: str) -> str:
        """Clean markdown content for better web display."""
        # Remove any problematic HTML that might not render well
        # Keep this simple for now, can be expanded as needed
        
        # Fix any broken HTML tags
        markdown = re.sub(r'<div[^>]*style="[^"]*"[^>]*>', '<div class="custom-style">', markdown)
        
        return markdown

def main():
    parser = argparse.ArgumentParser(description='Convert Jupyter notebooks to interactive markdown')
    parser.add_argument('input', help='Input .ipynb file path')
    parser.add_argument('-o', '--output', help='Output markdown file path')
    parser.add_argument('-t', '--title', help='Notebook title')
    parser.add_argument('-d', '--description', help='Notebook description')
    parser.add_argument('--difficulty', choices=['beginner', 'intermediate', 'advanced'], 
                       default='beginner', help='Difficulty level')
    parser.add_argument('--no-reflection', action='store_true', 
                       help='Skip adding reflection question prompts')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    if not args.input.endswith('.ipynb'):
        print(f"❌ Error: Input file must be a .ipynb file")
        sys.exit(1)
    
    # Generate output path if not provided
    if not args.output:
        input_path = Path(args.input)
        args.output = str(input_path.parent / f"{input_path.stem}.md")
    
    # Convert notebook
    converter = NotebookConverter()
    
    try:
        converter.convert_notebook(
            notebook_path=args.input,
            output_path=args.output,
            title=args.title,
            description=args.description,
            difficulty=args.difficulty,
            add_reflection_prompts=not args.no_reflection
        )
        
        print(f"🎉 Successfully converted '{args.input}' to interactive markdown!")
        print(f"📁 Output: {args.output}")
        
    except Exception as e:
        print(f"❌ Error converting notebook: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
