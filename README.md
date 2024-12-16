# Speech-to-Speech AI Chatbot with DialoGPT and Tkinter

This project is a speech-to-speech AI chatbot that leverages DialoGPT, speech recognition, text-to-speech conversion, and a graphical user interface built with Tkinter. It also includes webcam integration for added interactivity.

## Features

- **Speech-to-Text**: Converts user speech to text using the `speech_recognition` library.
- **AI Responses**: Generates conversational responses using a pre-trained DialoGPT model.
- **Text-to-Speech**: Converts AI responses back into speech using `pyttsx3`.
- **Predefined Topics**: Provides detailed explanations for specific topics like AI and Space.
- **Graphical UI**: User-friendly interface for interaction, built with Tkinter.
- **Webcam Integration**: Allows webcam access through a separate popup window.

## Technologies Used

- Python
- PyTorch
- Hugging Face Transformers
- SpeechRecognition
- Pyttsx3
- Tkinter
- OpenCV
- PIL (Pillow)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NiharRanjanMurudi/Speech_to_Speech_LLM_Bot.git
   ```
2. Navigate to the project directory:
   ```bash
   cd speech-to-speech-chatbot
   ```
3. Install dependencies:
   ```bash
   pip install torch transformers SpeechRecognition pyttsx3 opencv-python pillow
   ```
4. Download the pre-trained DialoGPT model:
   ```bash
   python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; AutoModelForCausalLM.from_pretrained('microsoft/DialoGPT-medium'); AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium')"
   ```

## Usage

1. Run the script:
   ```bash
   python chatbot.py
   ```
2. Use the graphical interface to:
   - Start/Stop the chatbot.
   - Interact via speech-to-speech communication.
   - Open the webcam window for live video capture.

## Future Enhancements

- Integration of more predefined topics.
- Improved conversational capabilities using fine-tuned models.
- Real-time sentiment analysis for better interaction.
