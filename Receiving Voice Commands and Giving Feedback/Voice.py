import speech_recognition as sr
import pyttsx3

# Sesli geri bildirim için motor oluşturma
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dinliyorum...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language="tr-TR")
            print(f"Komut: {command}")
            return command
        except sr.UnknownValueError:
            print("Ne dediğinizi anlayamadım")
            return None
        except sr.RequestError:
            print("İnternet bağlantısı yok")
            return None

# Örnek kullanım
speak("Merhaba, nasıl yardımcı olabilirim?")
command = listen()
if command:
    speak(f"{command} komutunu anladım")
