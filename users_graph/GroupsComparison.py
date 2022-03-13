import requests

token_list = ['9ad97d27909034b7b5d65167b35f3617867732f85b0f3c6f38527138a999bed72c287e7752322c48fda1b',  # мамин
              '46dd8d5dde569ef05784bf2faa176652a36441907fca84a9caf186a04ac610ced8251350f44e91bda8545',  # мой
              '71ce357930df58936799d99ee53e8b4b16d5a1ff3e970bde6f3dee95bede9639078356ebab2f630be2b55',  # мой 2
              ]

user_id1 = 305617399
user_id2 = 102353058
n = 1


def groups(identifier, token):
    payload = {'user_id': identifier, 'extended': 0, 'access_token': token, 'v': 5.131}
    answer = requests.get('https://api.vk.com/method/users.getSubscriptions', payload).json()
    if 'error' in answer:
        print(answer['error'])
        items = []
    else:
        items = answer['response']['groups']['items']
    return items


print(list(set(groups(user_id1, token_list[n])) & set(groups(user_id2, token_list[n]))))
