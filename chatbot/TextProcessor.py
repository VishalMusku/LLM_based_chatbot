import re

def read_entire_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def estimate_token_count(text):
    return len(text.split())

def split_text_into_chunks_at_page_breaks(text, n=4):
    page_break_pattern = r"--- Page \d+ ---"
    pages = re.split(page_break_pattern, text)
    if pages and not pages[0].strip():
        pages = pages[1:]
    pages_per_chunk = max(len(pages) // n, 1)
    chunks = []
    for i in range(0, len(pages), pages_per_chunk):
        chunk = ''.join(pages[i:i+pages_per_chunk])
        chunks.append(chunk)
        if len(chunks) == n:
            break
    if len(chunks) < n:
        chunks[-1] += ''.join(pages[i+pages_per_chunk:])
    return chunks

def erase_file_content(file_path):
    try:
        with open(file_path, 'w') as file:
            file.truncate(0)  # This ensures that the file is completely empty

    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")