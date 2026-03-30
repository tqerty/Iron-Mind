import requests
import app.config

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
        memories[login] = memory.copy()

    memories[login].append(
        {
            "role": "user",
            "text": text
        }
    )

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
    memories[login].append(
        {
            'role':'assistant',
            'text': result['alternatives'][0]['message']['text']
        }
    )
    return result['alternatives'][0]['message']['text']
