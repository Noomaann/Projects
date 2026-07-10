from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

print("Loading NLP models... This might take a minute.")


sentiment_analyzer = pipeline("sentiment-analysis")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


reply_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
reply_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")


TICKET_CATEGORIES = ["refund", "complaint", "delivery", "pricing", "technical issue", "feedback", "general inquiry"]

def analyze_ticket(text: str):

    sentiment_result = sentiment_analyzer(text)[0]
    sentiment = sentiment_result['label'].capitalize() 
    

    classification_result = classifier(text, TICKET_CATEGORIES)
    category = classification_result['labels'][0].capitalize() 
    

    priority_score = "Medium"
    if sentiment == "Negative" or category.lower() in ["complaint", "technical issue"]:
        priority_score = "High"
    elif category.lower() in ["pricing", "feedback", "general inquiry"]:
        priority_score = "Low"
        

    prompt = f"As a professional customer support agent, write a short, polite, and relevant thank you message to this customer feedback: '{text}'"
 
    inputs = reply_tokenizer(prompt, return_tensors="pt")
    outputs = reply_model.generate(**inputs, max_new_tokens=50, do_sample=False)
    
    ai_reply = reply_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
    return {
        "category": category,
        "sentiment": sentiment,
        "priority_score": priority_score,
        "ai_reply_draft": ai_reply
    }
