from aiogram.filters.callback_data import CallbackData


class QueuesButtonInfo(CallbackData, prefix='queues_'):
    button_name: str


class UserIdButtonInfo(CallbackData, prefix='user_id_'):
    user_id: str


class UserDeletion(CallbackData, prefix='user_id_deletion_'):
    user_id: str
    queue_name: str


class UserAddition(CallbackData, prefix='user_id_adding_'):
    user_id: str
    queue_name: str


class DeleteQueue(CallbackData, prefix='delete_queue_'):
    queue_name: str


class RenameQueue(CallbackData, prefix='rename_queue_'):
    queue_name: str


class MakeQueue(CallbackData, prefix='make_queue_'):
    ...


class NoneInfo(CallbackData, prefix='none_'):
    ...


class ReturnToQueues(CallbackData, prefix='return_to_queues_'):
    ...
