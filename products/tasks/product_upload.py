from celery import task
from products.gateways import product as product_gateway
from utils.logger import Logger
import traceback
import csv


def process_row(data):
    try:
        product = product_gateway.filter_products(sku=data.get("sku"))
        if product:
            return product_gateway.update_product(pk=product.get('pk'), data=data)
        return product_gateway.create_product(data)
    except Exception as e:
        error = traceback.format_exc()
        Logger.error(error)
        return error


@task
def process_upload(self, filepath, progress_observer):
    # process file upload here
    with open(filepath, 'rb') as fileobj:
        data = csv.DictReader(fileobj, delimiter=',')
        for row in data:
            process_row(row)
    return "Completed"
