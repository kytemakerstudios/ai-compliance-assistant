from dotenv import load_dotenv
import os
import json
import numpy as np
from openai import OpenAI
from knowledge_base import knowledge_base

# 🔑 Load environment variables
load_dotenv()

# 🔑 Pass API key explicitly
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CACHE_FILE = "embeddings_cache.json"


def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def build_policy_text(item):
    return " ".join([
        item["topic"],
        item["rule"],
        " ".join(item["conditions"]),
        " ".join(item["examples"])
    ])


def load_or_create_embeddings():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    updated = False

    for item in knowledge_base:
        key = item["topic"]
        if key not in cache:
            cache[key] = embed_text(build_policy_text(item))
            updated = True

    if updated:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f)

    return cache


embedding_cache = load_or_create_embeddings()


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_context(user_query):
    query_embedding = embed_text(user_query)

    scored = []
    for item in knowledge_base:
        emb = embedding_cache.get(item["topic"])
        if emb:
            score = cosine_similarity(query_embedding, emb)
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [item[1] for item in scored[:3]]
