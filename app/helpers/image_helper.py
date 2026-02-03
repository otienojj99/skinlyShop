import cloudinary
import cloudinary.uploader
from uuid import uuid4


class ImageHelper:
    @staticmethod
    def upload_product_image(file, folder: str = "products"):
        public_id = f"{folder}/{uuid4()}"
        
        result = cloudinary.uploader.upload(
            file,
            public_id=public_id,
            resource_type="image",
            overwrite=True,
        )
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
        }
        
    @staticmethod
    def delete_image(public_id: str):
        cloudinary.uploader.destroy(public_id)