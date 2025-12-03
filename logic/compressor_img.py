from PIL import Image
import os

def compress_image(input_path: str, output_path: str, quality:int =80, max_width: int =1920) -> bool:
    """Compress an image and optionally resize it to a maximum width.
    Args:
        input_path (str): The path to the input image.
        output_path (str): The path to save the compressed image.
        quality (int): The quality level for compression (Default is 80).
        max_width (int): The maximum width to resize the image to. If the image is wider, it will be resized proportionally.
    """
    try:
        with Image.open(input_path) as img:
            # 1.Format gestion PNG to JPEG conversion 
            outpout_ext = os.path.splitext(output_path)[1].lower()
            if outpout_ext in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # 2. Resize if needed
            if max_width and img.width > max_width: # Resize only if image is wider than max_width
                ratio = max_width / float(img.width) # Calculate resize ratio to maintain aspect ratio
                new_height = int(float(img.height) * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS) # Resize imag, using high-quality resampling (LANCZOS)

            # 3. Save compressed image with optimized settings
            #'optimize = True' helps reduce file size without quality loss
            if outpout_ext in ['.jpg', '.jpeg']:
                img.save(output_path, format='JPEG', quality= int(quality) ,optimize =True)
            elif outpout_ext == '.png': # For PNG, 'quality' is not used, but we can use compress_level (0-9)
                img.save(output_path, format='PNG', optimize=True, compress_level=9)
            else:
                img.save(output_path)
        return True
    except Exception as e:
        print("Erreur image {input_path}: {e}")
        return False