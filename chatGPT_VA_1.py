import speech_recognition as sr
import os
from gtts import gTTS
import pyttsx3
from pydub import AudioSegment
import pyautogui
import webbrowser

# Function to listen for voice commands
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

# Function to respond with speech
def respond(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang="en")
    tts.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    os.system("afplay response.wav")

tasks = []
listeningToTask = False

def main():
    global tasks
    global listeningToTask
    #respond("Hello, Jake. I hope you're having a nice day today.")
    while True:
        command = listen_for_command()
        if command:
          if listeningToTask:
            tasks.append(command)
            listeningToTask
            respond(f"Adding {command} to your tasks list. {str(len(tasks)) } currently in your list.")
          elif "add a task" in command:
            listeningToTask = True
            respond("Sure, what is the task?")
          elif "list tasks" in command:
            respond("Sure. Your tasks are:")
            for task in tasks:
              respond(task)
          elif "take a screenshot" in command:
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save('screenshot.png')
            respond("Done. I've saved the screenshot to your desktop.")
          elif "open chrome" in command:
            respond("Opening Chrome.")
            webbrowser.open('http://google.com')
            # os.system("open -a 'Google Chrome'")
          elif "exit" in command:
            respond("Goodbye.")
            break
          else:
            respond("Sorry, I don't understand that command.")


if __name__ == '__main__':
    main()

