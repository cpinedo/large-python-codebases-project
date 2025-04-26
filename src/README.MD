# Overview

This application is intended to create memes from the provided images and quotes.

# Modules

## QuoteEngine

The Quote Ingestor module is designed to parse various file formats (CSV, DOCX, PDF, and TXT) containing quotes and authors. It includes a flexible Ingestor class that dynamically selects the appropriate parser based on the file extension. The quotes are parsed into QuoteModel instances, each containing a quote's body and author.

Supported file formats:

CSV: Comma-separated values.

DOCX: Microsoft Word documents.

PDF: Portable Document Format.

TXT: Plain text files with quotes formatted as "quote" - author.

## MemeGenerator

The `MemeGenerator` module allows you to create memes by adding a quote and an author to an image. The text is added to the image at a random position, and the image is resized to fit within a specified width while maintaining its aspect ratio. The final meme is saved as a PNG image.

# Execution

It provides 2 ways to execute it:

## Web app

features:
- Generate random memes from a collection of quotes and images.
- Create your own meme by uploading an image URL and adding your text.

How to Use:

Visit `/` to get a random meme.

Visit `/create` to make your own meme

## cli
Command-line tool to generate memes

Random meme
`python meme.py`

With arguments
`python meme.py --path "./_data/photos/dog/dog1.jpg" --body "foo!" --author "bar"`