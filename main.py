import tkinter as tk
from tkinter import messagebox
import random
from question_model import Question
from quiz_brain import QuizBrain
from data import question_data


THEME_COLOR = "#375362"
LIGHT_BLUE = "#E6F3FF"
CORRECT_COLOR = "#4CAF50"
INCORRECT_COLOR = "#F44336"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.geometry("850x530")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = tk.Label(text="Score: 0", fg="white", bg=THEME_COLOR, font=("Arial", 12, "bold"))
        self.score_label.grid(row=0, column=1, pady=(0, 10))

        self.canvas = tk.Canvas(width=800, height=350, bg=LIGHT_BLUE, highlightthickness=0)
        self.question_text = self.canvas.create_text(
            400, 175,
            width=780,
            text="Question goes here",
            fill=THEME_COLOR,
            font=("Arial", 16, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=30)

        self.true_button = tk.Button(text="True", bg="green", fg="white", font=("Arial", 14, "bold"),
                                     command=self.true_pressed, width=10, height=2)
        self.true_button.grid(row=2, column=0, pady=(0, 20))

        self.false_button = tk.Button(text="False", bg="red", fg="white", font=("Arial", 14, "bold"),
                                      command=self.false_pressed, width=10, height=2)
        self.false_button.grid(row=2, column=1, pady=(0, 20))

        self.progress_bar = tk.Canvas(width=800, height=20, bg=LIGHT_BLUE, highlightthickness=0)
        self.progress_bar.grid(row=3, column=0, columnspan=2)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg=LIGHT_BLUE)
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.update_progress_bar()
        else:
            self.canvas.itemconfig(self.question_text, text="You've completed the quiz!")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
            messagebox.showinfo("Quiz Completed", f"Your final score: {self.quiz.score}/{self.quiz.question_number}")

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg=CORRECT_COLOR)
        else:
            self.canvas.config(bg=INCORRECT_COLOR)
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.window.after(1000, self.get_next_question)

    def update_progress_bar(self):
        progress = self.quiz.question_number / len(self.quiz.questions)
        self.progress_bar.delete("all")
        self.progress_bar.create_rectangle(0, 0, 800 * progress, 20, fill=THEME_COLOR, width=0)

# Create question bank
question_bank = [Question(q["text"], q["answer"]) for q in question_data]
random.shuffle(question_bank)

# Create QuizBrain instance
quiz = QuizBrain(question_bank)

# Create and run the quiz interface
quiz_ui = QuizInterface(quiz)

