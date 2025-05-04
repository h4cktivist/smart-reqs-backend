import json
from openai import OpenAI
import pandas as pd

from core.config import settings
from .clustering import get_clustering_results


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
    )
    result = completion.choices[0].message.content

    if result == 'False':
        result_json = {"status": False}
    else:
        result_json = json.loads(result)
        result_json['status'] = True
    return result_json


async def get_recommended_techs(project_data: dict) -> dict:
    (
        frameworks_df, libraries_df, databases_df,
        frameworks_encoders, libraries_encoders, databases_encoders,
        frameworks_km, libraries_km, databases_km
    ) = await get_clustering_results()

    license_preference = project_data.get('licensing_type', 'открытая')
    language_filter = project_data.get('languages_preferences', [])

    def predict_cluster(encoders, km_model, features: dict) -> int:
        encoded = {k: encoders[k].transform([v])[0] for k, v in features.items()}
        df = pd.DataFrame([encoded])
        return km_model.predict(df.values)[0]

    def filter_by_language(df, names, preferred_languages):
        if not preferred_languages:
            return names
        return [
            name for name in names
            if df[df['name'] == name]['language'].isin(preferred_languages).any()
        ]

    framework_features = {
        'purpose': project_data['product_type'],
        'scaling_poss': project_data['scaling_needed'],
        'db_integration': project_data['db_needed']
    }
    fw_cluster = predict_cluster(frameworks_encoders, frameworks_km, framework_features)
    fw_names = frameworks_df[frameworks_df['cluster'] == fw_cluster]['name'].tolist()
    recommended_frameworks = filter_by_language(frameworks_df, fw_names, language_filter)

    recommended_dbs = []
    if project_data['db_needed']:
        acid_support = project_data['data_structure'] == 'SQL'
        db_features = {
            'type': project_data['data_structure'],
            'scaling_poss': project_data['scaling_needed'],
            'big_data_poss': project_data['big_data_needed'],
            'acid_support': acid_support
        }
        db_cluster = predict_cluster(databases_encoders, databases_km, db_features)
        recommended_dbs = databases_df[databases_df['cluster'] == db_cluster]['name'].tolist()

    def get_libraries(purpose: str) -> list:
        return libraries_df[
            (libraries_df['purpose'] == purpose) &
            (libraries_df['licence_type'] == license_preference)
        ]['name'].tolist()

    recommended_libraries = []
    if project_data.get('data_analysis_needed'):
        recommended_libraries += get_libraries('обработка данных')
    if project_data.get('ml_needed'):
        recommended_libraries += get_libraries('машинное обучение')
    if project_data.get('autotesting_needed'):
        recommended_libraries += get_libraries('тестирование')

    recommended_libraries = filter_by_language(libraries_df, recommended_libraries, language_filter)

    return {
        'frameworks': recommended_frameworks,
        'libraries': recommended_libraries,
        'databases': recommended_dbs
    }


async def filter_recommended_techs_with_llm(request: dict, recommended_techs: dict) -> dict:
    intro_prompt = f'''
    Есть описание проекта: {request['idea_description']}
    И его функциональные требования: {request['functional_reqs']}
    Также есть стек, содержащий следующие технологии для реализации этого проекта, разделенные по категориям:
    Фреймворки: {recommended_techs['frameworks']}
    Библиотеки: {recommended_techs['libraries']}
    СУБД: {recommended_techs['databases']} Для каждой категории выбери наиболее подходящие и совместимые друг с 
    другом технологии, по 2-3 наименования в каждой категории, при этом не меняй технологии между категориями Также, 
    исходя из описания проекта, определи минмальное и максимальное количество исполнителей проекта'''
    result_format_prompt = '''
    Результат представь в формате JSON, следующего вида:
    {
      "frameworks": String[],
      "libraries": String[],
      "databases": String[],
      "min_devs": int,
      "max_devs": int
    }
    В своем ответе дай только JSON, без указания формата ```json и любых дополнительных символов
    '''

    completion = client.chat.completions.create(
        model=settings.LLM_NAME,
        messages=[{"role": "user", "content": intro_prompt + result_format_prompt}],
    )
    result = completion.choices[0].message.content
    try:
        return json.loads(result)
    except ValueError:
        return recommended_techs
