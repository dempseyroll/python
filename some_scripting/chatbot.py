# Simple chatbot
import random

def chatbot():
    responses = ['Hello!', 'How can I help you?', 'Goodbye!']
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'bye':
            print("Chatbot: Goodbye!")
            break
        print(f"Chatbot: {random.choice(responses)}")

chatbot()