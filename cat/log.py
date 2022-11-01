import json

log_path = 'cat/log.json'

def read_log(user):
    with open(log_path, 'r') as f:
        data = json.load(f)
    return data[user]


def write_log(user, status):
    with open(log_path, 'r') as f:
        data = json.load(f)
    data[user] = status
    with open(log_path, 'w') as f:
        json.dump(data, f)