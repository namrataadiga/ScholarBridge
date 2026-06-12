from google import genai

try:
    # Pass your API key directly into the client initialization
    client = genai.Client(api_key="AQ.Ab8RN6JFbcli5CRqRAA8xkdVllZQAfWI6OIOn7whu-4YMn8WxQ")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Say "Scholar Bridge is ready to launch!"'
    )
    print("✅ SUCCESS!")
    print(f"Gemini Response: {response.text}")
except Exception as e:
    print("❌ ERROR: Could not connect to Gemini API.")
    print(e)