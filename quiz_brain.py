class QuizBrain:
    def __init__(self, q_list):
        self.question_number = 0
        self.question_list = q_list
        self.score = 0

    def next_question(self):
        if self.question_number < len(self.question_list):
            current_question = self.question_list[self.question_number]
            self.question_number += 1
            user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False): ").strip()

            if user_answer.lower() == current_question.answer.lower():
                self.score += 1
                print("Correct!")
            else:
                print("Wrong!")
            print(f"Your current score is: {self.score}\n")
        else:
            print(f"Quiz Over! Your final score is: {self.score}")
