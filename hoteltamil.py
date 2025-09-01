import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Define scores for Tamil and English keywords
keyword_scores = {
    "puri": 10,
    "pongal": 30,
    "parotta": 20,
    "பூரி": 10,     # Tamil for "puri"
    "பொங்கல்": 30,   # Tamil for "pongal"
    "பரோட்டா": 20    # Tamil for "parotta"
}

# Map number words to integers for both English and Tamil
number_words = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "ஒன்று": 1, "இரண்டு": 2, "மூன்று": 3, "நான்கு": 4, "ஐந்து": 5,
    "ஆறு": 6, "ஏழு": 7, "எட்டு": 8, "ஒன்பது": 9, "பத்து": 10
}

try:
    # Use the microphone as the source
    with sr.Microphone() as source:
        print("Adjusting for background noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("I'm listening. Please speak...")
        # Capture the audio
        audio = recognizer.listen(source)

        print("Processing your speech...")
        # Recognize the speech using Google's API (Tamil + English)
        text = recognizer.recognize_google(audio, language="ta-IN")
        print(f"You said: {text}")

        # Process the recognized text
        words = text.split()  # Split into words
        total_score = 0

        # Iterate through the words to calculate scores
        i = 0
        while i < len(words):
            word = words[i]

            # Check if the current word is a digit or a number word (Tamil/English)
            if word.isdigit() or word in number_words:
                # Convert to a number
                quantity = int(word) if word.isdigit() else number_words[word]
                if i + 1 < len(words) and words[i + 1] in keyword_scores:
                    total_score += quantity * keyword_scores[words[i + 1]]
                    i += 1  # Skip the keyword since it's processed with the quantity
            elif word in keyword_scores:
                total_score += keyword_scores[word]

            i += 1

        print(f"Total Score: {total_score}")

except sr.UnknownValueError:
    print("Sorry, I could not understand what you said.")
except sr.RequestError as e:
    print(f"Request failed: {e}")
