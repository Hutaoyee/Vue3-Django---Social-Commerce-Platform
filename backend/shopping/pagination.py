from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    """
    商品分页类，默认每页20个SPU
    """
    page_size = 20  # 默认每页20条
    page_size_query_param = 'page_size'  # 允许客户端通过 page_size 参数指定
    max_page_size = 100  # 最大每页100条
