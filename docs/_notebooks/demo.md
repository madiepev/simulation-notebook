---
layout: notebook
title: "Demo: Interactive Features"
description: "Test the interactive notebook simulation features"
difficulty: beginner
---

# Welcome to Interactive Notebooks! 

This is a demo of the interactive features. Try clicking the "Run" buttons below to see the simulation in action.

## Basic Code Execution

<div class="code-cell" data-cell-id="demo-1">
<div class="code-input">
```python
# Simple hello world example
print("Welcome to interactive notebooks!")
print("This feels just like Jupyter!")
```
</div>
<div class="code-output" data-expected-output="text">
<pre class="output-text">Welcome to interactive notebooks!
This feels just like Jupyter!</pre>
</div>
</div>

<div class="reflection-question" data-question-id="demo-q1">
<h4>🤔 Reflection Question</h4>
<p>What happens when you run the cell above?</p>
<div class="choices">
<label><input type="radio" name="demo-q1" value="a"> Text is printed to the output</label>
<label><input type="radio" name="demo-q1" value="b"> A file is created</label>
<label><input type="radio" name="demo-q1" value="c"> Nothing happens</label>
<label><input type="radio" name="demo-q1" value="d"> An error occurs</label>
</div>
<div class="answer" data-correct="a">
<p><strong>Correct!</strong> The print statements output text that appears below the code cell.</p>
</div>
</div>

## Working with Data

<div class="code-cell" data-cell-id="demo-2">
<div class="code-input">
```python
# Create some sample data
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]

print("Original numbers:", numbers)
print("Squared numbers:", squared)
print("Sum of squares:", sum(squared))
```
</div>
<div class="code-output" data-expected-output="text">
<pre class="output-text">Original numbers: [1, 2, 3, 4, 5]
Squared numbers: [1, 4, 9, 16, 25]
Sum of squares: 55</pre>
</div>
</div>

<div class="reflection-question" data-question-id="demo-q2">
<h4>🤔 Reflection Question</h4>
<p>What programming concept is demonstrated in the line `squared = [x**2 for x in numbers]`?</p>
<div class="choices">
<label><input type="radio" name="demo-q2" value="a"> List comprehension</label>
<label><input type="radio" name="demo-q2" value="b"> Dictionary creation</label>
<label><input type="radio" name="demo-q2" value="c"> Function definition</label>
<label><input type="radio" name="demo-q2" value="d"> Loop iteration</label>
</div>
<div class="answer" data-correct="a">
<p><strong>Excellent!</strong> This is a list comprehension - a concise way to create lists in Python by applying an operation to each element of another list.</p>
</div>
</div>

## Function Definition

<div class="code-cell" data-cell-id="demo-3">
<div class="code-input">
```python
def greet_user(name, language="English"):
    """Greet a user in different languages"""
    greetings = {
        "English": f"Hello, {name}!",
        "Spanish": f"¡Hola, {name}!",
        "French": f"Bonjour, {name}!",
        "German": f"Hallo, {name}!"
    }
    return greetings.get(language, f"Hello, {name}!")

# Test the function
print(greet_user("Alice"))
print(greet_user("Bob", "Spanish"))
print(greet_user("Charlie", "French"))
```
</div>
<div class="code-output" data-expected-output="text">
<pre class="output-text">Hello, Alice!
¡Hola, Bob!
Bonjour, Charlie!</pre>
</div>
</div>

<div class="reflection-question" data-question-id="demo-q3">
<h4>🤔 Reflection Question</h4>
<p>What would happen if you called `greet_user("David", "Italian")`?</p>
<div class="choices">
<label><input type="radio" name="demo-q3" value="a"> Returns "Hello, David!" (default)</label>
<label><input type="radio" name="demo-q3" value="b"> Raises an error</label>
<label><input type="radio" name="demo-q3" value="c"> Returns "Ciao, David!"</label>
<label><input type="radio" name="demo-q3" value="d"> Returns None</label>
</div>
<div class="answer" data-correct="a">
<p><strong>That's right!</strong> The `dict.get()` method returns the default value "Hello, David!" when "Italian" is not found in the greetings dictionary.</p>
</div>
</div>

## Try These Features:

1. **🖱️ Click Run buttons** to execute cells in sequence
2. **⌨️ Use Ctrl/Cmd + Enter** to run the currently visible cell
3. **📊 Watch the progress bar** at the top of the page
4. **❓ Answer reflection questions** to test your understanding
5. **🔄 Use the Reset button** in the navigation to start over

---

## Navigation Controls

- **🏠 Home**: Return to the main page
- **▶ Run All**: Execute all cells automatically  
- **🔄 Reset**: Reset all cells and questions to initial state

Have fun exploring! 🎉
