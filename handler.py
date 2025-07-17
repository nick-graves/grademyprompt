import json
from core import evaluate_prompt, generate_questions, refine_prompt



def lambda_handler(event, context):

    path = event.get("rawPath") or event.get("resource") or ""
    body = json.loads(event.get("body","{}"))

    cors = {
      "Access-Control-Allow-Origin":  "*",
      "Access-Control-Allow-Methods": "OPTIONS,POST",
      "Access-Control-Allow-Headers": "Content-Type"
    }


    if event["requestContext"]["http"]["method"] == "OPTIONS":
        return {"statusCode": 200, "headers": cors}


    if path == "/default/promptinsight/evaluate":
        return evaluate(body)
    elif path == "/default/promptinsight/generate-questions":
        return questions(body)
    elif path == "/default/promptinsight/refine-prompt":
        return refine(body)
    else:
        return error(404, "Not Found")



def evaluate(data):
    prompt = data.get("prompt")
    if not prompt:
        return error(400, "Prompt is required.")
    
    try:
        full, score, feedback, breakdown = evaluate_prompt(prompt, data.get("model"))
        return ok({
            "score": score,
            "feedback": feedback,
            "breakdown": breakdown,
            "raw": full
        })
    except Exception as e:
        return error(500, str(e))


def questions(data):
    prompt = data.get("prompt")
    feedback = data.get("feedback")

    if not prompt or not feedback:
        return error(400, "Prompt and feedback are required.")
    
    try:
        questions = generate_questions(prompt, feedback)
        return ok({"questions": questions})
    except Exception as e:
        return error(500, str(e))


def refine(data):
    prompt = data.get("prompt")
    feedback = data.get("feedback")
    qa_pairs = data.get("qa_pairs")
    user_selected_model = data.get("model")

    if not prompt or not feedback or not qa_pairs or not user_selected_model:
        return error(400, "Prompt, feedback, QA pairs, and model are required.")

    try:
        refined = refine_prompt(prompt, feedback, qa_pairs, user_selected_model)
        return ok({"refined": refined})
    except Exception as e:
        return error(500, str(e))



def ok(body):
    return {"statusCode": 200, "body": json.dumps(body)}

def error(code, msg):
    return {"statusCode": code, "body": json.dumps({"error": msg})}