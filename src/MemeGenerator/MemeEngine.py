"""MemeEngine module to generate memes."""
import os
from random import randint
from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """MemeEngine module to generate memes."""

    def __init__(self, output_dir: str):
        """Initialize the Meme Generator.

        Args:
            output_dir (str): The directory where generated memes will be saved.

        Raises:
            ValueError: If output_dir is not a valid directory path.
            PermissionError: If the output directory is not writable.
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                raise Exception(f"Error creating output directory: {e}")

    def make_meme(
            self, img_path: str, text: str, author: str, width: int = 500
    ) -> str:
        """
        Create a meme by adding text and an author to the image.

        Args:
            img_path (str): Path to the image file.
            text (str): The main text for the meme.
            author (str): The author of the meme text.
            width (int): The width to scale the image to. Default is 500.

        Returns:
            str: The path to the saved meme image.
        """
        # Open the image
        try:
            img = Image.open(img_path)
        except Exception as e:
            raise FileNotFoundError(
                f"Error opening image file {img_path}: {e}"
            )

        # Resize the image
        try:
            original_width, original_height = img.size
            new_height = int((width / original_width) * original_height)
            img = img.resize((width, new_height))
        except Exception as e:
            raise Exception(f"Error resizing image: {e}")

        # Add quote and author
        try:
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.load_default()  # Load default font
            except IOError as e:
                raise Exception(f"Error loading font: {e}")

            full_text = f'"{text}"\n- {author}'
            bbox = draw.textbbox((0, 0), full_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            max_x = img.width - text_width - 20
            max_y = img.height - text_height - 20
            if max_x <= 0 or max_y <= 0:
                raise ValueError("Text does not fit on the image.")

            x_pos = randint(20, max_x)
            y_pos = randint(20, max_y)
            draw.text((x_pos, y_pos), full_text, font=font, fill="white")
        except Exception as e:
            raise Exception(f"Error adding text to image: {e}")

        # Save the image
        try:
            output_path = os.path.join(self.output_dir, "meme_image.png")
            img.save(output_path)
        except Exception as e:
            raise IOError(f"Error saving image to {output_path}: {e}")

        return output_path
