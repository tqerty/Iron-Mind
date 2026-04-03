import requests
import app.config
import asyncio
from database.logic_db import insert_data, get_data

memories = {

}

memory = [
    {
        'role':'system',
        'text': '''
Ты психолог - спортсмен со стажем более 15 лет, был 
прекрасным тренером в боевых единоборствах, имеешь огромный опыт в психологии, 
и помогаешь спортсменам справляться с психологическими и моральными трудностями таких как 
мандраж перед соревнованиями и перед каждым боем'''
    }
]

def gpt(text, login):
    if login not in memories:
        memories[login] = load_history(login)

    memories[login].append(
        {
            "role": "user",
            "text": text
        }
    )

    insert_data(login, 'user', text)

    prompt = {
        "modelUri": f"gpt://{app.config.id_ya}/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": memories[login]
    }
    
    
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {app.config.key_ya}"
    }
    
    response = requests.post(url, headers=headers, json=prompt)
    result = response.json().get('result')
    ai_answer = result['alternatives'][0]['message']['text']
    memories[login].append(
        {
            'role':'assistant',
            'text': ai_answer
        }
    )
    insert_data(login, 'assistant', ai_answer)



    return ai_answer

async def gpt_io(text, login):
    return await asyncio.to_thread(gpt, text, login)

def load_history(login):
    history = memory.copy()
    history.extend(get_data(login))
    return history