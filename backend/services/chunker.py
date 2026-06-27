from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str, url: str, timestamp: str) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=64,
        separators=["\n\n", "\n", ".", " "]
    )

    raw_chunks = splitter.split_text(text)

    chunks = []
    for chunk in raw_chunks:
        if len(chunk.strip()) > 100:
            chunks.append({
                "text": chunk,
                "url": url,
                "timestamp": timestamp
            })

    return chunks
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if len(chunk.strip()) > 100:
            chunks.append({
                "text": chunk,
                "url": url,
                "timestamp": timestamp,
            })
        start = end - overlap

    return chunks