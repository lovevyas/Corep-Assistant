import warnings

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    module="google.generativeai"
)

import google.generativeai as genai
import json
import os


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def safe_json_parse(text):
    text = text.strip()

    # Case 1: empty response
    if not text:
        raise ValueError("LLM returned empty response")

    # Case 2: find first JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in LLM response")

    json_str = text[start:end+1]
    return json.loads(json_str)



def generate_structured_output(question, scenario, rules, schema):
    prompt = f"""
You are a regulatory reporting assistant.

USER QUESTION:
{question}

SCENARIO:
{scenario}

REGULATORY TEXT:
{chr(10).join(rules)}

COREP TEMPLATE:
{schema}

INSTRUCTIONS:
- Populate only relevant fields.
- Use only field_id values present in the COREP TEMPLATE.
- Output JSON only.
- Include justification for each field.
- If information is missing, say "MISSING".
Must Follow:
- You MUST return valid JSON.
- Do NOT include explanations, markdown, or text.
- Do NOT wrap output in ``` blocks.
- The response must start with '{' and end with '}'.
- If unsure, still return JSON with value "MISSING".

Return JSON only in this format:
{{
  "template": "COREP C 01.00",
  "fields": [
    {{
      "field_id": "010",
      "value": "number",
      "justification": "Rule reference "
    }}
  ]
}}
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    # raw = response.text.strip()
    # if raw.startswith("```"):
    #     raw = raw.split("```")[1]

    return safe_json_parse(response.text)


def safe_json_parse(text):
    text = text.strip()

    # Case 1: empty response
    if not text:
        raise ValueError("LLM returned empty response")

    # Case 2: find first JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in LLM response")

    json_str = text[start:end+1]
    return json.loads(json_str)
