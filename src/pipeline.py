from src.ingest import load_and_segment_transcript
from src.summarize import summarize_chunk
from src.embed_retrieve import build_index, retrieve
from src.qa_mock import mock_gemini_qa

def run_pipeline(transcript_path, questions):
    chunks = load_and_segment_transcript(transcript_path)
    summaries = [summarize_chunk(c) for c in chunks]
    model, index, _ = build_index(chunks)
    answers = {}
    for q in questions:
        context = retrieve(q, model, index, chunks)
        ctx_text = '\n'.join(context)
        answers[q] = mock_gemini_qa(q, ctx_text)
    
    return answers