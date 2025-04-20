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

        try {
            const response = await fetch('http://localhost:5000/api/evaluate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt, model })
            });

            const data = await response.json();
            if (data.error) {
                alert(`Error: ${data.error}`);
                return;
            }

            resultsSection.classList.remove('hidden');
            overallFeedbackText.textContent = data.feedback;
            clarityScoreSpan.textContent = data.breakdown.clarity;
            specificityScoreSpan.textContent = data.breakdown.specificity;
            contextScoreSpan.textContent = data.breakdown.context;
            taskScoreSpan.textContent = data.breakdown.task;
            alignmentScoreSpan.textContent = data.breakdown.alignment;

            renderBarChart(graphContainers.clarity, data.breakdown.clarity, 20, 'Clarity');
            renderBarChart(graphContainers.specificity, data.breakdown.specificity, 20, 'Specificity');
            renderBarChart(graphContainers.context, data.breakdown.context, 20, 'Context');
            renderBarChart(graphContainers.task, data.breakdown.task, 20, 'Task');
            renderBarChart(graphContainers.alignment, data.breakdown.alignment, 20, 'Alignment');
        } catch (err) {
            console.error('Failed to fetch:', err);
            alert('Failed to connect to backend. Is it running?');
        }
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

        container.style.position = 'relative';
        container.appendChild(bar);
        container.appendChild(labelElement);
    }
});
