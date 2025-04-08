from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# FinBERT model yuklanmoqda
model_name = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.eval()

def analyze_with_finbert(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        sentiment = torch.argmax(probs).item()

    label_map = {
        0: "🔴 Negative",
        1: "🟡 Neutral",
        2: "🟢 Positive"
    }
    return label_map[sentiment], probs[0][sentiment].item()
