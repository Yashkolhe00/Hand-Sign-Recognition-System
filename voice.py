import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

# List available voices and their details
for i, voice in enumerate(voices):
    print(f"Voice {i}:")
    print(f"ID: {voice.id}")
    print(f"Name: {voice.name}")
    print(f"Language: {voice.languages}")
    print(f"Gender: {voice.gender}")
    print(f"Age: {voice.age}")
    print("-" * 20)

# Example: Set to the second voice in the list
engine.setProperty('voice', voices[1].id)

# You can also adjust the rate and volume if needed
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Test speech
engine.say("Hello, this is a test.")
engine.runAndWait()

# Set to the first voice in the list (usually male or female, depending on the system)
engine.setProperty('voice', voices[0].id)

# Set to a different voice, e.g., voices[1] for a different language or accent
engine.setProperty('voice', voices[1].id)


import pyttsx3

engine = pyttsx3.init()

# Get all available voices
voices = engine.getProperty('voices')

# Set to a voice that supports English or a specific language (adjust 'languages' as needed)
for voice in voices:
    if 'en_US' in voice.languages:  # For English, or change to 'fr_FR', 'de_DE', etc.
        engine.setProperty('voice', voice.id)
        break

# Adjust rate and volume
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Test the voice
engine.say("Hello, how are you?")
engine.runAndWait()



import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

# Print the voices
for voice in voices:
    print(f"ID: {voice.id}, Name: {voice.name}, Language: {voice.languages}")
