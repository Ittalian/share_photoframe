import config

from flask import Flask, request, jsonify
import threading
from PIL import Image, ImageTk
import tkinter as tk
import requests
from io import BytesIO
from queue import Queue
import os

app = Flask(__name__)

root = tk.Tk()
root.geometry("800x600")
root.title(config.title)

canvas = tk.Canvas(root, bg="black")
canvas.pack(fill="both", expand=True)

image_queue = Queue()

def load_background_image():
    if os.path.exists(config.background_image_path):
        bg_img = Image.open(config.background_image_path)
        bg_img = bg_img.resize((root.winfo_width(), root.winfo_height()))
        return ImageTk.PhotoImage(bg_img)
    return None

background_tk_image = None

def poll_queue():
    global background_tk_image
    try:
        while not image_queue.empty():
            img = image_queue.get()
            canvas.delete("all")

            background_tk_image = load_background_image()
            if background_tk_image:
                canvas.create_image(0, 0, anchor="nw", image=background_tk_image)

            canvas.create_image(
                root.winfo_width() // 2,
                root.winfo_height() // 2,
                anchor="center",
                image=img,
                tags="main_image"
            )
            canvas.image = img
    except Exception as e:
        print(f"画像の更新に失敗: {e}")

    root.after(100, poll_queue)

def fetch_and_queue_image(url):
    try:
        response = requests.get(url, timeout=10)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)

        max_w, max_h = root.winfo_width(), root.winfo_height()
        img.thumbnail((max_w, max_h))

        photo = ImageTk.PhotoImage(img)
        image_queue.put(photo)

    except Exception as e:
        print(f"画像の表示に失敗: {e}")

@app.route('/display', methods=['POST'])
def display():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    threading.Thread(target=fetch_and_queue_image, args=(url,), daemon=True).start()
    return jsonify({'status': 'Image is being queued for display'}), 200

def start_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    threading.Thread(target=start_flask, daemon=True).start()
    root.after(100, poll_queue)
    root.mainloop()
