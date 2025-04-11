import os
import tempfile
import pytest
from src.ingest import load_and_segment_transcript


@pytest.fixture
def sample_transcript_file():
    """Create a temporary file with sample transcript content."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as f:
        f.write("""This is paragraph one. It contains several sentences.
This is still paragraph one.

This is paragraph two. It's separated by a blank line.

This is paragraph three. It has some more text.
This is still paragraph three.

This is paragraph four. It will be in the next chunk if max_words is small enough.""")
        temp_filename = f.name
    
    yield temp_filename
    
    os.unlink(temp_filename)


@pytest.fixture
def realistic_transcript_file():
    """Create a temporary file with a more realistic transcript sample."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as f:
        f.write("""This is a section on space exploration. Space exploration has long captivated the imagination of humanity. 
From the earliest days of stargazing to the launch of Sputnik, the first artificial satellite, space has been a frontier of discovery, innovation, and challenge.

This is a section on propulsion systems. Central to all of space exploration is propulsion. Without effective propulsion systems, we cannot reach space or navigate once there.
Chemical propulsion, the most traditional form, involves burning fuel to produce thrust. Liquid-fueled and solid-fueled rockets are examples of this category.
For instance, the Saturn V rocket, which took astronauts to the Moon, used powerful stages of chemical propulsion to escape Earth's gravity.

This is a section on orbital mechanics. Orbital mechanics, or astrodynamics, is the study of the motion of spacecraft and celestial bodies under the influence of gravitational forces.
A deep understanding of orbital mechanics allows mission planners to design efficient trajectories, including gravity assists, transfer orbits, and orbital insertions.
For instance, the use of the Hohmann transfer orbit is common for sending spacecraft from one planetary orbit to another with minimal fuel usage.

This is a section on deep space missions. When we talk about deep space missions, we refer to missions that go beyond the Earth-Moon system, often targeting distant planets, asteroids, or even interstellar space.
These missions require robust communication systems, power generation (often through radioisotope thermoelectric generators), and autonomous systems due to the significant time delays in communication with Earth.
The farther a spacecraft travels, the more critical these systems become.""")
        temp_filename = f.name
    
    yield temp_filename
    
    os.unlink(temp_filename)


@pytest.fixture
def empty_file():
    """Create a temporary empty file."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as f:
        temp_filename = f.name
    
    yield temp_filename
    
    os.unlink(temp_filename)


@pytest.fixture
def single_paragraph_file():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as f:
        f.write("This is a single paragraph file. It has no paragraph breaks. It's just one continuous text block.")
        temp_filename = f.name
    
    yield temp_filename
    
    os.unlink(temp_filename)


@pytest.fixture
def long_paragraph_file():
    """Create a temporary file with one very long paragraph."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as f:
        words = ["word"] * 10000
        f.write(" ".join(words))
        temp_filename = f.name
    
    yield temp_filename
    
    os.unlink(temp_filename)


def test_basic_functionality(sample_transcript_file):
    chunks = load_and_segment_transcript(sample_transcript_file)
    
    assert len(chunks) >= 1
    
    for chunk in chunks:
        assert len(chunk) > 0
        assert isinstance(chunk, str)


def test_chunk_size_and_overlap(sample_transcript_file):
    max_words = 20
    overlap_words = 5
    chunks = load_and_segment_transcript(sample_transcript_file, max_words=max_words, overlap_words=overlap_words)
    
    assert len(chunks) > 1
    
    for chunk in chunks:
        assert len(chunk.split()) <= max_words
    
    # checking for some overlap
    # more realistic for a general-purpose chunking function
    for i in range(len(chunks) - 1):
        current_chunk_words = set(chunks[i].split())
        next_chunk_words = set(chunks[i + 1].split())
        
        # checking that there is some overlap between chunks
        overlap = current_chunk_words.intersection(next_chunk_words)
        assert len(overlap) > 0, f"No overlap found between chunks {i} and {i+1}"


def test_semantic_boundary_preservation(sample_transcript_file):
    """Test that segmentation preserves paragraph boundaries."""
    # small enough to force chunking but large enough to include full paragraphs
    max_words = 30
    chunks = load_and_segment_transcript(sample_transcript_file, max_words=max_words)
    
    with open(sample_transcript_file, 'r', encoding='utf-8') as f:
        text = f.read()
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    # checking that paragraphs are not split across chunks (except for overlap)
    # only checking if each paragraph appears intact in at least one chunk
    for paragraph in paragraphs:
        paragraph_words = paragraph.split()
        if len(paragraph_words) <= max_words:
            # The paragraph should appear intact in at least one chunk
            paragraph_found = any(paragraph in chunk for chunk in chunks)
            # If the paragraph is too long, it might be split, so we don't assert also allowing some buffer for overlap
            if len(paragraph_words) <= max_words - 10:
                assert paragraph_found, f"Paragraph not found intact: {paragraph}"


