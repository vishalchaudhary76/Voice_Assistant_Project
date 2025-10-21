import speech_recognition as sr
import webbrowser
import requests
import os
from openai import OpenAI
import musicLibrary  # Make sure this file exists with a dictionary `musicLibrary.music`

# Your API keys
newsapi = "<Your NewsAPI Key>"
openai_key = "<Your OpenAI Key>"

# Initialize recognizer
recognizer = sr.Recognizer()

# Speak function using native Mac 'say'
def speak(text):
    os.system(f'say "{text}"')

# Function to call OpenAI
def aiProcess(command):
    client = OpenAI(api_key=openai_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Assistant skilled in general tasks. Give short responses."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

# Command processor
def processCommand(c):
    c = c.lower()
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play "):
        song = c.replace("play ", "").strip()
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I don't have {song} in my library")
    elif "news" in c:
        speak("Here are the top headlines")
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # limit to top 5 headlines
                speak(article['title'])
    else:
        output = aiProcess(c)
        speak(output)

# Main program
if __name__ == "__main__":
    speak("Initializing Assistant")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)
                
                if word.lower() == "assistant":
                    speak("Yes?")
                    print("Assistant Active...")
                    
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = recognizer.listen(source, timeout=5)
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")
                        processCommand(command)

        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            print(f"Error: {e}")
