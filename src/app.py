"""Flask application for meme generation and management."""

import random
import os
import requests
from flask import Flask, render_template, request
import tempfile

from src.MemeGenerator.MemeEngine import MemeEngine
import glob

from src.QuoteEngine.Ingestor import Ingestor

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes_found = []
    for file in quote_files:
        for quote in Ingestor.parse(file):
            quotes_found.append(quote)

    images_path = "./_data/photos/dog/"
    img_extensions = ["*.jpg", "*.png"]

    images_found = []
    for ext in img_extensions:
        images_found.extend(glob.glob(os.path.join(images_path, ext)))

    return quotes_found, images_found


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')

    try:
        response = requests.get(image_url)
        response.raise_for_status()

        temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_image_path = temp_image.name
        with open(temp_image_path, 'wb') as f:
            f.write(response.content)
        temp_image.close()
    except requests.RequestException as e:
        return f"Error downloading image: {e}"

    generated_meme_path = meme.make_meme(temp_image_path, body, author)

    os.remove(temp_image_path)

    return render_template('meme.html', path=generated_meme_path)


if __name__ == "__main__":
    app.run()
