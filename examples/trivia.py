from anvolt.trivia import Trivia

trivia = Trivia(path="MyFolder/trivia.json")  # Default path is "AnVolt/trivia.json"


def add_trivia_question():
    question = "Who's maintain anvolt.py?"
    answer = "A"
    options = {"A": "Stawa", "B": "Tom", "C": "John"}

    trivia.add(
        question=question,
        answer=answer,
        options=options,
        difficulty="Easy",
        category="Information",
    )


add_trivia_question()


def delete_question():
    trivia.remove(question_id=1)  # Remove specific question ID


delete_question()


def play_on_console():
    trivia.play()  # Play on console


play_on_console()
