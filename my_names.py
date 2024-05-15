directories = {
    'datasets': './datasets/',
    'models': './models/',
    'reports': './reports/'
}

names_files = {
    'pattern': 'patterns.csv',
    'tags': 'tags.csv',
    'responses': 'responses.csv',
    'answers': 'answers.json',
    'test': 'test.json',
    'train': 'train.json',
    'eval': 'eval.json',
    'id2label': 'id2label.json',
    'label2id': 'label2id.json'
}
name_trained_model = 'my_model'


paths = dict()
for key, name in names_files.items():
    paths[key] = directories['datasets'] + name
paths['trained_model'] = directories['models'] + name_trained_model
paths['pretrained_model'] = 'distilbert/distilbert-base-uncased'
paths['model_reports'] = directories['reports'] + name_trained_model

if __name__ == '__main__':
    for _, path in paths.items():
        print(path)
