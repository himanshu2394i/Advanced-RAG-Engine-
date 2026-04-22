from search import create_sliding_chunks

def test_sliding_chunks_math():
    dummy_text="word1 word2 word3 word4 word5"
    chunks=create_sliding_chunks(dummy_text,words_per_chunk=3,overlap=1)

    assert len(chunks)==2
    assert chunks[0]=="word1 word2 word3"
    assert chunks[1]=="word3 word4 word5"
    