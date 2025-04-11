
def load_and_segment_transcript(path, max_words=800, overlap_words=100):
    """
    Load a transcript from a file and segment it into chunks with a maximum word count.
    
    Args:
        path: Path to the transcript file
        max_words: Maximum number of words per chunk
        overlap_words: Number of words to overlap between chunks
        
    Returns:
        List of text chunks
    """
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if not text.strip():
        return []
    
    words = text.split()
    if max_words >= len(words) and overlap_words == 0:
        return [text]
    
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    chunks = []
    i = 0
    while i < len(words):
        end = min(i + max_words, len(words))
        
        chunk = ' '.join(words[i:end])
        chunks.append(chunk)
        
        # Moving forward by (max_words - overlap_words) even if overlap is large
        step = max(1, max_words - overlap_words)
        i += step
    
    # making sure paragraphs are preserved when possible
    preserved_paragraphs = []
    for paragraph in paragraphs:
        paragraph_words = paragraph.split()
        if len(paragraph_words) <= max_words:
            # checking if this paragraph is already contained in any chunk
            if not any(paragraph in chunk for chunk in chunks):
                preserved_paragraphs.append(paragraph)
    
    chunks.extend(preserved_paragraphs)
    
    return chunks
