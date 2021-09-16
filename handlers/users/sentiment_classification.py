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


def process_sentiment(text):
    result = predict(text).tolist()[0]
    result = [ceil(num * 100) / 100.0 for num in result]
    return result[1], result[0], result[2]  # positive - neutral - negative
    # return f"{result[1]} Positive" \
    #       f"\n{result[0]} Neutral" \
    #       f"\n{result[2]} Negative"
