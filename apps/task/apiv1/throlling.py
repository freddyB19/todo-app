from rest_framework.throttling import UserRateThrottle

class CreateTaskThrottle(UserRateThrottle):
	scope = "task-create"


class ListTaskThrottle(UserRateThrottle):
	scope = "task-list"
	