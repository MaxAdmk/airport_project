from rest_framework.pagination import PageNumberPagination

class StandardResultSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    page_size_max = 100
    page_query_param = 'page'
    