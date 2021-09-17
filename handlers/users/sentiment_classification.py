import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast
from math import ceil

tokenizer = BertTokenizerFast.from_pretrained('blanchefort/rubert-base-cased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('blanchefort/rubert-base-cased-sentiment', return_dict=True)


@torch.no_grad()
def predict(text):
    inputs = tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    # predicted = torch.argmax(predicted, dim=1).numpy()
    return predicted


def normalize_percents(a):
    cumul_sum = 0.0
    cumul_sum_rounded = 0
    prev_baseline = 0
    result = []
    for i in a:
        cumul_sum += i*100
        cumul_sum_rounded = min(100, cumul_sum_rounded + int(round(i*100)))
        result.append(cumul_sum_rounded - prev_baseline)
        prev_baseline = cumul_sum_rounded
    return result


def process_sentiment(text):
    predicted = predict(text).tolist()[0]
    return normalize_percents([predicted[1], predicted[0], predicted[2]])
    # returns [positive, neutral, negative]
