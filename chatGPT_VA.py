import speech_recognition as sr
import pyttsx3
import openai
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY

engine = pyttsx3.init
recognizer = sr.Recognizer()

def transcribe_audio_to_text(filename):
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        print(f'Skipping, error occurred: {e}')

# get response From GPT-3
def generate_response(prompt):
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

messages = []
# speak text out loud
def speak_text(command):
    engine.say(command)
    engine.runAndWait()


def main():
    while True:
        print('Say "Genius" to start recording')
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == 'genius':
                    print('Recording... say your question now.')
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                        with open('input.wav', 'wb') as f:
                            f.write(audio.get_wav_data())

                        # transcribe audio to text
                        text = transcribe_audio_to_text('input.wav')
                        if text:
                            print(f"You said: {text}")

                            # generate response using GPT-3
                            response = generate_response(text)
                            print(f"GPT-3 says: {response.strip()}")

                            # read response using text-to-speech
                            speak_text(response)

            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    # main()
    #transcribe_audio_to_text('response.mp3')
    generate_response("Give me a list of the top 2 most popular songs in the US right now.")
