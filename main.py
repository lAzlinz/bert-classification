from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding
from transformers import AutoModelForSequenceClassification, TrainingArguments
import evaluate, numpy as np, json
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report, confusion_matrix

from my_convert import json_opener, id2label_opener
from my_names import paths
from my_trainer import CustomTrainer

MAX_LENGTH: int = 512
num_train_epochs: int = 15
batch_size: int = 16

dataset = load_dataset("json", data_files={'train': paths['train'], 'eval': paths['eval']})
tokenizer = AutoTokenizer.from_pretrained(paths['pretrained_model'])

def preprocess(examples: dict):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=MAX_LENGTH) # padding=True, truncation=True, return_tensors="pt"

tokenized_dataset = dataset.map(preprocess, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# evaluation
accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    # for binary
    # # return accuracy.compute(predictions=predictions, references=labels)
    # for multi-class
    accuracy = np.mean(predictions==labels)
    precision = precision_score(labels, predictions, average=None)
    recall = recall_score(labels, predictions, average=None)
    f1 = f1_score(labels, predictions, average=None)
    macro_f1 = f1_score(labels, predictions, average='macro')
    weighted_f1 = f1_score(labels, predictions, average='weighted')
    report = classification_report(labels, predictions)
    conf_mat = confusion_matrix(labels, predictions)

    # Print the metrics
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)
    print("Macro F1-score:", macro_f1)
    print("Weighted F1-score:", weighted_f1)
    print("Classification Report:\n", report)
    print("Confusion Matrix:\n", conf_mat)

    data: dict = {
        'epoch': 0,
        'accuracy': accuracy,
        'precision': precision.tolist(),
        'recall': recall.tolist(),
        'f1-score': f1.tolist(),
        'f1-score-macro': macro_f1,
        'f1-score-weighted': weighted_f1,
        'classification report': report,
        'confusion matrix': conf_mat.tolist()
    }

    # -- record report ---------------------------------
    path_file: str = './record/my_model'
    try:
        with open(path_file, 'r') as file:
            old_data: list[dir] = json.load(file)
            data['epoch'] = 1 + len(old_data)
            old_data.append(data)
    except FileNotFoundError:
        data['epoch'] = 1
        old_data = [data]
    
    with open(path_file, 'w') as file:
        json.dump(old_data, file, indent=4)
    # ---------------------------------------------------

    return {"accuracy": accuracy, "macro_f1": macro_f1, "weighted_f1": weighted_f1}


# train
label2id = json_opener(paths['label2id'])
id2label = id2label_opener()
num_labels = len(label2id)
# id2label = {0: "NEGATIVE", 1: "POSITIVE"}
# label2id = {"NEGATIVE": 0, "POSITIVE": 1}

model = AutoModelForSequenceClassification.from_pretrained(
    paths['pretrained_model'],
    num_labels=num_labels,
    id2label=id2label,
    label2id=label2id
)

training_args = TrainingArguments(
    output_dir=paths['trained_model'],
    learning_rate=2e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=num_train_epochs,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    push_to_hub=False, 
)

trainer = CustomTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["eval"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

if __name__ == '__main__':
    trainer.train()