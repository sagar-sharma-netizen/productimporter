import traceback
from typing import Optional, List, Dict, Any, Tuple
from contextlib import suppress
from utils.exception import CustomException
from utils.handlers import handle_api_exception, api_handler
from products.gateways import product as product_gateway
from products.tasks.product_upload import process_upload
import time
import csv


@handle_api_exception
@api_handler()
def list_create_products(request_params, query_params: Dict, body: Dict, **kwargs):
    status = 200
    if request_params.get("method") == "POST":
        return create_product(request_params, body, **kwargs)
    page = query_params.get("page", 1)
    page_size = query_params.get("page_size", 10)
    data = product_gateway.list_products(page=page, page_size=page_size)
    return data, status


def create_product(request_params, body, **kwargs):
    status = 201
    products = product_gateway.list_products(page=1, page_size=100)
    # if len(products) >= 10:
    #     raise CustomException(
    #         title="A maximum of 10 questions can be created",
    #         detail="Maximum limit of questions reached"
    #     )
    if not (body.get('sku') and body.get('name') and body.get('details')):
        raise CustomException(
            title="sku, name and details are required!",
            invalid_params=[
                {
                    "sku": "P001",
                    "name": "SSD",
                    "details": "M.2 PCIE3x4 NVME SSD"
                }
            ]
        )
    data = product_gateway.create_product(
        product_data=body
    )
    return data, status


@handle_api_exception
@api_handler()
def retrieve(request_params, query_params: Dict, body: Dict, pk):
    status = 200
    with suppress(CustomException):
        body = product_gateway.retrieve(pk=pk)
        return body, status
    raise CustomException(
        title="Item not found",
        invalid_params=[]
    )


def validate_file_data(filepath):
    # validate file
    with open(filepath, 'rb+') as file_attachment:
        data = csv.reader(file_attachment, delimiter=',')
        headers = ["sku", "name", "details"]
        count = 0
        while count < len(headers):
            header = next(data)
            if not header in headers:
                raise CustomException(
                    title="Incorrect header",
                    invalid_params=[
                        header
                    ]
                )
            count += 1
    return True


@handle_api_exception
@api_handler()
def upload_products(request_params, query_params: Dict, body: Dict):
    status = 200
    if not body.get('file'):
        raise CustomException(
            title="No attachment provided",
            invalid_params=[
                "file"
            ]
        )
    # validate file data
    validate_file_data(body.get('file'))
    # upload file to temp dir
    with open(body.get('file'), 'rb+') as fileobj:
        # handle the uploaded file
        filepath = "/tmp/file_" + str(time.time()) + ".csv"
        with open(filepath, 'wb+') as dest:
            for chunk in fileobj.chunks():
                dest.write(chunk)
    # process file
    process_upload.delay(filepath)
    data = {
        "result": "Upload Started"
    }
    return data, status
