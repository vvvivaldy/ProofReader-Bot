from enum import Enum


class User(str, Enum):
    CREATE_SUB_UID = "/v5/user/create-sub-member"
    CREATE_SUB_API_KEY = "/v5/user/create-sub-api"
    GET_SUB_UID_LIST = "/v5/user/query-sub-members"
    FREEZE_SUB_UID = "/v5/user/frozen-sub-member"
    GET_API_KEY_INFORMATION = "/v5/user/query-api"
    MODIFY_MASTER_API_KEY = "/v5/user/update-api"
    MODIFY_SUB_API_KEY = "/v5/user/update-sub-api"
    DELETE_MASTER_API_KEY = "/v5/user/delete-api"
    DELETE_SUB_API_KEY = "/v5/user/delete-sub-api"

    def __str__(self) -> str:
        return self.value
