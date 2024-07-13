from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
from ui import QuizInterface

# Create a list to store Question objects
question_bank = []

# Iterate through the question data to create Question objects
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

# Initialize the QuizBrain with the list of questions
quiz = QuizBrain(question_bank)

# Initialize the QuizInterface with the quiz brain
quiz_ui = QuizInterface(quiz)

