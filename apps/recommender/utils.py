import json
from openai import OpenAI
from core.config import settings


PROMPT_PATH: str = "apps/recommender/llm_prompt.txt"

client: OpenAI = OpenAI(
    base_url=settings.LLM_PROVIDER_URL,
    api_key=settings.LLM_API_KEY
)


def load_prompt_from_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        prompt = f.read()
    return prompt


async def get_project_info_from_llm(idea_description: str, functional_reqs: str) -> dict:
    project_info = f"""Есть следующая информация об IT-проекте, полученная от пользователя:
        {idea_description}
        И следующие функциональные требования:
        {functional_reqs}
    """

    prompt = load_prompt_from_file(PROMPT_PATH)
    completion = client.chat.completions.create(
        model=settings.LLM_NAME,
        messages=[{"role": "user", "content": project_info + prompt}],
        stream=True
    )
    result = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            result += chunk.choices[0].delta.content

    if result == 'False':
        result_json = {"status": False}
    else:
        result_json = json.loads(result)
        result_json['status'] = True
    return result_json
