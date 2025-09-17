/**
 * Interactive Notebook JavaScript
 * Simulates Jupyter notebook execution and handles reflection questions
 */

class InteractiveNotebook {
  constructor() {
    this.executedCells = new Set();
    this.totalCells = 0;
    this.init();
  }

  init() {
    this.setupCells();
    this.setupReflectionQuestions();
    this.setupProgressBar();
    this.bindEvents();
  }

  setupCells() {
    const codeCells = document.querySelectorAll('.code-cell');
    this.totalCells = codeCells.length;
    
    codeCells.forEach((cell, index) => {
      const cellId = cell.dataset.cellId || `cell-${index + 1}`;
      cell.dataset.cellId = cellId;
      
      // Add cell header if not present
      if (!cell.querySelector('.cell-header')) {
        const header = this.createCellHeader(index + 1, cellId);
        cell.insertBefore(header, cell.firstChild);
      }
      
      // Hide output initially
      const output = cell.querySelector('.code-output');
      if (output) {
        output.classList.remove('show');
      }
    });
  }

  createCellHeader(cellNumber, cellId) {
    const header = document.createElement('div');
    header.className = 'cell-header';
    header.innerHTML = `
      <span class="cell-number">In [${cellNumber}]:</span>
      <div>
        <span class="execution-indicator">Executing...</span>
        <button class="run-button" onclick="notebook.executeCell('${cellId}')">
          ▶ Run
        </button>
      </div>
    `;
    return header;
  }

  setupReflectionQuestions() {
    const questions = document.querySelectorAll('.reflection-question');
    questions.forEach(question => {
      const choices = question.querySelectorAll('input[type="radio"]');
      choices.forEach(choice => {
        choice.addEventListener('change', () => {
          this.handleQuestionAnswer(question, choice);
        });
      });
    });
  }

  setupProgressBar() {
    if (!document.querySelector('.progress-container')) {
      const progressContainer = document.createElement('div');
      progressContainer.className = 'progress-container';
      progressContainer.innerHTML = `
        <div class="progress-bar">
          <div class="progress-fill"></div>
        </div>
        <div class="progress-text">0 of ${this.totalCells} cells executed</div>
      `;
      
      const container = document.querySelector('.notebook-container');
      container.insertBefore(progressContainer, container.firstChild);
    }
    
    this.updateProgress();
  }

