from contextlib import suppress
from typing import List, Dict, Optional
from survey.models import Survey
from utils.paginator import paginate_queryset
from utils.exception import CustomException


def decode_survey(survey: Survey) -> Dict:
    """
    Decode survey
    :param survey:
    :return:
    """
    return survey.as_dict


def create_survey(survey_data: Dict) -> Dict:
    survey = Survey(
        reporter_name=survey_data.get("reporter_name"),
        reporter_email=survey_data.get("reporter_email"),
        answers=survey_data.get("answers")
    )
    survey.save()
    return decode_survey(survey)


def list_survey(page: int, page_size: int, reporter_name: Optional[str] = None, reporter_email: Optional[str] = None) -> List[Dict]:
    surveys = Survey.objects.filter_is_active(is_active=True)
    if reporter_name:
        surveys = surveys.filter(reporter_name__iexact=reporter_name)
    if reporter_email:
        surveys = surveys.filter(reporter_email__iexact=reporter_email)
    data = paginate_queryset(surveys, page=page, page_size=page_size)
    data["results"] = [decode_survey(survey) for survey in surveys]
    return data


def retrieve_survey(pk: int) -> Dict:
    with suppress(Survey.DoesNotExist):
        survey = Survey.objects.get(pk=pk)
        return decode_survey(survey)
    raise CustomException(
        title="Item not found",
        invalid_params=[]
    )

