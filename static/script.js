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
    const totalScoreSpan = document.getElementById('total-score');
    const loadingSpinner = document.getElementById('loading-spinner');
    const loadingMessage = document.getElementById('loading-message');

    const rewriteButton = document.getElementById('rewrite-button');
    const qaSection = document.getElementById('qa-section');
    const qaForm = document.getElementById('qa-form');
    const submitAnswersButton = document.getElementById('submit-answers-button');
    const refinedPromptOutput = document.getElementById('refined-prompt-output');
    const refinedPromptSection = document.getElementById('refined-prompt-section');

    let scoreChart = null;

    function showLoading(message = "Loading...") {
        loadingMessage.textContent = message;
        loadingSpinner.classList.remove('hidden');
    }

    function hideLoading() {
        loadingSpinner.classList.add('hidden');
    }

    gradeButton.addEventListener('click', async () => {
        const prompt = promptInput.value;
        const model = modelSelect.value;

        if (!prompt || !model) {
            alert('Please enter a prompt and select a model.');
            return;
        }

        showLoading("Evaluating prompt...");

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
            totalScoreSpan.textContent = data.score;

            const ctx = document.getElementById('scoreChart').getContext('2d');

            if (scoreChart) {
                scoreChart.destroy();
            }

            scoreChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Clarity', 'Specificity', 'Context', 'Task', 'Alignment'],
                    datasets: [{
                        label: 'Score (out of 20)',
                        data: [
                            data.breakdown.clarity,
                            data.breakdown.specificity,
                            data.breakdown.context,
                            data.breakdown.task,
                            data.breakdown.alignment
                        ],
                        backgroundColor: '#007bff'
                    }]
                },
                options: {
                    responsive: true,
                    animation: {
                        duration: 700
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 20,
                            title: {
                                display: true,
                                text: 'Score'
                            },
                            ticks: {
                                stepSize: 5
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });

        } catch (err) {
            console.error('Failed to fetch:', err);
            alert('Failed to connect to backend. Is it running?');
        } finally {
            hideLoading();
        }

        gradeButton.style.display = 'none';

    });

    rewriteButton.addEventListener('click', async () => {
        const prompt = promptInput.value;
        const feedback = overallFeedbackText.textContent;

        if (!prompt || !feedback) {
            alert("Prompt and feedback are required to generate clarification questions.");
            return;
        }

        showLoading("Generating clarifying questions...");

        try {
            const response = await fetch('http://localhost:5000/api/generate-questions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt, feedback })
            });

            const data = await response.json();
            if (data.error) {
                alert(`Error: ${data.error}`);
                return;
            }

            const questions = data.questions;
            console.log("Generated questions:", questions);

            qaForm.innerHTML = '';
            qaSection.classList.remove('hidden');

            questions.forEach((question, index) => {
                const item = document.createElement('div');
                item.classList.add('qa-item');

                const label = document.createElement('label');
                label.textContent = question;
                label.setAttribute('for', `answer-${index}`);

                const textarea = document.createElement('textarea');
                textarea.setAttribute('id', `answer-${index}`);
                textarea.setAttribute('name', `answer-${index}`);

                item.appendChild(label);
                item.appendChild(textarea);
                qaForm.appendChild(item);
            });

        } catch (err) {
            console.error('Failed to generate questions:', err);
            alert('Something went wrong generating questions.');
        } finally {
            hideLoading();
        }

        rewriteButton.style.display = 'none';
    });

    submitAnswersButton.addEventListener('click', async () => {
        const prompt = promptInput.value;
        const model = modelSelect.value;
        const feedback = overallFeedbackText.textContent;

        const answers = [];
        const formElements = qaForm.elements;

        for (let i = 0; i < formElements.length; i++) {
            const el = formElements[i];
            if (el.tagName === 'TEXTAREA') {
                const question = el.previousSibling.textContent;
                const answer = el.value;
                answers.push({ question, answer });
            }
        }

        showLoading("Rewriting your prompt...");

        try {
            const response = await fetch('http://localhost:5000/api/refine-prompt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    prompt,
                    feedback,
                    qa_pairs: answers,
                    model: model
                })
            });

            const data = await response.json();
            if (data.error) {
                alert(`Error: ${data.error}`);
                return;
            }

            refinedPromptOutput.textContent = data.refined_prompt;
            refinedPromptSection.classList.remove('hidden');
        } catch (err) {
            console.error('Failed to refine prompt:', err);
            alert('Something went wrong generating the refined prompt.');
        } finally {
            hideLoading();
        }

        submitAnswersButton.style.display = 'none';
    });

});