  bindEvents() {
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey || e.metaKey) {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.executeCurrentCell();
        }
      }
    });

    // Auto-scroll to executed cells
    window.addEventListener('scroll', this.throttle(() => {
      this.updateVisibleCells();
    }, 100));
  }

  async executeCell(cellId) {
    const cell = document.querySelector(`[data-cell-id="${cellId}"]`);
    if (!cell) return;

    const runButton = cell.querySelector('.run-button');
    const indicator = cell.querySelector('.execution-indicator');
    const output = cell.querySelector('.code-output');

    // Prevent multiple executions
    if (cell.classList.contains('executing')) return;

    // Mark as executing
    cell.classList.add('executing');
    runButton.disabled = true;
    indicator.classList.add('show');

    try {
      // Simulate execution delay
      await this.delay(this.getRandomDelay());

      // Show output with typing animation
      if (output) {
        await this.animateOutput(output);
      }

      // Mark as executed
      cell.classList.remove('executing');
      cell.classList.add('executed');
      this.executedCells.add(cellId);
      
      // Update button text
      runButton.textContent = '✓ Executed';
      runButton.style.background = '#28a745';

    } catch (error) {
      console.error('Cell execution error:', error);
      cell.classList.remove('executing');
      
    } finally {
      indicator.classList.remove('show');
      runButton.disabled = false;
      this.updateProgress();
    }
  }

  async animateOutput(outputElement) {
    const expectedOutput = outputElement.dataset.expectedOutput || 'text';
    const outputContent = outputElement.innerHTML;
    
    outputElement.innerHTML = '<pre class="output-text"><span class="loading-dots">Executing</span></pre>';
    outputElement.classList.add('show');
    
    // Simulate processing time
    await this.delay(800);
    
    // Clear loading and show content
    outputElement.innerHTML = outputContent;
    
    // Add typing animation for text output
    if (expectedOutput === 'text') {
      const textElement = outputElement.querySelector('pre');
      if (textElement) {
        await this.typeText(textElement, textElement.textContent);
      }
    }
  }

  async typeText(element, text) {
    element.textContent = '';
    for (let i = 0; i < text.length; i++) {
      element.textContent += text.charAt(i);
      await this.delay(20 + Math.random() * 30); // Variable typing speed
    }
  }

  handleQuestionAnswer(questionElement, selectedChoice) {
    const questionId = questionElement.dataset.questionId;
    const correctAnswer = questionElement.querySelector('.answer').dataset.correct;
    const choices = questionElement.querySelectorAll('input[type="radio"]');
    const answerElement = questionElement.querySelector('.answer');
    
    // Clear previous selections
    choices.forEach(choice => {
      choice.parentElement.classList.remove('selected', 'correct', 'incorrect');
    });
    
    // Mark selected choice
    selectedChoice.parentElement.classList.add('selected');
    
    // Check if answer is correct
    if (selectedChoice.value === correctAnswer) {
      selectedChoice.parentElement.classList.add('correct');
      answerElement.classList.remove('incorrect');
    } else {
      selectedChoice.parentElement.classList.add('incorrect');
      answerElement.classList.add('incorrect');
      
      // Also highlight the correct answer
      const correctChoice = questionElement.querySelector(`input[value="${correctAnswer}"]`);
      if (correctChoice) {
        correctChoice.parentElement.classList.add('correct');
      }
    }
    
    // Show answer explanation
    answerElement.classList.add('show');
    
    // Smooth scroll to answer
    setTimeout(() => {
      answerElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
  }

  executeCurrentCell() {
    // Find the currently focused or visible cell
    const cells = document.querySelectorAll('.code-cell');
    for (let cell of cells) {
      const rect = cell.getBoundingClientRect();
      if (rect.top >= 0 && rect.top <= window.innerHeight / 2) {
        const cellId = cell.dataset.cellId;
        this.executeCell(cellId);
        break;
      }
    }
  }

  updateProgress() {
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.progress-text');
    
    if (progressFill && progressText) {
      const percentage = (this.executedCells.size / this.totalCells) * 100;
      progressFill.style.width = `${percentage}%`;
      progressText.textContent = `${this.executedCells.size} of ${this.totalCells} cells executed`;
    }
  }

  updateVisibleCells() {
    const cells = document.querySelectorAll('.code-cell');
    cells.forEach(cell => {
      const rect = cell.getBoundingClientRect();
      const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
      
      if (isVisible) {
        cell.classList.add('visible');
      } else {
        cell.classList.remove('visible');
      }
    });
  }

  getRandomDelay() {
    // Random delay between 500ms and 2000ms to simulate realistic execution
    return 500 + Math.random() * 1500;
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  throttle(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Public methods for manual control
  executeAllCells() {
    const cells = document.querySelectorAll('.code-cell');
    cells.forEach((cell, index) => {
      setTimeout(() => {
        this.executeCell(cell.dataset.cellId);
      }, index * 1000); // Stagger execution
    });
  }

  resetNotebook() {
    this.executedCells.clear();
    
    const cells = document.querySelectorAll('.code-cell');
    cells.forEach(cell => {
      cell.classList.remove('executed', 'executing');
      
      const output = cell.querySelector('.code-output');
      if (output) {
        output.classList.remove('show');
      }
      
      const runButton = cell.querySelector('.run-button');
      if (runButton) {
        runButton.textContent = '▶ Run';
        runButton.style.background = '';
        runButton.disabled = false;
      }
    });
    
    const questions = document.querySelectorAll('.reflection-question');
    questions.forEach(question => {
      const choices = question.querySelectorAll('input[type="radio"]');
      choices.forEach(choice => {
        choice.checked = false;
        choice.parentElement.classList.remove('selected', 'correct', 'incorrect');
      });
      
      const answer = question.querySelector('.answer');
      if (answer) {
        answer.classList.remove('show', 'incorrect');
      }
    });
    
    this.updateProgress();
  }

  // Export notebook state
  getNotebookState() {
    return {
      executedCells: Array.from(this.executedCells),
      answers: this.getAnswers()
    };
  }

  getAnswers() {
    const answers = {};
    const questions = document.querySelectorAll('.reflection-question');
    questions.forEach(question => {
      const questionId = question.dataset.questionId;
      const selected = question.querySelector('input[type="radio"]:checked');
      if (selected) {
        answers[questionId] = selected.value;
      }
    });
    return answers;
  }
}

// Initialize when DOM is loaded
let notebook;
document.addEventListener('DOMContentLoaded', () => {
  notebook = new InteractiveNotebook();
  
  // Add global controls if needed
  console.log('Interactive Notebook initialized');
  console.log('Available commands:');
  console.log('- notebook.executeAllCells() - Execute all cells');
  console.log('- notebook.resetNotebook() - Reset notebook state');
  console.log('- notebook.getNotebookState() - Get current state');
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = InteractiveNotebook;
}
