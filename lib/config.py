from dotenv import load_dotenv
load_dotenv()

import os

title = os.getenv('TITLE')
background_image_path = os.getenv('BACKGROUND_IMAGE_PATH')
