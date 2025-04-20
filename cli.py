from core import evaluate_prompt, save_to_json, generate_questions, refine_prompt

def main():
    user_model = "llama3.1:8b"
    user_prompt = input("Enter the AI prompt you'd like to evaluate:\n> ")

    print("\n---------------------------------------------------")
    print("Evaluating prompt...\n")
    response, score, feedback = evaluate_prompt(user_prompt, model=user_model)
    print(response)
    print(f"\nScore: {score}/100")
    print(f"Feedback: {feedback}")

    save_to_json(user_prompt, score, feedback)
    print("\nResult saved to results.json")

    refine = input("\nWould you like to refine your prompt based on the feedback? (yes/no): ").strip().lower()
    if refine not in ["yes", "y"]:
        print("Exiting. Have a great day!")
        return

    print("\n---------------------------------------------------")
    print("\nGenerating follow-up questions...\n")
    questions = generate_questions(user_prompt, feedback, model=user_model)
    for q in questions:
        print(q)

    qa_pairs = []
    print("\nPlease answer the following questions to help improve your prompt:\n")
    for q in questions:
        answer = input("> ")
        qa_pairs.append({
            "question": q,
            "answer": answer.strip()
        })

    print("\n---------------------------------------------------")
    print("\nCreating a refined prompt...\n")
    refined_output = refine_prompt(user_prompt, feedback, qa_pairs, model=user_model)
    print("\n---------------------------------------------------")
    print("\nRefined Prompt:\n")
    print(refined_output)

if __name__ == "__main__":
    main()
