from memory import add_history,get_history,clear_history

def test_adding_and_clearing_history():
    clear_history()
    add_history("user","Hello World!")
    current_history=get_history()

    assert len(current_history) == 1
    assert current_history[0]["role"]=="user"
    assert current_history[0]["content"]=="Hello World!"

    clear_history()
    assert len(get_history()) == 0