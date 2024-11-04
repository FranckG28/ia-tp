import datetime
import os
from typing import Final
from PIL import Image


class ImageProcessor:
    output_path: Final[str] = "dataset"
    padding_color: Final[str] = (114, 114, 114)

    def __init__(self, path: str):
        self._path = path

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    @staticmethod
    def is_image(file: str) -> bool:
        """Check if the file is an image

        Args:
            file (str): The file name
        Returns:
            bool: True if the file is an image, False otherwise
        """
        return file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".jpg")

    def resize_image(self, image: Image, size: int) -> Image:
        """Resize the image to a square with the given size

        Args:
            image (Image): The image to resize
            size (int): The size of the square

        Returns:
            Image: The resized image
        """
        resized_image = Image.new("RGB", (size, size), self.padding_color)
        if image.width == image.height:
            resized_image.paste(image.resize((size, size)))
        elif image.width > image.height:
            height = int(size * image.height / image.width)
            resized_image.paste(image.resize((size, height)))
        else:
            width = int(size * image.width / image.height)
            resized_image.paste(image.resize((width, size)))
        return resized_image

    def process_folder(self) -> None:
        """Process all the images in the folder

        This method will process all the images in the folder and save them in the output folder

        Returns:
            None
        """
        for file in os.listdir(self._path):
            if self.is_image(file):
                self.process_image(file)

    def save_image(self, image: Image, file: str) -> None:
        """Save the image to the output folder

        Args:
            image (Image): The image to save
            file (str): The file name

        Returns:
            None
        """
        now = datetime.datetime.now()
        image.save(f"{self.output_path}/{now.strftime('%Y%m%d%H%M%S')}_{file}")

    def process_image(self, file: str) -> None:
        """Process the image

        This method will resize the image to a square with a size of 640x640 and save it in the output folder

        Args:
            file (str): The file name

        Returns:
            None
        """
        image = Image.open(f"{self._path}/{file}")
        resized_image = self.resize_image(image, 640)
        self.save_image(resized_image, file)
