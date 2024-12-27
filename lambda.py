import speech_recognition as sr
import pyttsx3
import wikipedia
import wikipedia.exceptions

# Define the version number
VERSION = "1.0.0, Gaia"

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking: {e}")

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred during listening: {e}")
            return ""


def process_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"There are multiple results for {query}. Please be more specific. Options include: {', '.join(e.options)}")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find any information on that.")
    except Exception as e:
        print(f"Error processing Wikipedia query: {e}")
        speak("An unexpected error occurred while accessing Wikipedia.")


def process_command(command):
    command = command.lower()
    if "hello" in command:
        speak("Hello, how can I assist you today?")
    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        process_wikipedia(query)
    elif "version" in command:
        speak(f"My current version is: {VERSION}") # Added version handling
    elif "exit" in command:
        speak("Goodbye!")
        return False
    else:
        speak("I'm not sure I understand. Can you please repeat?")
    return True

def main():
    while True:
        command = listen()
        if command:
            if not process_command(command):
                break

if __name__ == "__main__":
    main()


