from transformers import BertConfig, BertForSequenceClassification
import torch.nn as nn
from torch.nn import CrossEntropyLoss, MSELoss

class BertForSequenceClassificationReviewsSentiments(BertForSequenceClassification):

    def __init__(self, config):
        super(BertForSequenceClassificationReviewsSentiments, self).__init__(config)
        # self.num_labels = config.num_labels
        # self.bert = BertModel(config)
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(config.hidden_size, 128)
        self.classifier_2 = nn.Linear(128, self.config.num_labels)

    def forward(
        self, 
        input_ids=None, 
        attention_mask=None, 
        token_type_ids=None,
        position_ids=None, 
        head_mask=None, 
        inputs_embeds=None, 
        labels=None
    ):    
        
        outputs = self.bert(
            input_ids = input_ids,
            attention_mask = attention_mask,
            token_type_ids = token_type_ids,
            position_ids = position_ids,
            head_mask = head_mask,
            inputs_embeds = inputs_embeds,
        )
        
        pooled_output = outputs[1]

        pooled_output = self.dropout(pooled_output)
        pooled_output = self.classifier(pooled_output)
        logits = self.classifier_2(pooled_output)

        outputs = (logits,) + outputs[2:]  # add hidden states and attention if they are here

        if labels is not None:
            if self.num_labels == 1:
                #  We are doing regression
                loss_fct = MSELoss()
                loss = loss_fct(logits.view(-1), labels.view(-1))
            else:
                loss_fct = CrossEntropyLoss()
                loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
            outputs = (loss,) + outputs

        return outputs  # (loss), logits, (hidden_states), (attentions)