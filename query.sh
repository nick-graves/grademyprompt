#!/bin/bash

# get user prompt
echo "Enter the AI prompt you'd like to evaluate:"
read -r user_prompt

# create full prompt file
TEMPLATE_FILE="prompt.txt"
TMP_PROMPT_FILE="full_prompt.txt"

# combine prompt and input
escaped_prompt=$(printf '%s\n' "$user_prompt" | sed 's/"/\\"/g')
sed "s/{{user_input_here}}/$escaped_prompt/" "$TEMPLATE_FILE" > "$TMP_PROMPT_FILE"

# run query
echo ""
echo "Grading your prompt..."
echo "----------------------"
ollama run deepseek-r1:8b < "$TMP_PROMPT_FILE"