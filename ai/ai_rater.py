import requests
import json
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:mini"   # change if your model name is different
TIMEOUT = 30  # seconds


def _extract_first_json(text: str) -> Optional[object]:
    """
    Try to find and parse the first JSON object ({...}) or array ([...]) in `text`.
    Returns parsed Python object, or None if nothing found/parsable.
    """
    text = text.strip()
    # quick try: maybe the whole text is JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    def find_balanced(start_char, end_char):
        start = text.find(start_char)
        if start == -1:
            return None
        depth = 0
        for i in range(start, len(text)):
            ch = text[i]
            if ch == start_char:
                depth += 1
            elif ch == end_char:
                depth -= 1
                if depth == 0:
                    # include both start..i
                    return text[start:i+1]
        return None

    # try object first, then array
    candidate = find_balanced("{", "}")
    if candidate:
        try:
            return json.loads(candidate)
        except Exception:
            # fallthrough to try array
            pass

    candidate = find_balanced("[", "]")
    if candidate:
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return None


class AIRater:
    @staticmethod
    def _post_and_get_parsed(prompt: str):
        payload = {"model": MODEL_NAME, "prompt": prompt,"stream":False}
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        except Exception as e:
            return {"error": "request_failed", "detail": str(e)}

        # status check
        if not resp.ok:
            return {
                "error": "bad_status",
                "status_code": resp.status_code,
                "text": resp.text[:2000]
            }

        # try to parse normally if response is JSON
        try:
            # some Ollama endpoints return a JSON object; try to parse it first
            parsed = resp.json()
            # sometimes the model output is in parsed["response"] or parsed.get("outputs")
            # check common keys, fallback to raw text parsing if not found
            if isinstance(parsed, dict):
                if "response" in parsed:
                    return {"ok": True, "content": parsed["response"]}
                if "outputs" in parsed:
                    # outputs may be list of dicts; join strings if present
                    outputs = parsed["outputs"]
                    if isinstance(outputs, list):
                        combined = " ".join(
                            o.get("content", "") if isinstance(o, dict) else str(o)
                            for o in outputs
                        )
                        return {"ok": True, "content": combined}
                # otherwise, return the whole parsed JSON as content
                return {"ok": True, "content": parsed}
            else:
                # parsed is not dict (could be str/list) — return as content
                return {"ok": True, "content": parsed}
        except ValueError:
            # not pure JSON, attempt to extract JSON from text
            raw = resp.text
            extracted = _extract_first_json(raw)
            if extracted is not None:
                return {"ok": True, "content": extracted}
            # last resort: return raw text for debugging
            return {"error": "invalid_json", "text": raw[:4000]}

    @staticmethod
    def rate_user_profile(user_data, repo_stats, language_stats):
        prompt = f"""
You are an AI GitHub profile evaluator. Analyze the following GitHub user and rate them from 1 to 10.

USER DATA:
{json.dumps(user_data, indent=2)}

REPOSITORY STATS:
{json.dumps(repo_stats, indent=2)}

LANGUAGE STATS:
{json.dumps(language_stats, indent=2)}

Provide a JSON response with the following structure only (no extra commentary):

{{
  "rating": <number between 1-10>,
  "developer_level": "<junior/intermediate/senior/pro>",
  "strengths": [ ... ],
  "weaknesses": [ ... ],
  "suggestions": [ ... ]
}}
"""
        result = AIRater._post_and_get_parsed(prompt)
        if result.get("ok"):
            content = result["content"]
            # If content is a string (LLM output), try to extract JSON from it
            if isinstance(content, str):
                parsed = _extract_first_json(content)
                if parsed is not None:
                    return parsed
                # couldn't extract, return the raw string for inspection
                return {"error": "could_not_extract_json", "raw": content}
            else:
                # content already parsed JSON (dict/list)
                return content
        else:
            return result

    @staticmethod
    def rate_repos(repo_list):
        summaries = [repo.summary() for repo in repo_list]

        prompt = f"""
Rate these GitHub repositories individually. Respond with a JSON array where each element has:
- name
- rating (1-10)
- strengths (list)
- weaknesses (list)
- suggestions (list)

REPOS:
{json.dumps(summaries, indent=2)}

IMPORTANT: Respond with valid JSON array only.
"""
        result = AIRater._post_and_get_parsed(prompt)
        if result.get("ok"):
            content = result["content"]
            if isinstance(content, str):
                parsed = _extract_first_json(content)
                if parsed is not None:
                    return parsed
                return {"error": "could_not_extract_json", "raw": content}
            else:
                return content
        else:
            return result

