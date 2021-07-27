from typing import Optional, List, Dict, Any, Tuple
from contextlib import suppress
from utils.exception import CustomException
from utils.handlers import handle_api_exception, api_handler
from survey.gateways import question as question_gateway
from survey.gateways import survey as survey_gateway
from utils.email import send_mail
from django.contrib.sites.models import Site


@handle_api_exception
@api_handler()
def list_questions(request_params, query_params: Dict, body: Dict):
    page = query_params.get("page", 1)
    page_size = query_params.get("page_size", 10)
    data = question_gateway.list_questions(page=page, page_size=page_size)
    status = 200
    return data, status


@handle_api_exception
@api_handler()
def retrieve(request_params, query_params: Dict, body: Dict, pk):
    status = 200
    with suppress(CustomException):
        body = survey_gateway.retrieve_survey(pk=pk)
        return body, status
    raise CustomException(
        title="Item not found",
        invalid_params=[]
    )


@handle_api_exception
@api_handler()
def list_create(request_params, query_params: Dict, body: Dict, **kwargs):
    status = 200
    if request_params.get("method") == "POST":
        return create_survey(request_params, body, **kwargs)
    page = query_params.get("page", 1)
    page_size = query_params.get("page_size", 10)
    reporter_name = query_params.get("reporter_name", None)
    reporter_email = query_params.get("reporter_email", None)
    data = survey_gateway.list_survey(
        page=page, page_size=page_size, reporter_name=reporter_name, reporter_email=reporter_email
    )
    return data, status


def create_survey(request_params, body, **kwargs):
    status = 201
    if not (body.get('reporter_name') and body.get('reporter_email') and body.get('answers')):
        raise CustomException(
            title="Reporter name, email and answers are required!",
            invalid_params=[]
        )

    # validate answers
    validate_answers(body.get("answers"))
    data = survey_gateway.create_survey(survey_data=body)
    return data, status


def validate_answers(answers: List[Dict]) -> None:
    for item in answers:
        if not type(item) == dict:
            raise CustomException(
                title="each answer should be an object containing question_id, answer",
                invalid_params=[{"answers": [{"question_id": 1, "answer": 12}]}]
            )
        if not (item.get("question_id") and item.get("answer")):
            raise CustomException(
                title="each answer must have a question id and answer",
                invalid_params=[{"answers": [{"question_id": 1, "answer": 12}]}]
            )
        # validate question and answer type
        question = None
        with suppress(CustomException):
            question = question_gateway.retrieve(pk=item.get("question_id"))
        if not question:
            raise CustomException(
                title=f"Question with id: {item.get('question_id')} does not exist",
                invalid_params=[item]
            )


@handle_api_exception
@api_handler()
def mail_survey(request_params, query_params: dict, body: dict) -> Tuple[Dict, int]:
    if not request_params.get("method") == "POST":
        raise CustomException(
            title="Method not allowed",
            detail="POST"
        )
    status = 200
    if not (body.get("from") and body.get("recipients") and body.get("survey_id")):
        raise CustomException(
            title="Missing required data: from, recipients and survey_id",
            invalid_params=[
                {
                    "from": "from@domain.com",
                    "recipients": ["recipient1@domain.com", "recipient2@domain.com"],
                    "survey_id": 1
                }
            ]
        )
    if not(type(body.get("recipients")) == list):
        raise CustomException(
            title="recipients must be an array of emails",
            invalid_params=[
                {
                    "recipients": ["recipient1@domain.com"]
                }
            ]
        )
    domain = Site.objects.get_current().domain
    survey_link = f"http://{domain}/survey/{body.get('survey_id')}"
    send_mail(
        from_email=body.get("from"),
        recipients=body.get("recipients"),
        subject="Sample Survey",
        body=f"Please check this survey out here: {survey_link}"
    )
    return {}, status
