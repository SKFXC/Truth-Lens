import customtkinter as ctk
import tkinter as tk
from PIL import ImageGrab
import pytesseract
import threading
import requests
import json
import sys
import os

# --- CONFIGURATION ---
# 1. POINT TO YOUR TESSERACT INSTALLATION
# If you are on Windows, uncomment the line below and check the path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 2. API SETUP (Using Perplexity for live citations, or OpenAI)
API_KEY = "YOUR_PERPLEXITY_OR_OPENAI_KEY_HERE"
API_URL = "https://api.perplexity.ai/chat/completions" # Change to OpenAI URL if using GPT

class TruthWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Truth Lens v1.0")
        self.geometry("400x500")
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.90)
        self.overrideredirect(True) # Removes title bar
        
        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Variables
        self.lastClickX = 0
        self.lastClickY = 0

        # --- GUI LAYOUT ---
        self.setup_ui()
    
    def setup_ui(self):
        # 1. Custom Title Bar (Drag Handle)
        self.title_bar = ctk.CTkFrame(self, height=30, fg_color="#1a1a1a", corner_radius=0)
        self.title_bar.pack(fill="x", side="top")
        
        self.title_label = ctk.CTkLabel(self.title_bar, text=":: TRUTH LENS ::", text_color="#00ff00", font=("Consolas", 12, "bold"))
        self.title_label.pack(pady=2)

        # Bind dragging events
        self.title_bar.bind('<Button-1>', self.save_click_pos)
        self.title_bar.bind('<B1-Motion>', self.dragging)
        self.title_label.bind('<Button-1>', self.save_click_pos)
        self.title_label.bind('<B1-Motion>', self.dragging)

        # 2. Result Display Area
        self.result_box = ctk.CTkTextbox(self, width=380, height=350, font=("Roboto", 14))
        self.result_box.pack(pady=10)
        self.result_box.insert("0.0", "System Ready.\n1. Move window over suspicious text.\n2. Click SCAN.")

        # 3. Controls
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10, fill="x")

        self.scan_btn = ctk.CTkButton(self.btn_frame, text="SCAN REALITY", command=self.start_thread, width=200, fg_color="#008000", hover_color="#006400")
        self.scan_btn.pack(side="left", padx=20)

        self.exit_btn = ctk.CTkButton(self.btn_frame, text="EXIT", command=self.quit_app, width=100, fg_color="#8B0000", hover_color="#500000")
        self.exit_btn.pack(side="right", padx=20)

    # --- DRAGGING LOGIC ---
    def save_click_pos(self, event):
        self.lastClickX = event.x
        self.lastClickY = event.y

    def dragging(self, event):
        x = event.x_root - self.lastClickX
        y = event.y_root - self.lastClickY
        self.geometry(f"+{x}+{y}")

    # --- CORE LOGIC ---
    def start_thread(self):
        # We run this in a thread so the GUI doesn't freeze
        threading.Thread(target=self.process_scan, daemon=True).start()

    def process_scan(self):
        try:
            # 1. UI Feedback
            self.update_display("Scanning visual field...", clear=True)
            self.scan_btn.configure(state="disabled", text="SCANNING...")

            # 2. Capture Screen
            # Hide window momentarily so we don't screenshot the app itself
            self.withdraw() 
            self.update() # Force update
            
            # Get Coordinates
            x = self.winfo_x()
            y = self.winfo_y()
            w = self.winfo_width()
            h = self.winfo_height()
            
            # Grab Image (Pillow)
            # We add padding to capture slightly outside the window area if needed
            img = ImageGrab.grab(bbox=(x, y+30, x+w, y+h)) 
            
            # Show window again
            self.deiconify()

            # 3. OCR (Extract Text)
            self.update_display("Extracting text data...")
            extracted_text = pytesseract.image_to_string(img)
            
            if len(extracted_text.strip()) < 5:
                self.update_display("Error: No text detected.\nPlease place window over text.")
                self.reset_btn()
                return

            self.update_display(f"Analyzed Text Snippet:\n'{extracted_text[:100]}...'\n\nConsulting Knowledge Base...")

            # 4. API Call (The Brain)
            response = self.check_with_ai(extracted_text)
            
            # 5. Show Result
            self.update_display(response, clear=True)

        except Exception as e:
            self.update_display(f"Critical Error:\n{str(e)}")
            self.deiconify() # Ensure window comes back if it crashed while hidden
        
        finally:
            self.reset_btn()

    def check_with_ai(self, text):
        if "YOUR_KEY" in API_KEY:
            return "CONFIGURATION ERROR:\nPlease open main.py and insert your API Key."

        # Prompt Engineering
        payload = {
            "model": "llama-3.1-sonar-small-128k-online", # Perplexity Model
            "messages": [
                {
                    "role": "system",
                    "content": "You are a specialized fact-checking assistant. Analyze the user's text. 1. Determine if it is True, False, or Misleading. 2. Provide a brief explanation. 3. Cite a reputable source URL."
                },
                {
                    "role": "user",
                    "content": f"Verify this text: {text}"
                }
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            return f"Network Error: {e}"

    # --- HELPER FUNCTIONS ---
    def update_display(self, text, clear=False):
        # Must use .after() to update GUI from a separate thread
        self.after(0, self._safe_update, text, clear)

    def _safe_update(self, text, clear):
        if clear:
            self.result_box.delete("0.0", "end")
        self.result_box.insert("end", text + "\n")
        self.result_box.see("end")

    def reset_btn(self):
        self.after(0, lambda: self.scan_btn.configure(state="normal", text="SCAN REALITY"))

    def quit_app(self):
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = TruthWindow()
    app.mainloop()
