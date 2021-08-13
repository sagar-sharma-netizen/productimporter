from celery import shared_task
from celery.utils.log import get_task_logger
from products.models.product import Product


logger = get_task_logger(__name__)


@shared_task(bind=True, track_started=True)
def process_csv(self, file_name: str):
    """
    async function to process csv file upload
    """
