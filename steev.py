import speech_recognition as sr
import openai
from gtts import gTTS  # Text-to-speech library
import whisper

# Replace with your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"


def transcribe_audio():
    model = whisper.load_model("base")  # Choose a Whisper model (base, small, medium, or large)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Steev: Hi! Speak Anything:")
        audio = recognizer.listen(source)
    try:
        text = model.transcribe(audio)["text"]  # Transcribe using Whisper
        print("You said:", text)
        return text.lower()  # Convert user input to lowercase for easier comparison
    except Exception as e:
        print("Error:", e)
        return None


def gpt_response(query):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Replace with the specific GPT-3.5 engine you choose
        prompt=query,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


def speak(text):
    # Text-to-speech with gTTS
    tts = gTTS(text=text, lang="en")
    tts.save("output.mp3")
    print("Steev:", text)
    os.system("mpg321 output.mp3")  # Play the audio file (replace with your preferred player)
    os.remove("output.mp3")  # Remove temporary audio file


while True:
    user_query = transcribe_audio()
    if user_query:
        if "what's your name" in user_query or "who are you" in user_query:
            speak("It's nice to meet you! I'm Steev.")
        else:
            chatbot_response = gpt_response(user_query)
            speak(chatbot_response)
