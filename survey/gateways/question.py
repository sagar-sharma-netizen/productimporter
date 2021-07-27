from contextlib import suppress
from typing import List, Dict
from survey.models import Question
from utils.paginator import paginate_queryset
from utils.exception import CustomException


def decode_question(question: Question) -> Dict:
    """
    Decode questions
    :param question:
    :return:
    """
    return question.as_dict


def create_question(question_data: Dict) -> Dict:
    question = Question(
        question=question_data.get("question"),
        details=question_data.get("details"),
        answer_type=question_data.get("answer_type")
    )
    question.save()
    return decode_question(question)


def list_questions(page: int, page_size: int) -> List[Dict]:
    questions = Question.objects.filter_is_active(is_active=True)
    data = paginate_queryset(questions, page=page, page_size=page_size)
    data["results"] = [decode_question(question) for question in questions]
    return data


def retrieve(pk: int) -> Dict:
    with suppress(Question.DoesNotExist):
        question = Question.objects.get(pk=pk)
        return decode_question(question)
    raise CustomException(
        title="Item not found",
        invalid_params=[]
    )
