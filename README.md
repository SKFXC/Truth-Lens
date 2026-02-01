# Debate Assistant

Debate Assistant is a Python-based desktop utility designed for real-time text verification and fact-checking. It utilizes Optical Character Recognition (OCR) to extract text from the screen and processes it via user-configured Large Language Models (LLMs) such as DeepSeek or Perplexity.

## Features

- **Transparent Overlay:** Functions as a floating window that allows direct scanning of underlying content.
- **OCR Integration:** Uses Tesseract OCR to convert screen pixels into machine-readable text.
- **Universal API Support:** Compatible with any OpenAI-format API (DeepSeek, Perplexity, etc.).
- **Dynamic Interface:** Supports Light and Dark modes with a custom, borderless UI.
- **Resizable Window:** Includes a custom grip handler for resizing the capture area.

## Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR:** This software requires the Tesseract engine to be installed on the host machine.
   - Windows users: Ensure `tesseract.exe` is in the system PATH or configured in `main.py`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Debate-Assistant.git
   cd Debate-Assistant
