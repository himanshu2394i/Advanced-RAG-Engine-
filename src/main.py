import logging
from chat import get_response
from search import load_knowledge
from memory import load_history

def main():
    logging.basicConfig( 
        filename="chatbot.log",
        level=logging.INFO,
        format="%(asctime)s-%(levelname)s: %(message)s"
    )
    logging.info("Application Started")
    load_knowledge()
    load_history()

    print("ChatBot Started! Type 'quit' to exit")
    print("Type 'clear' to reset history.\n")

    try:
        while True:
            user_input=input("You: ").strip()
            if user_input.lower()=="quit":
                print("Shutting Down")
                break
            if user_input.lower()=="clear":
                from src.memory import clear_history
                clear_history()
                print("History cleared\n")
            if user_input=="":
                continue
            response = get_response(user_input)
            
    except KeyboardInterrupt:
        print("\n[!] Force quit detected.")


    
if __name__=="__main__":
    main()