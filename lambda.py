import pyttsx3
import wikipedia
import requests
import subprocess
import sys

# --- CONFIGURATION ---
CURRENT_VERSION = "1.1"
VERSION_CODENAME = "Helios"
VERSION_CHECK_URL = "https://github.com/ASGH027/Lambda/blob/main/version.txt"

engine = pyttsx3.init()

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def check_for_updates():
    """Checks if the current version matches the remote version."""
    try:
        response = requests.get(VERSION_CHECK_URL, timeout=2)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version != CURRENT_VERSION:
                return True, latest_version
    except:
        pass 
    return False, CURRENT_VERSION

def get_voice_input():
    """Attempts to use the microphone. Falls back to text if PyAudio/SpeechRecognition fails."""
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("\n[Listening...]")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio)
    except (ImportError, Exception):
        # This triggers if PyAudio is missing OR if there is a hardware error
        return "fallback_to_text"

def process_command(command):
    command = command.lower().strip()
    if not command: return True

    # --- WIKIPEDIA COMMAND ---
    if "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        speak(f"Searching Wikipedia for {query}...")
        try:
            summary = wikipedia.summary(query, sentences=2)
            speak(summary)
        except Exception:
            speak("I couldn't find a clear result for that.")

    # --- UPGRADE COMMAND ---
    elif "upgrade" in command:
        speak("Checking for system updates...")
        try:
            # Runs 'git pull' to download new code from your repository
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            if "Already up to date" in result.stdout:
                speak("Everything is already up to date.")
            else:
                speak("Files updated successfully. Please restart Helios.")
                sys.exit()
        except Exception:
            speak("Automatic upgrade failed. Please ensure Git is installed.")

    # --- VERSION COMMAND ---
    elif "version" in command:
        speak(f"I am running version {CURRENT_VERSION}, codename {VERSION_CODENAME}.")

    elif "exit" in command or "quit" in command:
        speak("Shutting down Helios. Goodbye!")
        return False
    
    else:
        speak(f"I heard: {command}. I don't know how to do that yet.")
    
    return True

def main():
    # Update Check
    is_outdated, latest = check_for_updates()
    
    print(f"--- Assistant v{CURRENT_VERSION} ({VERSION_CODENAME}) ---")
    if is_outdated:
        print(f"!!! UPDATE AVAILABLE: Version {latest} is out. Type 'upgrade' to fetch it. !!!\n")
    
    # Mode Selection
    mode = input("Choose mode - [V]oice or [T]ext: ").lower()

    running = True
    while running:
        if mode == 'v':
            user_input = get_voice_input()
            if user_input == "fallback_to_text":
                print("\n[!] Microphone or PyAudio not detected. Switching to Text Mode.")
                mode = 't'
                continue
            print(f"You (Voice): {user_input}")
        else:
            user_input = input("\nYou (Text): ")

        running = process_command(user_input)

if __name__ == "__main__":
    main()
