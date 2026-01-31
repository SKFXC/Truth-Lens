# Truth Lens 👁️
A Python-based floating window that performs real-time fact-checking on any text on your screen using OCR and AI.

## 🚀 The Problem
The internet is full of irrational arguments and fake news. Copy-pasting text to verify it takes too long.

## 💡 The Solution
**Truth Lens** is a transparent overlay. Move it over a tweet, comment, or article, click **SCAN**, and it will:
1. Capture the screen area (OCR).
2. Send the text to the Perplexity/OpenAI API.
3. Return a verdict with citations instantly.

## 🛠️ Installation

1. **Install Tesseract OCR**
   - Windows: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - Mac: `brew install tesseract`

2. **Clone the Repo**
   ```bash
   git clone https://github.com/SKFXC/Truth-Lens.git
   cd Truth-Lens