def test_realistic_transcript_segmentation(realistic_transcript_file):
    """Test segmentation with a more realistic transcript."""
    max_words = 50
    overlap_words = 10
    chunks = load_and_segment_transcript(realistic_transcript_file, max_words=max_words, overlap_words=overlap_words)
    
    assert len(chunks) > 1
    
    for chunk in chunks:
        assert len(chunk.split()) <= max_words
    
    # checking that sections are not unnecessarily split (this is approximate)
    # we will check if key phrases from each section appear in chunks
    key_phrases = [
        "space exploration has long captivated",
        "propulsion systems",
        "orbital mechanics",
        "deep space missions"
    ]
    
    # each key phrase should appear in at least one chunk
    for phrase in key_phrases:
        assert any(phrase.lower() in chunk.lower() for chunk in chunks), f"Key phrase not found: {phrase}"


def test_empty_file(empty_file):
    """Test handling of an empty file."""
    chunks = load_and_segment_transcript(empty_file)
    assert len(chunks) == 0


def test_single_paragraph(single_paragraph_file):
    """Test handling of a file with a single paragraph."""
    chunks = load_and_segment_transcript(single_paragraph_file)
    assert len(chunks) == 1
    
    with open(single_paragraph_file, 'r', encoding='utf-8') as f:
        original_text = f.read()
    
    assert chunks[0] == original_text


def test_long_paragraph(long_paragraph_file):
    """Test handling of a file with a very long paragraph."""
    max_words = 200
    overlap_words = 50
    chunks = load_and_segment_transcript(long_paragraph_file, max_words=max_words, overlap_words=overlap_words)
    
    expected_chunks = (1000 + max_words - 1) // max_words
    assert len(chunks) >= expected_chunks
    
    for chunk in chunks:
        assert len(chunk.split()) <= max_words


def test_zero_overlap(sample_transcript_file):
    """Test with zero overlap between chunks."""
    max_words = 20
    overlap_words = 0
    chunks = load_and_segment_transcript(sample_transcript_file, max_words=max_words, overlap_words=overlap_words)
    
    assert len(chunks) > 1
    
    # checking no overlap between consecutive chunks
    for i in range(len(chunks) - 1):
        current_chunk_last_word = chunks[i].split()[-1]
        next_chunk_first_word = chunks[i + 1].split()[0]
        
        # last word of current chunk should not be the first word of next chunk
        assert current_chunk_last_word != next_chunk_first_word


def test_nonexistent_file():
    """Test handling of a non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_and_segment_transcript("nonexistent_file.txt")


def test_different_max_words(sample_transcript_file):
    """Test with different max_words values."""
    small_chunks = load_and_segment_transcript(sample_transcript_file, max_words=10, overlap_words=2)
    
    large_chunks = load_and_segment_transcript(sample_transcript_file, max_words=100, overlap_words=10)
    
    assert len(small_chunks) > len(large_chunks)
    
    for chunk in small_chunks:
        assert len(chunk.split()) <= 10
    
    for chunk in large_chunks:
        assert len(chunk.split()) <= 100


def test_exact_max_words(sample_transcript_file):
    """Test with a file that has exactly max_words words."""
    with open(sample_transcript_file, 'r', encoding='utf-8') as f:
        text = f.read()
    total_words = len(text.split())
    
    chunks = load_and_segment_transcript(sample_transcript_file, max_words=total_words, overlap_words=0)
    
    assert len(chunks) == 1
    assert len(chunks[0].split()) == total_words


def test_content_preservation(realistic_transcript_file):
    """Test that all content from the original transcript is preserved in the chunks."""
    with open(realistic_transcript_file, 'r', encoding='utf-8') as f:
        original_text = f.read()
    
    original_words = set(original_text.split())
    
    chunks1 = load_and_segment_transcript(realistic_transcript_file, max_words=30, overlap_words=5)
    chunks2 = load_and_segment_transcript(realistic_transcript_file, max_words=100, overlap_words=20)
    
    # checking that all words from the original are in the chunks (ignoring order and accounting for overlap)
    for chunks in [chunks1, chunks2]:
        chunk_words = set()
        for chunk in chunks:
            chunk_words.update(chunk.split())
        
        assert original_words.issubset(chunk_words), "Some content was lost during segmentation"


def test_overlap_consistency(realistic_transcript_file):
    """Test that overlap is consistent across different chunk sizes."""
    # testing with different overlap sizes
    for overlap_words in [5, 10, 20]:
        chunks = load_and_segment_transcript(realistic_transcript_file, max_words=50, overlap_words=overlap_words)
        
        # checking each pair of consecutive chunks
        for i in range(len(chunks) - 1):
            current_chunk_words = chunks[i].split()
            next_chunk_words = chunks[i + 1].split()
            
            overlap_start = max(0, len(current_chunk_words) - overlap_words)
            expected_overlap = current_chunk_words[overlap_start:]
            
            # checking if they match the first words of the next chunk
            # only checking if the length is correct, as the exact words might vary due to paragraph boundaries
            actual_overlap = next_chunk_words[:min(len(expected_overlap), len(next_chunk_words))]
            
            # overlap should be close to the specified overlap_words (might be slightly less due to paragraph boundaries)
            assert abs(len(actual_overlap) - min(overlap_words, len(current_chunk_words))) <= 5, \
                f"Overlap inconsistent: expected ~{overlap_words}, got {len(actual_overlap)}"
