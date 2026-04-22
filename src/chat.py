import os
from dotenv import load_dotenv
from memory import get_history,add_history
from search import search_knowledge
from model import AnthropicLLM,OllamaLLM,LLMRouter
import ollama

load_dotenv()
anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")

with open("system_prompt.txt","r",encoding="utf-8") as f:
    System_Prompt=f.read()

claude= AnthropicLLM(api_key=anthropic_api_key)
local_llama=OllamaLLM(model_name="llama3.2")

router= LLMRouter(fallback_chain=[claude,local_llama])

def get_response(user_input):
    current_history=get_history()

    if len(current_history)>10:
        old_messages=current_history[:6]
        compression_prompt="You are a memory optimizer.Summarize the following conversation history briefly,retaining only key facts and user preferences." 
        summary=router.run(old_messages,compression_prompt,stream_to_console=False)
        from memory import compress_history
        compress_history(6,summary)
    
    relevant_docs=search_knowledge(user_input)
    compressed_content=""
    if relevant_docs:
        raw_context="\n".join(relevant_docs)
        compression_prompt="You are an expert fact extractor. Read the provided Documents. Extract ONLY the specific sentences that answer the User's Question. If the answer is not in the documents, output exactly nothing."
        payload=[{"role":"user","content":f"Documents:\n{raw_context}\n\nQuestion: {user_input}"}]
        compressed_content=router.run(payload,compression_prompt,stream_to_console=False)


    argumented_input=f"""Relevant knowledge extracted:{compressed_content}
    User question: {user_input}"""

    message_payload=get_history()+[{"role":"user","content":argumented_input}]
    reply = router.run(message_payload,System_Prompt)
    
    add_history("user",user_input)
    add_history("assistant",reply)

    return reply
    
    

    