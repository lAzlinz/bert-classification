from transformers import Trainer
from torch import nn
import torch, json, numpy as np
from my_names import paths
from sklearn.utils.class_weight import compute_class_weight

# calculate the class weights
# get training set
with open(paths['train'], 'r') as f:
    train_set = json.load(f)
    labels = [row['label'] for row in train_set]
class_weights = compute_class_weight('balanced', classes=np.unique(labels), y=labels)

class CustomTrainer(Trainer):
    def compute_loss (self, model, inputs, return_outputs=False):
        labels = inputs.get('labels')
        # forward pass
        outputs = model(**inputs)
        logits = outputs.get('logits')
        # compute custom loss
        loss_fct = nn.CrossEntropyLoss(weight=torch.tensor(class_weights).float())
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss
