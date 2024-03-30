from rest_framework import pagination


class TasksListPaginationPN(pagination.PageNumberPagination):
	page_size = 3
	page_query_param = 'page'
	page_size_query_param = 'size'
	last_page_strings = ('last',)
	max_page_size = 10


class TasksListPaginationLO(pagination.LimitOffsetPagination):
	default_limit = 5
	max_limit = 10
	

