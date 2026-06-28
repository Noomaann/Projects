from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

print("Loading NLP models... This might take a minute.")

# আগের মডেলগুলো
sentiment_analyzer = pipeline("sentiment-analysis")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# রিপ্লাই তৈরি করার জন্য T5
reply_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
reply_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# নতুন ক্যাটাগরি যোগ করা হয়েছে (feedback)
TICKET_CATEGORIES = ["refund", "complaint", "delivery", "pricing", "technical issue", "feedback", "general inquiry"]

def analyze_ticket(text: str):
    # ১. সেন্টিমেন্ট বের করা
    sentiment_result = sentiment_analyzer(text)[0]
    sentiment = sentiment_result['label'].capitalize() 
    
    # ২. ক্যাটাগরি বের করা
    classification_result = classifier(text, TICKET_CATEGORIES)
    category = classification_result['labels'][0].capitalize() 
    
    # ৩. প্রায়োরিটি স্কোর নির্ধারণ করা
    priority_score = "Medium"
    if sentiment == "Negative" or category.lower() in ["complaint", "technical issue"]:
        priority_score = "High"
    elif category.lower() in ["pricing", "feedback", "general inquiry"]:
        priority_score = "Low"
        
    # ৪. AI Reply Draft তৈরি করা (প্রম্পট আরও স্পেসিফিক করা হয়েছে)
    prompt = f"As a professional customer support agent, write a short, polite, and relevant thank you message to this customer feedback: '{text}'"
    
    # টোকেনাইজ করা (do_sample=False দেওয়া হয়েছে যাতে আবল তাবল না বানায়)
    inputs = reply_tokenizer(prompt, return_tensors="pt")
    outputs = reply_model.generate(**inputs, max_new_tokens=50, do_sample=False)
    
    ai_reply = reply_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
    return {
        "category": category,
        "sentiment": sentiment,
        "priority_score": priority_score,
        "ai_reply_draft": ai_reply
    }