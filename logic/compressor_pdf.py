from pypdf import PdfReader, PdfWriter

def compress_pdf(input_path, output_path):
    """
    Optimizes a PDF by cleaning structure and compressing streams.
    """
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)

        # 4. Metadata compression
        if reader.metadata is not None:
            writer.add_metadata(reader.metadata)
        
        # Compress content streams (images/text inside PDF)
        for page in writer.pages:
            page.compress_content_streams()

        with open(output_path, "wb") as f:
            writer.write(f)
            
        return True
    except Exception as e:
        print(f"PDF Error {input_path}: {e}")
        return False