def chunk_text(text: str,chunk_size: int = 500,overlap: int = 50):
    chunks = []
    start = 0
    index = 0


    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append((index,chunk))
        index += 1
        start += chunk_size - overlap
<<<<<<< HEAD

    # print("hii chunks:", chunks)
=======
    
>>>>>>> 4efc8fe8579685c2241a39edbde6ddf18fd84c1f
    return chunks