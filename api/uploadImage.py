import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from decouple import config

# Configuration       
cloudinary.config( 
    cloud_name = config('CLOUDINARY_APP_NAME'),
    api_key = config('CLOUDINARY_API_KEY'),
    api_secret = config('CLOUDINARY_API_SECRET_KEY'),
    secure=True
)

# Upload an image
upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
                                           public_id="shoes")
print(upload_result["secure_url"])

# Optimize delivery by resizing and applying auto-format and auto-quality
optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
print(optimize_url)

# Transform the image: auto-crop to square aspect_ratio
auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
print(auto_crop_url)