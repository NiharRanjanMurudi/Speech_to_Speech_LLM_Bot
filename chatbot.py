import torch
import speech_recognition as sr
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import cv2
from PIL import Image, ImageTk

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speaking rate
engine.setProperty('volume', 1.0)  # Set volume

# Load Pre-Trained Model Locally
print("Loading Pre-Trained Model...")
model_name = "microsoft/DialoGPT-medium"

# Check device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)  # Move model to device

# Function: Recognize Speech (Speech-to-Text)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio).lower()

            # Trigger predefined speech when specific input is detected
            if "what is ai" in text:
                predefined_speech("ai")
                return
            elif "what is space" in text:
                predefined_speech("space")
                return

            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError as e:
            return f"Error with speech recognition: {e}"
        except sr.WaitTimeoutError:
            return "No input detected. Please try again."

# Function: Predefined Speech
def predefined_speech(topic):
    if topic == "ai":
        predefined_text = (
            "Artificial Intelligence (AI) is a branch of computer science focused on creating systems capable of performing tasks that typically require human intelligence. "
            "These tasks include learning from data, reasoning to solve problems, and making decisions. AI also enables machines to interpret and respond to sensory inputs like images, speech, and text. "
            "It powers technologies like chatbots, autonomous vehicles, and recommendation systems. By mimicking human cognitive abilities, AI is transforming industries such as healthcare, finance, and education. "
            "Its goal is to build intelligent systems that can work efficiently and adapt to new situations."
        )
    elif topic == "space":
        predefined_text = (
            "Space is the vast, seemingly infinite expanse that exists beyond Earth's atmosphere. "
            "It is where planets, stars, galaxies, and other celestial bodies exist. Space is characterized by a near vacuum, with no air or life as we know it. "
            "It holds mysteries about the origins of the universe, black holes, and the potential for life on other planets. "
            "Exploration of space has led to groundbreaking discoveries and advancements in science and technology, inspiring humanity to understand the cosmos and our place within it."
        )
    else:
        predefined_text = "Sorry, I do not have information on that topic."

    update_conversation(f"Bot: {predefined_text}")
    speak_text(predefined_text)

# Function: Get Response from Pre-Trained LLM
def get_llm_response(user_input):
    try:
        input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt").to(device)
        output = model.generate(input_ids, max_length=100, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response
    except Exception as e:
        return "Sorry, I am unable to process your request right now."

# Function: Convert Text to Speech
def speak_text(response_text):
    engine.say(response_text)
    engine.runAndWait()

# Function: Speech-to-Speech Interaction
def start_bot():
    while running:
        user_input = recognize_speech()
        if user_input:
            if user_input == "exit":
                update_conversation("You: exit")
                update_conversation("Bot: Goodbye! Have a great day!")
                speak_text("Goodbye! Have a great day!")
                stop_bot()
                break

            update_conversation(f"You: {user_input}")
            if "Triggered predefined" not in user_input:
                bot_response = get_llm_response(user_input)
                update_conversation(f"Bot: {bot_response}")
                speak_text(bot_response)

# Function: Update Conversation in UI
def update_conversation(message):
    conversation_area.config(state=tk.NORMAL)
    conversation_area.insert(tk.END, message + "\n")
    conversation_area.config(state=tk.DISABLED)
    conversation_area.see(tk.END)

# Function: Start Bot in a Thread
def start_bot_thread():
    global running
    running = True
    bot_thread = Thread(target=start_bot)
    bot_thread.start()

# Function: Stop Bot
def stop_bot():
    global running
    running = False

# Function: Open Webcam in Popup
def open_webcam():
    def update_frame():
        _, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        webcam_label.imgtk = imgtk
        webcam_label.configure(image=imgtk)
        webcam_label.after(10, update_frame)

    cap = cv2.VideoCapture(0)

    webcam_window = tk.Toplevel()
    webcam_window.title("Webcam")
    webcam_label = tk.Label(webcam_window)
    webcam_label.pack()

    update_frame()

    webcam_window.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), webcam_window.destroy()))

# Create UI
def create_ui():
    global conversation_area

    root = tk.Tk()
    root.title("Speech-to-Speech Bot")

    # Conversation Area
    conversation_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20, font=("Arial", 12))
    conversation_area.pack(pady=10)

    # Buttons
    start_button = tk.Button(root, text="Start Bot", command=start_bot_thread, font=("Arial", 12))
    start_button.pack(pady=5)

    stop_button = tk.Button(root, text="Stop Bot", command=stop_bot, font=("Arial", 12))
    stop_button.pack(pady=5)

    webcam_button = tk.Button(root, text="Open Webcam", command=open_webcam, font=("Arial", 12))
    webcam_button.pack(pady=5)

    root.mainloop()

# Main Execution
if __name__ == "__main__":
    running = False
    create_ui()