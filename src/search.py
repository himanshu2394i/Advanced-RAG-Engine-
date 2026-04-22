import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi

model= SentenceTransformer("all-MiniLM-L6-v2")
reranker =CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
chroma_client=chromadb.Client()
collection=chroma_client.get_or_create_collection("knowledge")

documents=[]
bm25 = None
def create_sliding_chunks(text,words_per_chunk=100, overlap=20):
    if overlap>words_per_chunk:
        raise ValueError("overlap must be smaller than words_per_chunk")
    words= text.split()
    chunks=[]
    i=0
    while i+ words_per_chunk<=len(words):
        chunk_string=" ".join(words[i: i+words_per_chunk])
        chunks.append(chunk_string)
        i+=(words_per_chunk-overlap)
    return chunks

def load_knowledge(filepath="knowledge/notes.txt"):
    global documents,bm25

    with open(filepath,"r",encoding="utf-8") as f:
        full_text=f.read()
    documents=create_sliding_chunks(full_text,words_per_chunk=100,overlap=20)
    if not documents:
        print("knowledge base is empty")
        return
    

    embeddings=model.encode(documents).tolist()
    collection.upsert(
        documents=documents,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(documents))]
        )
    

    tokenized =[doc.lower().split() for doc in documents]
    bm25=BM25Okapi(tokenized)
    print(f"Loaded {len(documents)} knowledge entries.")

def search_knowledge(query,n_results=5):
    if not documents:
        return []
    query_embedding= model.encode([query]).tolist()
    semantic_results=collection.query(
        query_embeddings=query_embedding,
        n_results=len(documents)
    )
    semantic_docs= semantic_results["documents"][0]
    semantic_distances=semantic_results["distances"][0]

    max_dist=max(semantic_distances) or 1
    semantic_scores={
        doc:(1-dist/max_dist)*0.7
        for doc,dist in zip(semantic_docs,semantic_distances)
    }

    tokenized_query=query.lower().split()
    bm25_scores_raw=bm25.get_scores(tokenized_query)
    max_bm25=max(bm25_scores_raw) or 1
    bm25_scores={
        documents[i]: (score/max_bm25)*0.3
        for i, score in enumerate(bm25_scores_raw)
    }

    combined={}
    for doc in documents:
        combined[doc]=semantic_scores.get(doc,0)+bm25_scores.get(doc,0)

    ranked = sorted(combined.items(),key=lambda x: x[1],reverse=True)
    initial_docs =[doc for doc, score in ranked[:10]]

    if not initial_docs:
        return []
    
    pairs=[[query,doc] for doc in initial_docs]
    cross_scores=reranker.predict(pairs)
    reranked_docs_scores=zip(cross_scores,initial_docs)
    final_ranked=sorted(reranked_docs_scores,key=lambda x: x[0],reverse=True)

    return [doc for score,doc in final_ranked[:n_results]]

