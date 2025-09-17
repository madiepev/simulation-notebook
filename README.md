# Interactive Notebook Template System

This repository provides a lightweight template system for converting Jupyter notebooks into interactive GitHub Pages simulations that feel like running real notebooks.

## 🌟 Features

- **🏃‍♂️ Simulated execution**: Code cells execute with realistic timing and output animation
- **📊 Progressive display**: Outputs appear with typing effects
- **🤔 Reflection questions**: Multiple choice questions after key code blocks
- **📈 Progress tracking**: Visual progress bar and execution state
- **📱 Mobile responsive**: Works on all device sizes
- **⚡ Lightweight**: Minimal dependencies, fast loading
- **🎨 Jupyter-like UI**: Familiar interface for notebook users

## 🚀 Quick Start

### 1. Convert a Notebook

```bash
# Convert single notebook
python3 scripts/convert_notebook.py notebooks/your-notebook.ipynb

# Convert with custom options
python3 scripts/convert_notebook.py notebooks/your-notebook.ipynb \
  -t "Custom Title" \
  -d "Custom description" \
  --difficulty advanced

# Convert all notebooks
./scripts/convert_all.sh
```

### 2. Setup GitHub Pages

1. Enable GitHub Pages in repository settings
2. Set source to `docs` folder
3. Push the `docs` directory

### 3. Customize Reflection Questions

Edit the generated markdown files in `docs/_notebooks/` to customize:

```html
<div class="reflection-question" data-question-id="q1">
<h4>🤔 Reflection Question</h4>
<p>What does this code accomplish?</p>
<div class="choices">
<label><input type="radio" name="q1" value="a"> Option A</label>
<label><input type="radio" name="q1" value="b"> Option B</label>
<label><input type="radio" name="q1" value="c"> Option C</label>
</div>
<div class="answer" data-correct="a">
<p><strong>Correct!</strong> Explanation here.</p>
</div>
</div>
```

## 📁 Structure

```
├── docs/                    # GitHub Pages site
│   ├── _layouts/           # Jekyll templates
│   ├── _notebooks/         # Converted notebooks
│   ├── assets/            # CSS & JavaScript
│   └── _config.yml        # Site configuration
├── notebooks/             # Original .ipynb files
├── scripts/              # Conversion utilities
└── README.md
```

## 🎯 Interactive Features

### Code Execution Simulation
- Click "▶ Run" buttons to execute cells
- Realistic execution delays (500ms - 2s)
- Progressive output display with typing animation
- Execution state tracking (not started → executing → completed)

### Reflection Questions
- Automatically generated based on code content
- Multiple choice format
- Immediate feedback on answers
- Customizable explanations

### User Experience
- **Keyboard shortcuts**: `Ctrl/Cmd + Enter` to run current cell
- **Progress tracking**: Visual progress bar shows completion
- **Mobile friendly**: Touch-optimized interface
- **Accessible**: Screen reader compatible

## 🛠️ Customization

### Styling
Modify `docs/assets/notebook.css` to customize:
- Color scheme
- Layout spacing
- Animation timing
- Mobile responsiveness

### Functionality
Extend `docs/assets/notebook.js` to add:
- New interaction patterns
- Additional output types
- Custom question formats
- Analytics tracking

### Content
Edit the conversion script `scripts/convert_notebook.py` to:
- Change question generation logic
- Modify output processing
- Add custom cell types
- Enhance markdown processing

## 📚 Markdown Format

The system uses a structured markdown format:

```markdown
---
layout: notebook
title: "Notebook Title"
description: "Description"
difficulty: beginner|intermediate|advanced
---

## Regular Markdown
Normal markdown content renders as documentation.

## Interactive Code Cells
<div class="code-cell" data-cell-id="cell-1">
<div class="code-input">
```python
print("Hello World")
```
</div>
<div class="code-output" data-expected-output="text">
<pre class="output-text">Hello World</pre>
</div>
</div>

## Reflection Questions
<div class="reflection-question" data-question-id="q1">
<h4>🤔 Reflection Question</h4>
<p>Question text here?</p>
<div class="choices">
<label><input type="radio" name="q1" value="a"> Option A</label>
<label><input type="radio" name="q1" value="b"> Option B</label>
</div>
<div class="answer" data-correct="a">
<p><strong>Correct!</strong> Explanation.</p>
</div>
</div>
```

## 🔧 Development

### Local Testing
```bash
# Install Jekyll (if not already installed)
gem install bundler jekyll

# Serve locally
cd docs
jekyll serve

# Open http://localhost:4000
```

### Adding New Features
1. Modify CSS in `docs/assets/notebook.css`
2. Update JavaScript in `docs/assets/notebook.js`
3. Enhance conversion script if needed
4. Test with sample notebooks

## 📖 Examples

See the converted notebooks in `docs/_notebooks/` for examples of:
- Data science workflows
- Machine learning tutorials  
- Programming concepts
- Analysis walkthroughs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test with sample notebooks
5. Submit a pull request

## 📄 License

MIT License - feel free to use and modify for your educational content!

## 💡 Tips

- **Keep code cells focused**: Each cell should demonstrate one concept
- **Write clear questions**: Questions should test understanding, not memorization
- **Test on mobile**: Many learners use mobile devices
- **Provide context**: Include enough explanation in markdown cells
- **Use realistic outputs**: Make the simulation feel authentic

## 🐛 Troubleshooting

### Common Issues

**Conversion fails**: Check notebook format and ensure valid JSON
**JavaScript errors**: Verify cell IDs are unique
**Styling issues**: Check CSS class names match HTML structure
**Questions don't work**: Ensure question IDs are unique

### Getting Help

1. Check the [issues page](../../issues) for common problems
2. Review the template format documentation
3. Test with the included example notebook
4. Open an issue with details about your problem
