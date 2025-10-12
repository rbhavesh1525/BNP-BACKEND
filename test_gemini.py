import os
import json
import google.generativeai as genai

# Credentials path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Projects\BNP-Hackathon\BNP-Backend\keys\gemini_key.json"

# Optional configure
genai.configure()

prompt = "Extract investment keywords from: 'I want to invest for 5 years safely with medium risk'"

# Use text.create() for your version
response = genai.text.create(
    model="gemini-1.5",
    prompt=prompt,
    temperature=0  # optional, for deterministic output
)

# Output
output_text = response.output_text
print("Gemini Output:", output_text)

# Optional: parse JSON
try:
    keywords = json.loads(output_text)
    print("Parsed Keywords:", keywords)
except:
    print("Response is not valid JSON yet")
