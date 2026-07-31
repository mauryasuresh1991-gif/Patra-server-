from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI(title="Digital Patra Commercial API", version="1.0")

# CORS इनेबल करना ताकि किसी भी फ्रंटएंड या मोबाइल ऐप से रिक्वेस्ट आ सके
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # कमर्शियल स्तर पर इसे बाद में स्पेसिफिक डोमेन पर सेट किया जा सकता है
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# सुरक्षित तरीके से API Key सेट करना (एनवायरनमेंट वेरिएबल या डायरेक्ट)
API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6L8xnioGmLZ9TUpRHqXcF_HiYZVJSHCXOIRyJBu_fY28w")
genai.configure(api_key=API_KEY)

class LetterRequest(BaseModel):
    prompt: str

@app.post("/generate-letter")
async def generate_letter(req: LetterRequest):
    try:
        # आधुनिक और आधिकारिक Gemini Model का उपयोग (gemini-1.5-flash)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(req.prompt)
        
        if response and response.text:
            return {"status": "success", "result": response.text}
        else:
            raise HTTPException(status_code=500, detail="AI से कोई उत्तर प्राप्त नहीं हुआ।")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "Server is running smoothly!"}
