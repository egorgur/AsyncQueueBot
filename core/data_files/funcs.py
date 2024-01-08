import json
from jsonhandler import read_json, write_json

"""Check functions"""


def in_dictionary(dictionary: dict, key=None, item=None):
    if key:
        return key in dictionary.keys()
    if item:
        return item in dictionary.items()
    return False


def user_id_in_user_dict(user_id: str) -> bool:
    users_dict = read_json('users_id_dict.json')
    return in_dictionary(users_dict, key=user_id)


def user_id_in_queue(user_id: str, queue_name: str) -> bool:
    if queue_exists(queue_name):
        print('123123213321')
        queue_list = read_json('queue_list.json')
        queue = queue_list[queue_name]
        return in_dictionary(queue, item=user_id)
    else:
        return False


def queue_exists(queue_name: str) -> bool:
    queue_list = read_json('queue_list.json')
    print(in_dictionary(queue_list, key=queue_name))
    return in_dictionary(queue_list, key=queue_name)


def position_is_occupied(position: str, queue_name: str) -> bool:
    if queue_exists(queue_name):
        queue_list = read_json('queue_list.json')
        return in_dictionary(queue_list[queue_name], key=position)


"""Check functions"""
"""Get info functions"""


def get_user_pos(user_id: str, queue_name: str) -> int:
    if user_id_in_queue(user_id, queue_name):
        queue_list = read_json('queue_list.json')
        queue = queue_list[queue_name]
        print('////////////')
        return queue.keys()[queue.values().index(user_id)]


"""Get info functions"""


def find_last_empty_pos_in_queue(queue: dict) -> int:
    positions = list(queue.keys())
    positions.sort()
    for i in range(len(positions) + 1):
        print(i + 1, positions[i])
        if i + 1 < positions[i]:
            return i + 1


def add_user_to_user_dict(user_id: str, user_name: str) -> bool:
    users_list = read_json('users_id_dict.json')
    if not user_id_in_user_dict(user_id):
        users_list[user_id] = user_name
        write_json('users_id_dict.json', users_list)
        return True
    else:
        return False


def add_user_to_last_position_in_queue(user_id: str, queue_name: str) -> bool:
    if not user_id_in_queue(user_id, queue_name):
        queue_list = read_json('queue_list.json')
        queue = queue_list[queue_name]
        queue_pos = find_last_empty_pos_in_queue(queue)
        queue[queue_pos] = user_id
        queue_list[queue_name] = queue
        write_json('queue_list.json',queue_list)
        return True
    else:
        return False


def add_user_to_spec_position_in_queue(user_id: str, position: str, queue_name: str) -> bool:
    if not user_id_in_queue(user_id, queue_name):
        if not position_is_occupied(position, queue_name):
            queue_list = read_json('queue_list.json')
            queue_list[queue_name][position] = user_id
    else:
        ...
    ...


def delete_user_from_queue(user_id: str, queue_name: str) -> bool:
    if user_id_in_queue(user_id, queue_name):
        queue_list = read_json('queue_list.json')
        queue_list[queue_name].pop(user_id)
        write_json('queue_list.json', queue_list)
        return True
    else:
        return False


def make_new_queue(queue_name: str) -> bool:
    if not queue_exists(queue_name):
        queue_list = read_json('queue_list.json')
        queue_list[queue_name] = {}
        write_json('queue_list.json', queue_list)
        return True
    else:
        return False


def delete_queue(queue_name: str) -> bool:
    queue_list = read_json('queue_list.json')
    if queue_exists(queue_name):
        queue_list.pop(queue_name)
        return True
    else:
        return False


test_dict = {
    "name": {
        "1": 11,
        "2": 22,
        "4": 44,
    }
}
print(in_dictionary(test_dict,key='name'))
print(get_user_pos(22, 'name'))
