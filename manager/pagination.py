# from rest_framework.pagination import PageNumberPagination
#
#
# class SubTaskPagination(PageNumberPagination):
#     page_size = 5                  # 5 объектов на страницу
#     page_query_param = "page"      # ?page=2
#     max_page_size = 5

from rest_framework.pagination import CursorPagination

class DefaultCursorPagination(CursorPagination):
    page_size = 6
    ordering = "-created_at"