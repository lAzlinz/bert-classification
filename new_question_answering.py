from typing import List, Tuple, Union
from transformers import pipeline
import json, random

# functions
def get_answers_questions(label: str) -> Tuple[List[str], List[str]]:
    answers_list: List[str]=  [chosen['answers'] for chosen in answers if chosen['label'] == label][0]
    questions_list: List[str] = [chosen['questions'] for chosen in questions if chosen['label'] == label][0]
    return (answers_list, questions_list)

def get_result(question: str) -> dict[str, Union[float, str]]:
    prediction = classifier(question)[0]
    answers_list, question_list = get_answers_questions(prediction['label'])

    return_value = {
        'score': prediction['score'],
        'answer': random.choice(answers_list),
        'question': random.choice(question_list)
    }
    return return_value

def json_opener(path: str):
    with open(path, encoding='utf-8', mode='r') as file:
        return json.load(file)

# names
name_trained_model: str = 'my_model'
checkpoint: str = '970' # chechpoint-1344 is epoch 14

# paths
path_trained_model: str = f'./models/{name_trained_model}/checkpoint-{checkpoint}'
path_answers: str = './datasets/answers.json'
path_questions: str = './datasets/questions.json'
# variables
classifier = pipeline("sentiment-analysis", model=path_trained_model)
answers = json_opener(path_answers)
questions = json_opener(path_questions)

if __name__ == '__main__':
    while True:
        question: str = input(': ')

        if question == 'q':
            break

        result = get_result(question)
        
        if result['score'] >= 0.2:
            print('answer:', result['answer'])
        else:
            while True:
                print('answer:', result['question'])
                confirmation: str = input(': ')

                if confirmation.lower() in ['yes', 'y', 'yeah', 'yup']:
                    print('answer:', result['answer'])
                    break
                elif confirmation.lower() in ['no', 'n']:
                    print('answer:', 'please modify your question then ask again.')
                    break
                else:
                    print('Invalid confirmation.')
