import csv, json
from sklearn.model_selection import train_test_split
from typing import Union, List, Dict, Tuple
from itertools import groupby
from my_names import paths
from my_typing import DatasetDict, AnswerDict

def get_dataset() -> List[DatasetDict]:
    """
    keys: text | label
    """
    with open(paths['pattern'], encoding='utf-8', mode='r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)
        dataset = [{'text': row[1], 'label': int(row[2])} for row in csv_reader]
    return dataset

def split_dataset(dataset: List[DatasetDict], test_size: float = 0.2) -> Tuple[List[DatasetDict], List[DatasetDict]]:
    texts: list[str] = [data['text'] for data in dataset]
    labels: list[int] = [data['label'] for data in dataset]

    texts_train, texts_test, labels_train, labels_test = train_test_split(texts, labels, test_size=test_size, random_state=42, stratify=labels)

    train_dataset = [{'text': text, 'label': label} for text, label in zip(texts_train, labels_train)]
    test_dataset = [{'text': text, 'label': label} for text, label in zip(texts_test, labels_test)]

    return (train_dataset, test_dataset)

def get_label2id_and_id2label() -> Dict[Dict[str, int], Dict[int, str]]:
    """
    keys: label2id | id2label | the_label_id | the_label_itself
    """
    labels = {'label2id': {}, 'id2label': {}}
    with open(paths['tags'], encoding='utf-8', mode='r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)

        for row in csv_reader:
            labels['label2id'][row[1]] = int(row[0])
            labels['id2label'][int(row[0])] = row[1]
    
    return labels

def export_data(data, path_file: str = 'Untitled.txt') -> None:
    with open(path_file, encoding='utf-8', mode='w') as file:
        json.dump(data, file, indent=4)

def get_answers(id2label) -> List[AnswerDict]:
    """
    keys: label | answers
    """
    with open(paths['responses'], encoding='utf-8', mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        answers: List[Dict] = sorted([{'label': int(row[2]), 'answers': row[1]} for row in csv_reader], key=lambda x: x['label'])
        labelled_answers = [{'label': id2label[label_id], 'answers': [resp['answers'] for resp in resps]} for label_id, resps in groupby(answers, key=lambda x: x['label'])]
        return labelled_answers

def dataset_split_to_train_eval_test(dataset: List[DatasetDict], train_size: float = 1.0, eval_size: float = 0, test_size: float = 0) -> Tuple[List[DatasetDict], List[DatasetDict], List[DatasetDict]]:
    train_eval_dataset, test_dataset = split_dataset(dataset, test_size=test_size)
    train_dataset, eval_dataset = split_dataset(train_eval_dataset, test_size=eval_size/(1-test_size))
    return (train_dataset, eval_dataset, test_dataset)

def json_opener(path: str):
    with open(path, encoding='utf-8', mode='r') as file:
        return json.load(file)

def id2label_opener():
    with open(paths['id2label'], encoding='utf-8', mode='r') as file:
        return {int(key): label for key, label in json.load(file).items()}

if __name__ == '__main__':
    labels = get_label2id_and_id2label()
    dataset = get_dataset() # 100%
    train, eval, test = dataset_split_to_train_eval_test(dataset, 0.64, 0.16, 0.2)
    answers = get_answers(labels['id2label'])

    export_data(labels['label2id'], paths['label2id'])
    export_data(labels['id2label'], paths['id2label'])
    export_data(train, paths['train'])
    export_data(test, paths['test'])
    export_data(eval, paths['eval'])
    export_data(answers, paths['answers'])