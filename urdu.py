from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError, WaitTimeoutError
from googletrans import Translator
from gtts import gTTS
from playsound import playsound

# Function to recognize speech with a timeout
def recognize_speech_with_timeout(recognizer, source, timeout=None):
    try:
        print("Recognizing...")
        audio = recognizer.listen(source, timeout=timeout)
        return recognizer.recognize_google(audio)
    except WaitTimeoutError:
        print("Timeout occurred, please try speaking again.")
        return ""
    except UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except RequestError as e:
        print("Error fetching results; {0}".format(e))
        return ""

# Function to translate text
def translate_text(text, dest_language='ur'):
    try:
        translator = Translator()
        translated_text = translator.translate(text, dest=dest_language)
        return translated_text.text
    except Exception as e:
        print("Error translating text:", e)
        return ""

# Function to convert text to speech
def text_to_speech(text, lang='ur'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    playsound("output.mp3")  # Use playsound to play the audio file

# Main function
def main():
    recognizer = Recognizer()
    with Microphone() as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        print("Please speak clearly. Press 'Enter' when you're finished.")
        english_text = ""
        while True:
            partial_text = recognize_speech_with_timeout(recognizer, source, timeout=5)
            if not partial_text:  # If no speech recognized
                break
            print("Partial text:", partial_text)
            english_text += partial_text + " "

    if english_text.strip():
        # Translate to Urdu
        urdu_text = translate_text(english_text)
        print("Translated text:", urdu_text)

        # Convert translated text to speech
        text_to_speech(urdu_text)

if __name__ == "__main__":
    main()
