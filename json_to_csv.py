import json, csv

with open('./datasets/training_set.json', encoding='utf-8') as f:
    training_data = json.load(f)

with open('./datasets/validation_set.json', encoding='utf-8') as f:
    validation_data = json.load(f)

tags = []
for intent in training_data['intents']:
    tags.append(intent['tag'])

def convert_pattern_to_csv() -> None:
    X_pattern = []
    y_pattern = []
    data_pattern = [['index','pattern','tag']]
    for intent in training_data['intents']:
            for pattern in intent['patterns']:
                X_pattern.append(pattern)
                y_pattern.append(tags.index(intent['tag']))
    
    for intent in validation_data['intents']:
        for pattern in intent['patterns']:
            if intent['tag'] in tags:
                X_pattern.append(pattern)
                y_pattern.append(tags.index(intent['tag']))

    for index, pattern in enumerate(X_pattern):
        row = [index, pattern, y_pattern[index]]
        data_pattern.append(row)
    export_data_as_csv('patterns', data_pattern)

def convert_response_to_csv() -> None:
    X_response = []
    y_response = []
    data_response = [['index','response','tag']]
    for intent in training_data['intents']:
        for response in intent['responses']:
            X_response.append(response)
            y_response.append(tags.index(intent['tag']))
        
    for intent in validation_data['intents']:
        for response in intent['responses']:
            X_response.append(response)
            y_response.append(tags.index(intent['tag']))

    for index, x in enumerate(X_response):
        row = [index, x, y_response[index]]
        data_response.append(row)
    export_data_as_csv('responses', data_response)

def convert_tag_to_csv() -> None:
    data_tag = [['tag_id','tag']]
    for index, tag in enumerate(tags):
        data_tag.append([index,tag])
    export_data_as_csv('tags', data_tag)

def export_data_as_csv(file_name:str, data:list[list]) -> None:
    file_path = './datasets/' + file_name + '.csv'
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)

if __name__ == '__main__':
    convert_pattern_to_csv()
    convert_response_to_csv()
    convert_tag_to_csv()