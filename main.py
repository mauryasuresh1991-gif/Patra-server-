# पायथन बैकएंड (main.py) के अंदर एआई जनरेशन का मजबूत स्ट्रक्चर
@app.post("/generate-letter")
def generate_letter(req: LetterRequest):
    # एक सख्त और पेशेवर सिस्टम प्रॉम्प्ट जो एआई को समझाएगा कि उसे नकल नहीं करनी है
    system_instruction = (
        "You are an expert Government correspondence writer in India. "
        "The user will provide raw notes or instructions. "
        "DO NOT copy the user's instructions into the letter. "
        "Instead, analyze the intent and write a formal, flawless, high-standard official government letter in Hindi. "
        "Include proper formal structure: 'सेवा में,', recipient designation, 'विषय:', 'महोदय,', formal body paragraphs, "
        "and 'भवदीय,' with signature space. Use pure formal bureaucratic Hindi vocabulary."
    )
    
    full_prompt = f"{system_instruction}\n\nUser Request/Notes: {req.prompt}"
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(full_prompt)
    
    return {"result": response.text}
