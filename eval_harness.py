from src.model import LLMRouter, OllamaLLM

def evaluate_rag(question, retrieved_context, generated_answer):
    judge = LLMRouter(fallback_chain=[OllamaLLM()])

    eval_prompt= """You are an impartial AI judge evaluating a RAG system.
    Please evaluate the following on a scale of 1 to 5:
    
    1. Context Precision: Did the context actually contain the answer, or was it useless?
    2. Faithfulness: Is the generated answer hallucinating, or sticking strictly to context facts?
    
    Return your scores in this precise format:
    Context Score: [1-5]
    Faithfulness Score: [1-5]
    Reasoning: [1 short sentence explaining why]
    """
    payload=    [{
        "role":"user",
        "content":f"Question: {question}\nContent:{retrieved_context}\nAnswer: {generated_answer}"}]
    print("\n--- RAG Evalution Metrics ---")
    judge.run(payload, eval_prompt, stream_to_console=True)

if __name__=="__main__":
    evaluate_rag(
        question="What us Hybrid Search?",
        retrieved_context="Hybrid search uses both keyword based enginen like BM25 and vector based semantic search.",
        generated_answer="Hybrid search combines BM25 and semantic search."
    )
      