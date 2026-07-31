from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# 1. FastAPI ऐप का इंस्टेंस
app = FastAPI()

# 2. CORS इनेबल करें ताकि फ्रंटएंड से रिक्वेस्ट आसानी से आ सके
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. जेमिनी API की को सीधे यहाँ सेट कर दिया गया है
API_KEY = "AQ.Ab8RN6INB6Fc7lArhiSAMSRK3aNPml1gkPaBz_SecwPO_3paxQ"
genai.configure(api_key=API_KEY)

class LetterRequest(BaseModel):
    prompt: str

@app.post("/generate-letter")
def generate_letter(req: LetterRequest):
    try:
        # सख्त और पेशेवर सिस्टम निर्देश ताकि एआई केवल एक उच्च-स्तरीय शासकीय पत्र ही लिखे
        system_instruction = (
            "You are an expert Government correspondence writer in India. "
            "The user will provide raw notes or instructions. "
            "DO NOT copy the user's instructions into the letter. "
            "Instead, analyze the intent and write a formal, flawless, high-standard official government letter in Hindi. "
            "Include proper formal structure: 'सेवा में,', recipient designation, 'विषय:', 'महोदय,', formal body paragraphs, "
            "and 'भवदीय,' with signature space. Use pure formal bureaucratic Hindi vocabulary."
        )
        
        full_prompt = f"{system_instruction}\n\nUser Request/Notes: {req.prompt}"
        
        # सबसे स्थिर और मानक जेमिनी मॉडल
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(full_prompt)
        
        return {"result": response.text}
    except Exception as e:
        return {"result": f"एरर: {str(e)}"}

@app.get("/")
def home():
    return {"status": "Patra Manager Server is Running perfectly!"}
