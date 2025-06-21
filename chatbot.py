import nltk
from nltk.stem import WordNetLemmatizer
import random
import os
import traceback 

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

FAREWELL_INPUTS = ("bye", "goodbye", "see you", "farewell", "exit", "quit")
FAREWELL_RESPONSES = ["Goodbye!", "See you later!", "Bye! Have a great day!", "It was nice talking to you."]

responses = {
    "name": [
        "I am a simple chatbot created to assist you.",
        "You can call me ChatBot.",
        "I don't have a name yet, but I'm here to help!"
    ],
}

FALLBACK_RESPONSES = [
    "I'm sorry, I don't understand that.",
    "Could you please rephrase that?",
    "I'm still learning. Can you try asking something else?",
    "I'm not sure I can help with that specific query."
]

def download_nltk_data():
    data_packages = ['punkt', 'wordnet', 'averaged_perceptron_tagger']
    for package in data_packages:
        try:
            nltk.data.find(f'tokenizers/{package}' if package == 'punkt' else f'corpora/{package}')
            print(f"NLTK data '{package}' already downloaded.")
        except Exception as e: 
            print(f"Downloading NLTK data: {package}...")
            try:
                nltk.download(package)
                print(f"Successfully downloaded '{package}'.")
            except Exception as e:
                print(f"Error downloading '{package}': {e}")
                print("Please ensure you have an active internet connection or try running 'python -m nltk.downloader all' in your terminal.")

download_nltk_data() 

lemmatizer = WordNetLemmatizer() 

def tokenize_and_lemmatize(sentence):
    """
    Tokenizes a sentence and lemmatizes each word.
    """
    tokens = nltk.word_tokenize(sentence.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized_tokens

def greeting(sentence):
    """
    Checks if the user's input is a greeting.
    """
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
    return None

def farewell(sentence):
    """
    Checks if the user's input is a farewell.
    """
    for word in sentence.split():
        if word.lower() in FAREWELL_INPUTS:
            return random.choice(FAREWELL_RESPONSES)
    return None

def generate_response(user_input):
    """
    Generates a response based on the user's input.
    """
    greet_response = greeting(user_input)
    if greet_response:
        return greet_response

    farewell_response = farewell(user_input)
    if farewell_response:
        return farewell_response

    user_tokens = tokenize_and_lemmatize(user_input)
    user_input_lower = user_input.lower()

    for keyword, possible_responses in responses.items():
        if keyword in user_tokens or keyword in user_input_lower:
            return random.choice(possible_responses)
        if keyword == "name" and ("what is your name" in user_input_lower or "your name" in user_input_lower):
            return random.choice(possible_responses)
        if keyword == "creator" and ("who created you" in user_input_lower or "who made you" in user_input_lower):
            return random.choice(possible_responses)
        if keyword == "how are you" and ("how are you" in user_input_lower):
             return random.choice(possible_responses)
        if keyword == "help" and ("can you help me" in user_input_lower or "i need help" in user_input_lower):
             return random.choice(possible_responses)

    return random.choice(FALLBACK_RESPONSES)

def chatbot_loop():
    print("ChatBot: Hi there! I'm a simple chatbot. You can type 'bye' to exit.")
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            response = generate_response(user_input) 
            print(f"ChatBot: {response}")

            if farewell(user_input):
                break
        except Exception as e:
            print(f"ChatBot: An unexpected error occurred: {e}")
            traceback.print_exc()
            print("ChatBot: I apologize for the inconvenience. Let's try that again.")
            continue

if __name__ == "__main__":
    chatbot_loop()
