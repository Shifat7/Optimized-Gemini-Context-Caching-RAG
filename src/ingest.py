

def load_and_segment_transcript(path, max_words=800):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    words = text.split()
    chunks = [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]
    return chunks