from flask import Flask, send_file
import pyautogui
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Use ThreadPoolExecutor to handle requests concurrently
executor = ThreadPoolExecutor(max_workers=4)  # Adjust the number of workers as needed

def process_screenshot():
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Resize the screenshot to 128x128 pixels (using faster resampling method)
    screenshot = screenshot.resize((96, 64), Image.NEAREST)  # NEAREST for faster resizing

    # Save to an in-memory file
    img_byte_arr = io.BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr

@app.route('/screenshot', methods=['GET'])
def take_screenshot():
    # Run the screenshot processing asynchronously
    img_byte_arr = executor.submit(process_screenshot).result()

    # Return the image as a response
    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)  # Enable multithreading for handling requests
