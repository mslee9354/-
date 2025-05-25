import json
from flask import Flask, request, jsonify
import threading
import tkinter as tk

# Placeholder for KoAlpaca model integration
# In a real setup, load the KoAlpaca model from HuggingFace or local directory.
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
except ImportError:
    AutoModelForCausalLM = None  # type: ignore
    AutoTokenizer = None  # type: ignore

app = Flask(__name__)

latest_result = ""

def analyze_entry(text: str) -> str:
    """Analyze entry purpose and destination text using KoAlpaca.

    Returns "예" or "아니요". If unsure, return "아니요".
    """
    global AutoModelForCausalLM, AutoTokenizer
    if AutoModelForCausalLM is None:
        # Model not available; return default response.
        return "아니요"
    if AutoModelForCausalLM is not None:
        # Example generation code. The actual model path must be provided by user.
        tokenizer = AutoTokenizer.from_pretrained("beomi/KoAlpaca-Polyglot-12.8B")
        model = AutoModelForCausalLM.from_pretrained(
            "beomi/KoAlpaca-Polyglot-12.8B",
            device_map="auto",
            torch_dtype=torch.float16,
        )
        prompt = f"위의 사람이 위병소에 출입하려하는데 적절해? 예/아니요로 답하고 애매하면 아니요로 답해.\n{text}"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        output = model.generate(**inputs, max_new_tokens=10)
        answer = tokenizer.decode(output[0], skip_special_tokens=True)
        if "예" in answer:
            return "예"
        return "아니요"
    return "아니요"

@app.route('/check', methods=['POST'])
def check_entry():
    """Receive data from client and evaluate."""
    global latest_result
    data = request.get_json(force=True)
    purpose = data.get('purpose', '')
    destination = data.get('destination', '')
    text = f"목적: {purpose} 행선지: {destination}"
    result = analyze_entry(text)
    latest_result = json.dumps({
        'person': data.get('person', {}),
        'purpose': purpose,
        'destination': destination,
        'result': result,
    }, ensure_ascii=False, indent=2)
    return jsonify({'result': result})


def start_gui():
    """Start a simple Tkinter GUI to display the latest result."""
    root = tk.Tk()
    root.title("Guard Post Control")
    text = tk.Text(root, height=20, width=60)
    text.pack()

    def refresh():
        text.delete('1.0', tk.END)
        text.insert(tk.END, latest_result)
        root.after(1000, refresh)

    refresh()
    root.mainloop()


def run_app():
    threading.Thread(target=start_gui, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    run_app()
