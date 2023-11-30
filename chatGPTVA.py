import speech_recognition as sr
import pyttsx3
import pyautogui
import webbrowser
import openai
import os

from gtts import gTTS
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY

# Listen For Voice Commands
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening for commands...')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said: ", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Translates Text To Audible Speech
def text_to_speech(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang="en")
    tts.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    os.system("afplay response.wav")

# Get Response From GPT-3
def chatGPT_response(prompt):
    response = openai.chat.completions.create(
         messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content

# Main Function
def main():
    text_to_speech("Hello What Can I Do For You Today?")
    while True:
        # Start Program By Giving A Command
        command = listen_for_command()
        if command:
          # Ask chatGPT A Question
          if any(word in command for word in ["who", "what", "when", "where", "how", "should", "why", "will", "would", "can", "could", "do", "does", "is", "are", "am", "was", "were", "have", "has", "had", "which",]):
            response = chatGPT_response(command)
            text_to_speech(response)
          if "open chrome" in command:
            text_to_speech("Opening Chrome.")
            webbrowser.open('http://google.com')
          if "exit" in command:
            text_to_speech("Goodbye.")
            break
          else:
            text_to_speech("Sorry, I don't understand that command.")


if __name__ == '__main__':
    main()



