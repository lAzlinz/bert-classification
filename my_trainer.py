from transformers import Trainer
from torch import nn
import torch, json

with open('./datasets/class_weights.json', 'r') as file:
    class_weights: list[float] = json.load(file)

class CustomTrainer(Trainer):
    def compute_loss (self, model, inputs, return_outputs=False):
        labels = inputs.get('labels')
        # forward pass
        outputs = model(**inputs)
        logits = outputs.get('logits')
        # compute custom loss
        loss_fct = nn.CrossEntropyLoss(weight=torch.tensor(class_weights))
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss