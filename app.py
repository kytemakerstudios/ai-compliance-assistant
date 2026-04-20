import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

from retrieval import retrieve_context
from prompts import system_prompt
from logger import log_interaction

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------- Guardrails --------
RATE_LIMIT = 5
WINDOW = 60
user_requests = {}

MAX_INPUT_LENGTH = 300


def is_rate_limited(user_id="default"):
    now = time.time()

    if user_id not in user_requests:
        user_requests[user_id] = []

    user_requests[user_id] = [
        t for t in user_requests[user_id] if now - t < WINDOW
    ]

    if len(user_requests[user_id]) >= RATE_LIMIT:
        return True

    user_requests[user_id].append(now)
    return False


# -------- Main Logic --------
def ask_agent(user_query, user_role):

    if len(user_query) > MAX_INPUT_LENGTH:
        return {
            "answer": "Input too long.",
            "risk_level": "low",
            "reasoning": "Prevents abuse.",
            "role_guidance": "Shorten query.",
            "sources": []
        }

    if is_rate_limited():
        return {
            "answer": "Too many requests. Please wait.",
            "risk_level": "low",
            "reasoning": "Rate limit exceeded.",
            "role_guidance": "Slow down.",
            "sources": []
        }

    context = retrieve_context(user_query)

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": json.dumps({
                "role": user_role,
                "question": user_query,
                "context": context
            })
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    log_interaction(user_query, result)

    return result
