from contextlib import suppress
from typing import List, Dict
from products.models import Product
from utils.paginator import paginate_queryset
from utils.exception import CustomException


def decode_product(product: Product) -> Dict:
    """
    Decode questions
    :param product:
    :return:
    """
    return product.as_dict


def create_product(product_data: Dict) -> Dict:
    product = Product(
        sku=product_data.get("sku"),
        name=product_data.get("name"),
        details=product_data.get("details")
    )
    product.save()
    return decode_product(product)


def list_products(page: int, page_size: int) -> List[Dict]:
    products = Product.objects.filter_is_active(is_active=True)
    data = paginate_queryset(products, page=page, page_size=page_size)
    data["results"] = [decode_product(product) for product in products]
    return data


def retrieve(pk: int) -> Dict:
    with suppress(Product.DoesNotExist):
        product = Product.objects.get(pk=pk)
        return decode_product(product)
    raise CustomException(
        title="Item not found",
        invalid_params=[]
    )


def filter_products(sku: str):
    products = Product.objects.filter(sku__iexact=sku)
    return decode_product(products[0])


def update_product(pk: int, data: dict):
    product = Product.objects.get(pk=pk)
    product.sku = data.get('sku')
    product.name = data.get('name')
    product.details = data.get("details")
    return decode_product(product)
