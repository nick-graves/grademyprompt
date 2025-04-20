# Prompt Insights: AI Prompt Grader & Rewriter

**Prompt Insights** is a locally-run AI tool designed to help users craft high-quality prompts for large language models (LLMs). It provides an interactive interface to:

- Grade prompts on five critical dimensions  
- Generate clarifying questions to improve vague prompts  
- Rewrite prompts based on user feedback and answers  
- Visualize scores with interactive charts

Built with a Flask backend and a modern JavaScript UI, Prompt Insights integrates seamlessly with **locally-hosted LLMs** like `llama3:8b` via [Ollama](https://ollama.com).

---

## Project Structure

```
├── backend.py              # Flask server exposing API endpoints
├── core.py                 # Prompt evaluation, question generation, and rewriting logic
├── interface.py            # Handles interaction with the local LLM via subprocess
├── templates/
│   └── index.html          # Main frontend page
├── static/
│   ├── script.js           # Frontend logic, chart rendering, and prompt rewriting flow
│   └── style.css           # UI styling and layout
├── prompts/
│   ├── evaluate_prompt.txt
│   ├── generate_questions.txt
│   └── refine_prompt.txt
```

---

## Features

### Prompt Evaluation
- Prompts are scored on:
  - Clarity
  - Specificity
  - Context/Background
  - Task Definition
  - Model Alignment
- Each category is scored out of 20, and results are displayed both numerically and graphically.

### Clarifying Question Generation
- After evaluation, the tool can ask follow-up questions to gather necessary context for improvement.

### Prompt Rewriting
- Using the original prompt, feedback, and user answers, a refined prompt is generated using a separate LLM prompt template.

### Interactive Frontend
- Clean UI for input and results
- Chart.js integration for real-time score visualization
- Loading spinner and step-by-step flow for seamless interaction

---

## Local Model Integration

This project uses **Ollama** to run LLMs locally via subprocess. You’ll need:

- Ollama installed: [https://ollama.com](https://ollama.com)
- A supported model pulled (e.g., `llama3.1:8b`, etc.)

```bash
ollama pull llama3.1:8b
```

---

## Running the Application

### 1. Install Python dependencies

```bash
pip install flask flask-cors
```

> (You may use a virtual environment if preferred.)

### 2. Start the backend

```bash
python backend.py
```

This will launch the Flask server on `http://localhost:5000`.

### 3. Open the Frontend

Open your browser and visit:  
`http://localhost:5000`

From there, you can:
- Enter a prompt
- Select an intended model
- Grade it
- Generate questions
- Submit answers
- Get a refined prompt — all in a clean UI

---

## Configuration

You can edit the behavior of the model by modifying these templates:

- `prompts/evaluate_prompt.txt`
- `prompts/generate_questions.txt`
- `prompts/refine_prompt.txt`

Placeholders like `{{user_input_here}}`, `{{feedback}}`, and `{{qa_pairs}}` will be dynamically filled by the app.

---

## Example Use Case

**Original Prompt:**  
"Summarize this article."

The tool may respond:
- **Score:** 42/100
- **Feedback:** Lacks specificity and context. What article? What tone or format?

Then ask:
- “What kind of article is being summarized?”
- “Who is the intended audience?”

You answer, and the tool rewrites the prompt as:  
"Summarize the attached New York Times opinion article for a general audience in under 100 words, using a neutral tone."

---

## Future Enhancements (Ideas)

- Prompt version comparison view
- Copy-to-clipboard and save features
- Dark mode UI
- Offline support with Web Workers
- Support for multiple local models

---

## License

MIT License – free to use, modify, and share.

---

## Acknowledgements

- Inspired by OpenAI's best practices for prompt engineering
- Built using [Ollama](https://ollama.com), [Flask](https://flask.palletsprojects.com), and [Chart.js](https://www.chartjs.org/)