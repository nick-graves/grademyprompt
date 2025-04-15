document.addEventListener('DOMContentLoaded', () => {
    const gradeButton = document.getElementById('grade-button');
    const promptInput = document.getElementById('prompt-input');
    const modelSelect = document.getElementById('model-select');
    const resultsSection = document.getElementById('results-section');
    const clarityScoreSpan = document.getElementById('clarity-score');
    const specificityScoreSpan = document.getElementById('specificity-score');
    const contextScoreSpan = document.getElementById('context-score');
    const taskScoreSpan = document.getElementById('task-score');
    const alignmentScoreSpan = document.getElementById('alignment-score');
    const overallFeedbackText = document.getElementById('overall-feedback-text');
    const graphContainers = {
        clarity: document.getElementById('clarity-graph'),
        specificity: document.getElementById('specificity-graph'),
        context: document.getElementById('context-graph'),
        task: document.getElementById('task-graph'),
        alignment: document.getElementById('alignment-graph'),
    };

    gradeButton.addEventListener('click', async () => {
        const prompt = promptInput.value;
        const model = modelSelect.value;

        if (!prompt || !model) {
            alert('Please enter a prompt and select a model.');
            return;
        }

        // Simulate sending data to the backend and receiving results
        // In a real application, you would use fetch or axios to make an API call to your Node.js backend
        resultsSection.classList.remove('hidden');
        overallFeedbackText.textContent = "This is some example overall feedback on your prompt.";
        clarityScoreSpan.textContent = '15';
        specificityScoreSpan.textContent = '18';
        contextScoreSpan.textContent = '12';
        taskScoreSpan.textContent = '19';
        alignmentScoreSpan.textContent = '16';

        // Example of rendering basic bar charts (you'd likely use a library like Chart.js or D3.js for more sophisticated graphs)
        renderBarChart(graphContainers.clarity, 15, 20, 'Clarity');
        renderBarChart(graphContainers.specificity, 18, 20, 'Specificity');
        renderBarChart(graphContainers.context, 12, 20, 'Context');
        renderBarChart(graphContainers.task, 19, 20, 'Task');
        renderBarChart(graphContainers.alignment, 16, 20, 'Alignment');
    });

    function renderBarChart(container, score, maxScore, label) {
        container.innerHTML = ''; // Clear previous content
        const bar = document.createElement('div');
        bar.style.backgroundColor = '#007bff';
        bar.style.height = '80%';
        bar.style.width = `${(score / maxScore) * 100}%`;
        bar.style.borderRadius = '4px';
        bar.style.display = 'flex';
        bar.style.justifyContent = 'center';
        bar.style.alignItems = 'center';
        bar.style.color = 'white';
        bar.textContent = score;

        const labelElement = document.createElement('div');
        labelElement.style.position = 'absolute';
        labelElement.style.bottom = '-20px';
        labelElement.style.left = '50%';
        labelElement.style.transform = 'translateX(-50%)';
        labelElement.style.color = '#555';
        labelElement.textContent = label;

        container.style.position = 'relative'; // For absolute positioning of the label
        container.appendChild(bar);
        container.appendChild(labelElement);
    }
});