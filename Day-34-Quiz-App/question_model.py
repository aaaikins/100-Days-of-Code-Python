class Question:
    """
    A class to represent a single quiz question.
    """

    def __init__(self, q_text, q_answer):
        """
        Initialize a new Question instance.
        """
        self.text = q_text
        self.answer = q_answer
