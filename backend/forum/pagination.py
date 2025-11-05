from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    自定义分页类，支持客户端通过 page_size 参数控制每页数量
    """
    page_size = 10  # 默认每页10条
    page_size_query_param = 'page_size'  # 允许客户端通过 page_size 参数指定
    max_page_size = 1000  # 最大每页1000条
