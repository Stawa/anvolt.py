import os
import random
import json
import time
from typing import Union, Tuple, Optional


class Trivia:
    def __init__(self, path: str = "AnVolt/trivia.json"):
        self.path = path
        self.trivia = {"questions": {}}

    def _ensure_file_exists(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.isfile(self.path):
            with open(self.path, "w") as file:
                json.dump({"questions": {}}, file)

    def _next_id(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                ids = list(map(int, json.load(file)["questions"]))
                return max(ids + [0]) + 1 if ids else 1
        except:
            return 1

    def add(self, question: str, answer: str, options: dict, **kwargs) -> str:
        self._ensure_file_exists()
        question_id = self._next_id()
        question_data = {
            "question": question,
            "answer": answer,
            "options": options,
            "difficulty": kwargs.get("difficulty"),
            "category": kwargs.get("category"),
        }

        try:
            with open(self.path, "r") as file:
                self.trivia = json.load(file)
        except json.decoder.JSONDecodeError:
            pass

        self.trivia["questions"][question_id] = question_data
        with open(self.path, "w") as file:
            json.dump(self.trivia, file, indent=4, ensure_ascii=False)
        return f"Question (#{question_id}) added"

    def remove(self, question_id: Union[int, str]) -> str:
        self._ensure_file_exists()
        with open(self.path, "r") as file:
            self.trivia = json.load(file)

        if str(question_id) in self.trivia["questions"]:
            self.trivia["questions"].pop(str(question_id))
            with open(self.path, "w") as file:
                json.dump(self.trivia, file, indent=4, ensure_ascii=False)
            return f"Question (#{question_id}) Removed"

        return "Trivia: No Question Found"

    def run(self, question_id: Optional[int] = None) -> Tuple:
        self._ensure_file_exists()

        with open(self.path, "r") as f:
            data = json.load(f)["questions"]

        if question_id is None:
            question_id = random.choice(list(data.keys()))

        question = data.get(str(question_id))
        if question:
            return (
                question_id,
                question["question"],
                question["answer"],
                question["options"],
                question.get("difficulty"),
                question.get("category"),
            )

        return f"No question with id {question_id} was found"

    def answer(self, run, guess: Optional[str] = None) -> Tuple:
        if guess is None:
            return False, run[2]
        return (guess.lower() == run[2].lower(), run[2])

    def play(self) -> None:
        score = 0
        self._ensure_file_exists()

        try:
            with open(self.path, "r") as f:
                questions = json.load(f)["questions"]
        except json.decoder.JSONDecodeError:
            print("No question found")
            return

        for question_id, question in questions.items():
            options = [f"{k}. {v}" for k, v in question["options"].items()]

            print(f"Question: {question['question']}")
            print(f"Options: {', '.join(options)}")
            print(f"Difficulty: {question.get('difficulty')}")
            print(f"Category: {question.get('category')}")
            answer = input("Answer: ")

            if answer.lower() == question["answer"].lower():
                score += 1
                print("That's correct!")
            else:
                print("That's incorrect!")
            time.sleep(2)

        print(f"\nGame over! Score: {score}/{len(questions)}")
