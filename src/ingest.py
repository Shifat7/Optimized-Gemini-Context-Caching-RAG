

def load_and_segment_transcript(path, max_words=800, overlap_words=100):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # maintain semantic structure of paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    chunks = []
    current_chunk = []
    current_word_count = 0

    for paragraph in paragraphs:
        paragraph_words = paragraph.split()
        paragraph_words_count = len(paragraph_words)

        # finalize current chunk if paragraph word count exceeds max_words
        if current_word_count + paragraph_words_count > max_words and current_word_count > 0:
            chunks.append(' '.join(current_chunk))

            # record overlapped words from end of previous chunk
            overlap_start = max(0, len(current_chunk) - overlap_words)
            current_chunk = current_chunk[overlap_start:]
            current_word_count = len(current_chunk)

        current_chunk.extend(paragraph_words)
        current_word_count += paragraph_words_count

    # adding last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks