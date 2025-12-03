import os

def get_uique_output_path(input_path, suffix="_compressed"):
    """
    Generate a unique output file path by appending a suffix before the file extension.
    
    Args:
        original_path (str): The original file path.
        suffix (str): The suffix to append before the file extension.
        
    Returns:
        str: A new file path with the suffix added.
    """
    directory, filename = os.path.dirname(input_path), os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}{suffix}{ext}" # Create new filename with suffix
    outpout_path = os.path.join(directory, new_filename)
    counter = 1 # To handle potential name collisions
    while os.path.exists(outpout_path): # Check if file already exists
        new_filename = f"{name}{suffix}({counter}){ext}" # Append counter to filename
        outpout_path = os.path.join(directory, new_filename) # Create new output path
        counter += 1 # Increment counter
    return outpout_path 

def get_size_in_mb(file_path: str) -> float:
    """
    Get the size of a file in megabytes (MB).
    
    Args:
        file_path (str): The path to the file.

    Returns:
        float: The size of the file in MB.
    """
    if os.path.exists(file_path):
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024) # Convert bytes to MB
        return size_mb
    return 0

def format_size(size_in_mb: float) -> str:
    """
    Format the size in MB to a string with two decimal places.
    
    Args:
        size_in_mb (float): The size in megabytes.

    Returns:
        str: Formatted size string.
    """
    return f"{size_in_mb:.2f} MB"

def calculate_savings(original_size: float, compressed_size: float) -> float:
    """
    Calculate the percentage of size savings after compression.
    
    Args:
        original_size (float): The original file size in MB.
        compressed_size (float): The compressed file size in MB.

    Returns:
        float: The percentage of size savings.
    """
    if original_size == 0:
        return 0.0
    savings = ((original_size - compressed_size) / original_size) * 100
    return round(savings, 1)