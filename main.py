from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import urllib.request
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "AQ.Ab8RN6INB6Fc7lArhiSAMSRK3aNPml1gkPaBz_SecwPO_3paxQ"

class LetterRequest(BaseModel):
    prompt: str

@app.post("/generate-letter")
def generate_letter(req: LetterRequest):
    try:
        system_instruction = (
            "You are an expert Government correspondence writer in India. "
            "The user will provide raw notes or instructions. "
            "DO NOT copy the user's instructions into the letter. "
            "Instead, analyze the intent and write a formal, flawless, high-standard official government letter in Hindi. "
            "Include proper formal structure: 'सेवा में,', recipient designation, 'विषय:', 'महोदय,', formal body paragraphs, "
            "and 'भवदीय,' with signature space. Use pure formal bureaucratic Hindi vocabulary."
        )
        
        full_text = f"{system_instruction}\n\nUser Request/Notes: {req.prompt}"
        
        # डायरेक्ट गूगल जेमिनी रेस्ट एपीआई का उपयोग (बिना किसी लाइब्रेरी एरर के)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": full_text}]
            }]
        }
        
        data = json.dumps(payload).encode('utf-8')
        request = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(request) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            output_text = res_data['candidates'][0]['content']['parts'][0]['text']
            return {"result": output_text}
            
    except Exception as e:
        return {"result": f"एरर: {str(e)}"}

@app.get("/")
def home():
    return {"status": "Patra Manager Server is Running!"}
