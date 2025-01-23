
# NexusAI-Phi3

NexusAI-Phi3 is a simple AI assistant that works offline, powered by the **Phi-3-mini-4k-instruct** model. It’s designed to provide intelligent responses using a pre-trained language model, with easy setup and minimal configuration.

---

## Features

- **Offline Operation**: After the model is downloaded, no internet connection is needed.
- **Lightweight**: Runs well on most systems.
- **Customizable**: You can adjust settings to fit your needs.
- **Easy Interaction**: Just type and get responses.

---

## Prerequisites

To get NexusAI-Phi3 running, you'll need:

- Python 3.9 or higher
- pip (Python’s package installer)

---

## Installation & Setup

### 1. Clone or Download the Repository

Start by cloning or downloading this repository to your computer.

```bash
git clone https://github.com/0x3EF8/NexusAI-Phi3.git
cd NexusAI-Phi3
```

### 2. Install Python Dependencies

Next, install the necessary libraries using `pip`. It’s recommended to use a virtual environment for easier management, though it’s optional.

#### Using a Virtual Environment (Optional):

```bash
python -m venv venv # On Linux/macOS
source venv/bin/activate # On Windows
venv\Scripts\activate

```

#### Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Download the Model

If the model isn’t already in the `model/` folder, it will automatically be downloaded when you run the program. 

If for any reason the model isn’t found, the script will download it from Hugging Face. You can also manually download the model [here](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf).

---

## Configuration

Here are some settings you can adjust in the script:

- **MODEL_FILENAME**: The filename of the model (currently set to `"Phi-3-mini-4k-instruct-q4.gguf"`).
- **MODEL_DIRECTORY**: The folder where the model file will be stored (defaults to `"model"`).
- **MAX_SEQUENCE_LENGTH**: Maximum sequence length (context size) for the model.
- **NUM_THREADS**: Number of CPU threads to use.
- **GPU_LAYERS**: How many layers to offload to GPU, if available.
- **MAX_TOKENS**: The maximum number of tokens generated in each response.

These values are set to reasonable defaults, but feel free to change them if needed.

---

## Running NexusAI

Once everything is set up, you can start the AI assistant with:

```bash
python Nexus.py
```

The assistant will prompt you for input, and you can start asking questions right away.

### Example Usage:

- **Start chatting**: Type your question and press Enter.
- **Exit**: Type `exit` to stop the program.

---

## Example Interaction:

```bash
[NexusAI] Welcome to NexusAI! Type 'exit' to quit.

You: What is the capital of Southern Leyte?
NexusAI: The capital of Southern Leyte is Maasin City.
```

---

## Troubleshooting

- **Model download fails**: If there’s an issue with downloading the model, make sure your internet connection is working. If needed, you can manually download the model and place it in the `model/` folder.
  
- **Python dependencies**: Ensure you’re using Python 3.9 or higher and that `pip` is up-to-date if you run into any issues installing dependencies.

---

## License

This project is licensed under the MIT License. You can find the full license [here](LICENSE).

---

## Acknowledgments

- The **Llama** model framework and the **Phi-3-mini-4k-instruct** model from Hugging Face make this project possible.

---

Thank you for using **NexusAI**. If you have any suggestions or questions, feel free to reach out or contribute to the repository!

