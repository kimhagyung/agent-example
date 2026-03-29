

from typing import Literal
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field, List

class Question(BaseModel):
    question : str = Field(description="The quiz question text")
    options : List[str] = Field(description="Exactyle 4 multiple choice options, labeled A,B,C or D")
    conrrect_answer : str = Field(description="The correct answer (MUST MATCH ONE of 'options)")
    explanation : str = Field(
        description="Explantion of why the answer is correct and the other ones are wrong"
    )

class Quiz(BaseModel): 
    topic : str = Field(description="THe main topic being tested")
    questions : List[Question] = Field(description="List of the quiz questions")

@tool
def generate_quiz(
    research_text : str,
    topic : str,
    difficulty: Literal[
        "easy",
        "medium",
        "hard",
    ],
    num_questions:int, 
):
    model = init_chat_model("openai:gpt-4o")
    structured_model = model.with_structured_output(Quiz)

    prompt = f"""
    Create a {difficulty} quiz, about {topic} with {num_questions} using the following research information.

    <RESEARCH_TEXT>
    {research_text}
    </RESEARCH_TEXT>
    """