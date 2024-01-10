from core.data_files.jsonhandler import read_json, write_json

"""Check functions"""


def in_dictionary(dictionary: dict, key=None, value=None):
    if key:
        return key in dictionary.keys()
    if value:
        return value in dictionary.values()
    return False


def user_id_in_registered_users(user_id: str) -> bool:
    users_dict = read_json('users_info.json')
    return in_dictionary(users_dict, key=user_id)


def user_id_in_queue(user_id: str, queue_name: str) -> (bool, str):
    if queue_exists(queue_name):
        queue_list = read_json('queue_list.json')
        queue = queue_list[queue_name]
        return in_dictionary(queue, value=user_id)
    else:
        return 'Queue_not_exists'


def queue_exists(queue_name: str) -> bool:
    queue_list = read_json('queue_list.json')
    return in_dictionary(queue_list, key=queue_name)


def position_is_occupied(position: str, queue_name: str) -> (bool, str):
    if queue_exists(queue_name):
        queue_list = read_json('queue_list.json')
        return in_dictionary(queue_list[queue_name], key=position)
    else:
        return 'Queue_not_exists'


"""/Check functions"""
"""Get functions"""


def get_user_pos(user_id: str, queue_name: str) -> (int, str):
    if user_id_in_queue(user_id, queue_name) == 'Queue_not_exists':
        return 'Queue_not_exists'
    elif user_id_in_queue(user_id, queue_name):
        queue_list = read_json('queue_list.json')
        queue = queue_list[queue_name]
        return list(queue.keys())[list(queue.values()).index(user_id)]
    else:
        return 'No_user_in_queue'


def get_user_id_by_pos(position: str, queue_name: str) -> str:
    if position_is_occupied(position, queue_name) == 'Queue_not_exists':
        return 'Queue_not_exists'
    elif position_is_occupied(position, queue_name):
        queue_list = read_json('queue_list.json')
        queue = queue_list[queue_name]
        return list(queue.values())[list(queue.keys()).index(position)]
    else:
        return 'Position_is_empty'


def get_positions_in_queue(queue_name: str) -> list:
    if queue_exists(queue_name):
        queue_list = read_json('queue_list.json')
        queue = queue_list[queue_name]
        positions = list(queue.keys())
        positions.sort()
        return positions


def get_users_in_queue(queue_name: str) -> list:
    positions = get_positions_in_queue(queue_name)
    users = [get_user_id_by_pos(positions[i], queue_name) for i in range(len(positions))]
    return users


def get_all_queue_names() -> list:
    queue_list = read_json('queue_list.json')
    return list(queue_list.keys())


"""/Get info functions"""


def find_last_empty_pos_in_queue(queue: dict) -> str:
    positions = list(map(int, (queue.keys())))
    if positions:
        positions.sort()
        empty_pos = 1
        while True:
            if empty_pos in positions:
                empty_pos += 1
            else:
                return str(empty_pos)
    else:
        return "1"


def add_user_to_registered_users(user_id: str, user_name: str) -> bool:
    users_list = read_json('users_info.json')
    if not user_id_in_registered_users(user_id):
        users_list[user_id] = user_name
        write_json('users_info.json', users_list)
        return True
    else:
        return False


def add_user_to_last_position_in_queue(user_id: str, queue_name: str) -> (bool, str):
    if user_id_in_queue(user_id, queue_name) == 'Queue_not_exists':
        return 'Queue_not_exists'
    if not user_id_in_queue(user_id, queue_name):
        queue_list = read_json('queue_list.json')
        queue = queue_list[queue_name]
        queue_pos = find_last_empty_pos_in_queue(queue)
        queue[queue_pos] = user_id
        queue_list[queue_name] = queue
        write_json('queue_list.json', queue_list)
        return True
    else:
        return 'user_already_in_queue'


def add_user_to_specific_position_in_queue(user_id: str, position: str, queue_name: str) -> (bool, str):
    if not user_id_in_queue(user_id, queue_name):
        if not position_is_occupied(position, queue_name):
            queue_list = read_json('queue_list.json')
            queue = queue_list[queue_name]
            queue[position] = user_id
            queue_list[queue_name] = queue
            write_json('queue_list.json', queue_list)
            return True
        else:
            return 'position_is_occupied'
    else:
        return 'user_already_in_queue'


def delete_user_from_queue(user_id: str, queue_name: str) -> (bool, str):
    if user_id_in_queue(user_id, queue_name) == 'Queue_not_exists':
        return 'Queue_not_exists'
    elif user_id_in_queue(user_id, queue_name):
        user_pos = get_user_pos(user_id, queue_name)
        queue_list = read_json('queue_list.json')
        queue_list[queue_name].pop(user_pos)
        write_json('queue_list.json', queue_list)
        return True
    else:
        return 'No_user_in_queue'


def make_new_queue(queue_name: str) -> (bool, str):
    if not queue_exists(queue_name):
        queue_list = read_json('queue_list.json')
        queue_list[queue_name] = {}
        write_json('queue_list.json', queue_list)
        return True
    else:
        return 'Queue_exists'


def delete_queue(queue_name: str) -> (bool, str):
    queue_list = read_json('queue_list.json')
    if queue_exists(queue_name):
        queue_list.pop(queue_name)
        write_json('queue_list.json', queue_list)
        return True
    else:
        return 'Queue_not_exist'
