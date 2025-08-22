#!/usr/bin/env python3

# depends on "spectacle" to be installed, tested on KDE Plasma6/Wayland
# waiting for a better/faster solution

from flask import Flask, Response
import subprocess
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/screenshot')
def screenshot():
    try:
        # Capture screenshot using spectacle
        result = subprocess.run(
            ['spectacle', '-o', '/dev/stdout', '-n', '-b', '-m'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True
        )

        # Open image from binary output
        image = Image.open(BytesIO(result.stdout))

        # Resize to 10% of original size
        new_size = (image.width // 10, image.height // 10)
        image = image.resize(new_size, Image.LANCZOS)

        # Convert to RGB (JPEG doesn't support alpha)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Save to buffer as JPEG
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)

        return Response(buffer.read(), mimetype='image/jpeg')
    except subprocess.CalledProcessError:
        return "Failed to capture screenshot", 500
    except Exception as e:
        return f"Error processing image: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)

