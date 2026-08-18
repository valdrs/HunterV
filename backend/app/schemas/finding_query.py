from enum import Enum


class FindingSort(str, Enum):
    ID = "id"
    SEVERITY = "severity"
    STATUS = "status"
    TARGET_ID = "target_id"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"