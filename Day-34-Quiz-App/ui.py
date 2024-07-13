import tkinter as tk
from quiz_brain import QuizBrain

# Define the theme color for the app
THEME_COLOR = "#375362"


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        """Initialize the QuizInterface with the quiz brain."""
        self.quiz = quiz_brain

        # Create the main window
        self.window = tk.Tk()
        self.window.title("Quiz App")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Create a label to display the score
        self.score_label = tk.Label(text='Score: 0', fg='white', bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        # Create a canvas to display the question
        self.canvas = tk.Canvas(width=300, height=250, bg='white')
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Question",
            font=("Ariel", 20, "italic"),
            fill=THEME_COLOR
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # Load images for the buttons
        cross_image = tk.PhotoImage(file="./images/false.png")
        self.wrong_button = tk.Button(image=cross_image, highlightthickness=0, command=self.false_pressed)
        self.wrong_button.grid(row=2, column=1)

        check_image = tk.PhotoImage(file="./images/true.png")
        self.right_button = tk.Button(image=check_image, highlightthickness=0, command=self.true_pressed)
        self.right_button.grid(row=2, column=0)

        # Fetch the first question
        self.get_next_question()

        # Start the main loop
        self.window.mainloop()

    def get_next_question(self):
        """Fetch the next question from the quiz and update the UI."""
        if self.quiz.still_has_questions():
            self.canvas.config(bg='white')
            self.score_label.config(text=f'Score: {self.quiz.score}')
            question_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=question_text)
        else:
            self.canvas.config(bg='white')
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz!")
            self.wrong_button.config(state=tk.DISABLED)
            self.right_button.config(state=tk.DISABLED)

    def true_pressed(self):
        """Handle the event when the 'True' button is pressed."""
        self.give_feedback(self.quiz.check_answer(user_answer='True'))

    def false_pressed(self):
        """Handle the event when the 'False' button is pressed."""
        self.give_feedback(self.quiz.check_answer(user_answer='False'))

    def give_feedback(self, is_right):
        """Provide feedback to the user based on their answer."""
        if is_right:
            self.canvas.config(bg='green')
        else:
            self.canvas.config(bg='red')
        # Wait for 1 second before showing the next question
        self.window.after(1000, self.get_next_question)
