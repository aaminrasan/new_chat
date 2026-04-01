#!/usr/bin/env python3
"""Simple test script for the chatbot API."""

import requests

# Dictionary of thread_id -> list of questions
test_data = {
    "thread_1": [
        "Hello, how are you?",
        "What is your name?",
        "Tell me a joke."
    ],
    "thread_2": [
        "Hi there!",
        "What's the weather like today?",
        "Do you like programming?"
    ],
    "thread_3": [
        "Good morning!",
        "What can you help me with?"
    ]
}

API_URL = "http://localhost:8000/chat"

def main():
    print("=" * 60)
    print("Chatbot API Test")
    print("=" * 60)
    
    for thread_id, questions in test_data.items():
        print(f"\n{'=' * 60}")
        print(f"Thread: {thread_id}")
        print("=" * 60)
        
        for question in questions:
            print(f"\n[User]: {question}")
            
            try:
                response = requests.post(
                    API_URL,
                    json={"message": question, "thread_id": thread_id},
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"[Bot]: {data.get('response', 'No response')}")
                else:
                    print(f"[Error]: Status {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                print("[Error]: Could not connect to API. Is the server running?")
                print("Run: cd chatbot && python -m src.main")
                return
            except requests.exceptions.Timeout:
                print("[Error]: Request timed out")
            except Exception as e:
                print(f"[Error]: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
