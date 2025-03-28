import os
import logging
import shutil
from cryptography.fernet import Fernet
from PIL import Image
import pytesseract
import numpy as np
from src.config.config import UPLOAD_DIR, TESSERACT_PATH

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self):
        self.ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY", Fernet.generate_key())
        self.cipher_suite = Fernet(self.ENCRYPTION_KEY)
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    def ensure_upload_dir(self):
        """Ensure the upload directory exists"""
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

    def get_user_folder(self, telegram_id: int) -> str:
        """Create and return a unique folder for each user"""
        user_folder = os.path.join(UPLOAD_DIR, f"user_{telegram_id}")
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        return user_folder

    def encrypt_file(self, file_path: str) -> None:
        """Encrypt a file using Fernet encryption"""
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            encrypted_data = self.cipher_suite.encrypt(data)
            with open(file_path, "wb") as f:
                f.write(encrypted_data)
            logger.info(f"File encrypted: {file_path}")
        except Exception as e:
            logger.error(f"Encryption error on {file_path}: {e}")

    def decrypt_file(self, file_path: str) -> None:
        """Decrypt a file using Fernet encryption"""
        try:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()
            data = self.cipher_suite.decrypt(encrypted_data)
            with open(file_path, "wb") as f:
                f.write(data)
            logger.info(f"File decrypted: {file_path}")
        except Exception as e:
            logger.error(f"Decryption error on {file_path}: {e}")

    def save_user_files(self, context) -> None:
        """Move temporary files to user's permanent folder"""
        user_folder = self.get_user_folder(context.user_data.get('telegram_id'))
        for key in ['doc_path', 'id_path', 'selfie_path', 'signature_path']:
            file_path = context.user_data.get(key)
            if file_path and os.path.exists(file_path):
                new_path = os.path.join(user_folder, os.path.basename(file_path))
                shutil.move(file_path, new_path)
                context.user_data[key] = new_path
                logger.info(f"Moved {key} to {new_path}")

    def delete_temp_files(self, context) -> None:
        """Delete temporary files if loan process is cancelled"""
        for key in ['doc_path', 'id_path', 'selfie_path', 'signature_path']:
            file_path = context.user_data.get(key)
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted temporary file for {key}: {file_path}")
                except Exception as e:
                    logger.error(f"Error deleting temporary file {file_path}: {e}")

    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from an image using OCR"""
        try:
            self.decrypt_file(image_path)
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            self.encrypt_file(image_path)
            logger.info(f"OCR extracted text: {text}")
            return text.strip()
        except Exception as e:
            logger.error(f"OCR extraction error: {e}")
            return ""

    def validate_signature_image(self, file_path: str) -> bool:
        """Validate if uploaded image appears to be a digital signature"""
        try:
            with Image.open(file_path) as img:
                gray = img.convert("L")
                arr = np.array(gray)
                dark_pixels = np.sum(arr < 200)  # Count pixels darker than 200
                total_pixels = arr.size
                ratio = dark_pixels / total_pixels
                logger.info(f"Dark pixel ratio: {ratio:.4f}")
                return 0.005 < ratio < 0.15
        except Exception as e:
            logger.error(f"Error validating signature image: {e}")
            return False