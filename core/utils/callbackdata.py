from aiogram.filters.callback_data import CallbackData


class QueuesButtonInfo(CallbackData, prefix='queues_'):
    button_name: str


class UserToSwap(CallbackData, prefix='swap_'):
    user_1_id: str
    user_2_id: str
    queue_name: str


class UserIdButtonInfo(CallbackData, prefix='user_id_'):
    user_id: str


class UserDeletion(CallbackData, prefix='user_id_deletion_'):
    user_id: str
    queue_name: str


class UserAddition(CallbackData, prefix='user_id_adding_'):
    user_id: str
    queue_name: str


class SpecUserAdditionCall(CallbackData, prefix='spec_user_id_menu_'):
    user_id: str
    queue_name: str


class SpecUserAddition(CallbackData, prefix='spec_user_id_adding_'):
    position: str
    user_id: str
    queue_name: str


class DeleteQueue(CallbackData, prefix='delete_queue_'):
    queue_name: str


class DeleteTimedQueue(CallbackData, prefix='delete_timed_queue_'):
    queue_name: str


class RenameQueue(CallbackData, prefix='rename_queue_'):
    queue_name: str


class MakeQueue(CallbackData, prefix='make_queue_'):
    ...


class MakeTimedQueue(CallbackData, prefix='make_timed_'):
    ...


class TimedQueues(CallbackData, prefix='timed_queue_'):
    ...


class NoneInfo(CallbackData, prefix='none_'):
    ...


class ReturnToQueues(CallbackData, prefix='return_to_queues_'):
    ...


class QueuesControl(CallbackData, prefix='return_to_queues_control_'):
    ...
