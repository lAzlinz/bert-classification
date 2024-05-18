from typing import List
from transformers import pipeline
import json, random

# functions
def get_answers(label: str) -> List[str]:
    unformatted_answers_list: List[List[str]] =  [chosen['answers'] for chosen in answers if chosen['label'] == label]
    return unformatted_answers_list[0]

def get_answer(question: str) -> str:
    prediction = classifier(question)[0]
    answers_list: List[str] = get_answers(prediction['label'])
    return random.choice(answers_list)

def json_opener(path: str):
    with open(path, encoding='utf-8', mode='r') as file:
        return json.load(file)

# names
name_trained_model: str = 'my_model'
checkpoint: str = '970' # chechpoint-1344 is epoch 14

# paths
path_trained_model: str = f'./models/{name_trained_model}/checkpoint-{checkpoint}' 
path_answers: str = './datasets/answers.json'

# variables
classifier = pipeline("sentiment-analysis", model=path_trained_model)
answers = json_opener(path_answers)

if __name__ == '__main__':
    while True:
        question: str = input(': ')

        if question == 'q':
            break

        answer = get_answer(question)
        print('answer:', answer)
