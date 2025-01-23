import os
import io
import sys
import requests
from tqdm import tqdm  
from llama_cpp import Llama

# Configuration Constants (Easily Adjustable)
MODEL_FILENAME = "Phi-3-mini-4k-instruct-q4.gguf"  # Model filename
MODEL_DIRECTORY = "model"  # Directory where the model will be stored
MAX_SEQUENCE_LENGTH = 4096  # Maximum sequence length (context size)
NUM_THREADS = 8  # Number of CPU threads to use
GPU_LAYERS = 35  # Number of layers to offload to GPU
MAX_TOKENS = 2048  # Maximum tokens to generate per response
MODEL_URL = "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"  # Model download URL


class NexusAI:
    def __init__(self, model_directory: str, model_filename: str):
        self._ensure_model_exists(model_directory, model_filename)
        self.model = self._load_model(model_directory, model_filename)

    @staticmethod
    def _ensure_model_exists(model_directory: str, model_filename: str):
        model_path = os.path.join(model_directory, model_filename)
        if os.path.exists(model_path):
            return

        os.makedirs(model_directory, exist_ok=True)
        try:
            
            print("[NexusAI] Model not found. Downloading...\n")
            response = requests.get(MODEL_URL, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))  
            with open(model_path, "wb") as model_file:
                with tqdm(total=total_size, unit="B", unit_scale=True, desc=MODEL_FILENAME) as bar:
                    for chunk in response.iter_content(chunk_size=8192):
                        model_file.write(chunk)
                        bar.update(len(chunk)) 

            print(f"[NexusAI] Model downloaded successfully: {model_path}")
        except requests.RequestException as e:
            raise Exception(f"Failed to download the model: {e}")

    @staticmethod
    def _load_model(model_directory: str, model_filename: str) -> Llama:
        model_path = os.path.join(model_directory, model_filename)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file '{model_filename}' not found.")
        return Llama(
            model_path=model_path,
            n_ctx=MAX_SEQUENCE_LENGTH,
            n_threads=NUM_THREADS,
            n_gpu_layers=GPU_LAYERS,
            verbose=False
        )

    def generate_response(self, prompt: str) -> str:
        try:
            sys.stderr = io.StringIO()

            response = self.model(
                f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
                max_tokens=MAX_TOKENS,
                stop=["<|end|>"],
                echo=False
            )
            return response['choices'][0]['text'].strip()

        except Exception as e:
            return f"Error: Unable to generate response. Details: {e}"

        finally:
            sys.stderr = sys.__stderr__


def main():
    print("\n[NexusAI] Welcome to NexusAI.")
    print("[NexusAI] Type 'exit' to terminate the program.\n")

    try:
        assistant = NexusAI(MODEL_DIRECTORY, MODEL_FILENAME)
        print("[NexusAI] Model successfully loaded.\n")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                print("[NexusAI] Session terminated. Goodbye!")
                break

            if user_input:
                response = assistant.generate_response(user_input)
                print(f"NexusAI: {response}\n")

    except Exception as e:
        print(f"[NexusAI] Critical Error: {e}")


if __name__ == "__main__":
    main()
