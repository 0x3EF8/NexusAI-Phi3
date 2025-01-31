import os
import sys
import io
import requests
import time
import threading
from tqdm import tqdm
from llama_cpp import Llama
import art
import pyperclip
import re

# Configuration Constants
MODELS = {
    "phi3": {
        "name": "Phi-3-mini-4k-instruct-q4.gguf",
        "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
    },
    "deepseek": {
        "name": "DeepSeek-R1-Distill-Qwen-1.5B-Q6_K.gguf",
        "url": "https://huggingface.co/bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-1.5B-Q6_K.gguf"
    }
}
MODEL_DIRECTORY = "models"
MAX_SEQUENCE_LENGTH = 4096
NUM_THREADS = 8
GPU_LAYERS = 35
MAX_TOKENS = 2048


# Custom prompt for AI initialization (can be disabled by setting to False)
# CUSTOM_PROMPT = "From now on, your name is NexusAI, developed by 0x3ef8. Act as a highly professional assistant with expertise in advanced programming concepts, tools, and best practices. Provide detailed, efficient, and professional responses."
CUSTOM_PROMPT = False
# Limit for conversation history (can be disabled by setting to False)
MAX_HISTORY_SIZE = False

# Monitoring and analytics
ENABLE_MONITORING = True  # Enable detailed response time and request tracking

