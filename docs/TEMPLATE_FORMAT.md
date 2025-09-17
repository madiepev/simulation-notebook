# Interactive Notebook Template Format

This document describes the markdown format used to create interactive notebook simulations on GitHub Pages.

## Markdown Structure

Each notebook is a markdown file with specific conventions:

### 1. Frontmatter
```yaml
---
layout: notebook
title: "Notebook Title"
description: "Brief description"
---
```

### 2. Markdown Cells
Regular markdown content - no special syntax needed.

### 3. Code Cells
```html
<div class="code-cell" data-cell-id="cell-1">
<div class="code-input">
```python
# Your Python code here
import pandas as pd
print("Hello World")
```
</div>
<div class="code-output" data-expected-output="text">
Hello World
</div>
</div>
```

### 4. Reflection Questions
```html
<div class="reflection-question" data-question-id="q1">
<h4>🤔 Reflection Question</h4>
<p>What does this code accomplish?</p>
<div class="choices">
<label><input type="radio" name="q1" value="a"> Option A: Imports a library</label>
<label><input type="radio" name="q1" value="b"> Option B: Prints a message</label>
<label><input type="radio" name="q1" value="c"> Option C: Both A and B</label>
</div>
<div class="answer" data-correct="c">
<p><strong>Correct!</strong> The code both imports pandas and prints "Hello World".</p>
</div>
</div>
```

## Data Attributes

- `data-cell-id`: Unique identifier for each code cell
- `data-expected-output`: Type of output (text, html, image, etc.)
- `data-question-id`: Unique identifier for reflection questions
- `data-correct`: The correct answer for multiple choice questions

## Special Features

1. **Simulated Execution**: Code cells show a "Run" button and simulate execution
2. **Progressive Output**: Output appears with typing animation
3. **Reflection Questions**: Multiple choice questions after code blocks
4. **Progress Tracking**: Track which cells have been "executed"
5. **Mobile Responsive**: Works on all device sizes