class NexusAI:
    def __init__(self, model_directory: str):
        self.history = []
        self.num_requests = 0
        self.total_tokens = 0
        self.model_directory = model_directory
        self.current_model = None
        self.model = None

        if CUSTOM_PROMPT:
            self.history.append(f"<|assistant|>\n{CUSTOM_PROMPT}\n")

    def _ensure_model_exists(self, model_key: str):
        """Checks if the model exists locally; otherwise, downloads it."""
        model_info = MODELS[model_key]
        model_path = os.path.join(self.model_directory, model_info["name"])
        if os.path.exists(model_path):
            return

        print(f"[NexusAI] Model '{model_info['name']}' not found in the local repository.")
        print(f"[NexusAI] Downloading the required model from the server...")
        os.makedirs(self.model_directory, exist_ok=True)

        try:
            headers = {}
            current_size = 0
            if os.path.exists(model_path):
                current_size = os.path.getsize(model_path)
                headers['Range'] = f"bytes={current_size}-"

            with requests.get(model_info["url"], stream=True, headers=headers) as response:
                response.raise_for_status()
                total_size = int(response.headers.get("content-length", 0)) + current_size
                with open(model_path, "ab") as model_file, tqdm(total=total_size, unit="B", unit_scale=True, initial=current_size) as progress_bar:
                    for chunk in response.iter_content(chunk_size=8192):
                        model_file.write(chunk)
                        progress_bar.update(len(chunk))

            print(f"[NexusAI] The model has been successfully downloaded to '{model_path}'.")
        except requests.RequestException as e:
            raise Exception(f"[NexusAI] Model download failed: {e}")

    def load_model(self, model_key: str):
        """Loads the AI model into memory for interaction."""
        self._ensure_model_exists(model_key)
        model_path = os.path.join(self.model_directory, MODELS[model_key]["name"])
        print(f"[NexusAI] Loading the model from '{model_path}'...")
        self.model = Llama(
            model_path=model_path,
            n_ctx=MAX_SEQUENCE_LENGTH,
            n_threads=NUM_THREADS,
            n_gpu_layers=GPU_LAYERS,
            verbose=False
        )
        self.current_model = model_key

    def generate_response(self, prompt: str) -> str:
        """Generates a response to the given prompt using the loaded AI model."""
        if not self.model:
            return "[NexusAI] No model loaded. Please select a model first."

        self.num_requests += 1
        start_time = time.time()

        try:
            sys.stderr = io.StringIO()
            self.history.append(f"<|user|>\n{prompt}\n")

            if MAX_HISTORY_SIZE and len(self.history) > MAX_HISTORY_SIZE * 2:
                self.history = self.history[-(MAX_HISTORY_SIZE * 2):]

            spinner_thread = threading.Thread(target=self._show_loading_animation)
            spinner_thread.daemon = True  
            spinner_thread.start()

            response = self.model(
                f"{''.join(self.history)}\n<|assistant|>",
                max_tokens=MAX_TOKENS,
                stop=["<|end|>"],
                echo=False
            )

            response_text = response['choices'][0]['text'].strip()
            self.total_tokens += len(response_text.split())
            self.history.append(f"<|assistant|>\n{response_text}")

            self._stop_spinner(spinner_thread)

            end_time = time.time()
            response_time = end_time - start_time

            print(f"\nNexusAI Response: {response_text}\n")

            if ENABLE_MONITORING:
                print(f"\n[Monitoring Details]\n  • Response Time: {response_time:.2f} seconds\n  • Total Requests: {self.num_requests}\n  • Total Tokens Processed: {self.total_tokens}")

            return response_text

        except Exception as e:
            return f"[NexusAI] An error occurred: {e}"

        finally:
            sys.stderr = sys.__stderr__

    def reset_conversation(self):
        """Resets the conversation history and clears the screen."""
        os.system("cls" if os.name == "nt" else "clear")
        self.history = []
        if CUSTOM_PROMPT:
            self.history.append(f"<|assistant|>\n{CUSTOM_PROMPT}\n")
        print("\n[NexusAI] All conversation history has been reset. Feel free to start afresh.")
        show_ascii(self.current_model)
        return "[NexusAI] Conversation reset successfully."

    def show_help(self):
        """Displays a detailed help message with instructions for available commands."""
        return (
            "\n[NexusAI Help Center]\n\n"
            "Below is the list of commands you can use:\n\n"
            "  - 'exit'     : Safely terminates the program and exits.\n"
            "  - 'reset'    : Clears all conversation history and resets the AI's context.\n"
            "  - 'clear'    : Clears the screen for a cleaner workspace.\n"
            "  - 'cc'       : Copies the most recent code snippet from the AI's response to your clipboard.\n"
            "  - 'ca'       : Copies the latest full response from the AI to your clipboard.\n"
            "  - 'model'    : Allows you to select or change the AI model.\n\n"
            "Tips:\n"
            "• Use clear and concise prompts to get the best responses.\n"
            "• Reset the conversation if the AI's context becomes too long or irrelevant.\n"
            "For further assistance, contact the developer 0x3ef8.\n"
        )

    def clear_screen(self):
        """Clears the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def process_command(self, command: str):
        """Handles special commands like 'cc' (copy code) or 'ca' (copy response)."""
        if command.lower() == "cc":
            code = self.extract_code(self.history[-1])
            pyperclip.copy(code)
            print("[NexusAI] The most recent code snippet has been copied to your clipboard.")
        elif command.lower() == "ca":
            response = self.history[-1] if self.history else ""
            pyperclip.copy(response)
            print("[NexusAI] The latest AI response has been copied to your clipboard.")

    def extract_code(self, response: str) -> str:
        """Extracts code blocks from the AI's response."""
        match = re.search(r'```(.*?)```', response, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _show_loading_animation(self):
        """Displays a spinner while the AI is processing the request."""
        spinner = ["|", "/", "-", "\\"]
        self.spinner_running = True
        while self.spinner_running:
            try:
                for s in spinner:
                    print(f"\rNexusAI is processing... {s}", end="", flush=True)
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.spinner_running = False
                print("\r[NexusAI] Operation cancelled by user.")
                break

    def _stop_spinner(self, spinner_thread):
        """Stops the spinner but leaves it visible."""
        self.spinner_running = False
        spinner_thread.join()

# Show ASCII art
def show_ascii(model_name=None):
    ascii_art = art.text2art("NexusAI")
    lines = ascii_art.splitlines()
    ascii_with_name = "\n".join(lines[:-1]) + f"\n{' ' * (len(lines[-1]) - 20)}Developed by @0x3ef8"
    print(ascii_with_name)
    if model_name:
        print(f"\nCurrent Model: {MODELS[model_name]['name']}")
    print("\nType 'help' to show available commands or 'exit' to quit.\n")

def select_model():
    print("\nAvailable models:")
    for i, (key, value) in enumerate(MODELS.items(), 1):
        print(f"{i}. {value['name']}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the model you want to use: "))
            if 1 <= choice <= len(MODELS):
                return list(MODELS.keys())[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    try:
        assistant = NexusAI(MODEL_DIRECTORY)
        assistant.clear_screen()
        show_ascii()

        print("Please select a model to start.")
        model_key = select_model()
        assistant.load_model(model_key)
        assistant.clear_screen()
        show_ascii(model_key)

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == "exit":
                print("[NexusAI] Thank you for using NexusAI. Goodbye!")
                break

            if user_input.lower() == "reset":
                print(assistant.reset_conversation())
                continue

            if user_input.lower() == "help":
                print(assistant.show_help())
                continue

            if user_input.lower() == "clear":
                assistant.clear_screen()
                show_ascii(assistant.current_model)
                continue

            if user_input.lower() in ['cc', 'ca']:
                assistant.process_command(user_input.lower())
                continue

            if user_input.lower() == "model":
                model_key = select_model()
                assistant.load_model(model_key)
                assistant.clear_screen()
                show_ascii(model_key)
                continue

            if user_input:
                print()  
                assistant.generate_response(user_input)

    except KeyboardInterrupt:
        print("\n[NexusAI] Program terminated by user.")
    except Exception as e:
        print(f"[NexusAI] A critical error occurred: {e}")

if __name__ == "__main__":
    main()

