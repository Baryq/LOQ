import requests
import time
from FrequentFunctions import read, write_json, write_txt

start_time = time.time()

do_you_want_to_continue_dictionary_or_start_a_new_one = False  # continue - True; new one - False

token_list = ['9ad97d27909034b7b5d65167b35f3617867732f85b0f3c6f38527138a999bed72c287e7752322c48fda1b',  # мамин
              '5001a5c9cf09c80ac916fac79239c40ed6bb55336f93f6fd13cf1b0234888ec000575445c6ffe2a56e003',  # мой
              '71ce357930df58936799d99ee53e8b4b16d5a1ff3e970bde6f3dee95bede9639078356ebab2f630be2b55',  # мой 2
              ]

fields1 = 'bdate,career,city,contacts,country,education,military,occupation,personal,relation,schools,sex,universities'
fields2 = ['first_name', 'id', 'last_name', 'can_access_closed', 'is_closed', 'sex', 'bdate', 'city', 'country',
           'mobile_phone', 'home_phone', 'career', 'military', 'university', 'university_name', 'faculty',
           'faculty_name', 'graduation', 'relation', 'personal', 'universities', 'schools', 'occupation']
vk_id = 305617399
depth = 200
users_lim = 25
friends_lim = 100
city = 'Самара'


def users(identifier, token):
    identifier = str(identifier)[1:-1]
    payload = {'user_ids': identifier, 'fields': fields1, 'access_token': token, 'v': 5.131}
    answer = requests.get('https://api.vk.com/method/users.get', payload).json()
    time.sleep(sleep_info)
    if 'error' in answer:
        if answer['error']['error_code'] not in [18, 30, 5]:
            global flag
            flag = False
        print(answer['error'])
        items = []
    else:
        items = answer['response']
        for a in items:
            a['link'] = 'https://vk.com/id' + str(a['id'])
    return items


def friends(identifiers, token):
    f = 0
    payload = {}
    for identifier in identifiers:
        f += 1
        payload['user' + str(f)] = identifier
    payload = {**payload, **{'access_token': token, 'v': 5.131}}
    answer = requests.get('https://api.vk.com/method/execute.friends', payload).json()
    time.sleep(sleep_friends)
    if 'execute_errors' in answer:
        if answer['execute_errors'][-1]['error_code'] not in [18, 30, 5]:
            global flag
            flag = False
        print(answer['execute_errors'])
    items = answer['response']
    return items


if do_you_want_to_continue_dictionary_or_start_a_new_one is True:
    dct = read('dctFolder/dct.txt')
    q_friends_list = read('dctFolder/q_friends_list.txt')
    q_friends_set = read('dctFolder/q_friends_set.txt')
    q_info_list = read('dctFolder/q_info_list.txt')
    del_friends_set = read('dctFolder/del_friends_set.txt')
    all_friends_set = read('dctFolder/all_friends_set.txt')
    all_info_set = read('dctFolder/all_info_set.txt')
else:
    dct = {}
    q_friends_list = [vk_id]
    q_friends_set = {vk_id, }
    q_info_list = []
    del_friends_set = {vk_id, }
    all_friends_set = set()
    all_info_set = set()

sleep_friends = 0.1
sleep_info = 0.1
flag = True

while True:

    for temp_token in token_list:

        flag = True

        while len(dct) <= depth:

            if not q_friends_list:
                print('queue is empty. wait for limits to update')
                break

            if len(q_friends_set) <= friends_lim:
                friends_lists_list = friends(q_friends_list, temp_token)
            else:
                friends_lists_list = friends(q_friends_list[:friends_lim], temp_token)

            for friends_list in friends_lists_list:
                if friends_list is None:
                    friends_list = []
                dct[str(q_friends_list[0])] = {'friends': friends_list}
                all_friends_set.add(q_friends_list[0])
                q_info_list.append(q_friends_list[0])
                del_friends_set.add(q_friends_list[0])
                del q_friends_list[0]
                for friend in friends_list:
                    if (friend not in q_friends_set) & (friend not in del_friends_set):
                        q_friends_list.append(friend)
                        q_friends_set.add(friend)

            if (len(q_info_list) >= users_lim) | (len(dct) > depth) | (flag is False):
                cropped_list = q_info_list[:users_lim]
                info_lists_list = users(cropped_list, temp_token)

                for i in range(len(info_lists_list)):

                    user = info_lists_list[i]['id']
                    if 'city' in info_lists_list[i]:
                        if info_lists_list[i]['city']['title'] == city:
                            for field in fields2:
                                dct[str(user)][field] = ''
                            dct[str(user)] = {**dct[str(user)], **info_lists_list[i]}
                            all_info_set.add(user)
                        else:
                            del dct[str(user)]
                            all_friends_set.remove(user)
                    else:
                        del dct[str(user)]
                        all_friends_set.remove(user)

                    q_info_list.remove(user)

                for user in list(all_friends_set.difference(all_info_set).difference(set(q_info_list))):
                    del dct[str(user)]
                    # all_friends_set.remove(user)

                all_friends_set = {friend for friend in all_friends_set if friend not in
                                   list(all_friends_set.difference(all_info_set).difference(set(q_info_list)))}

            if flag is False:
                break

        print('writing...')

        write_json('graphFolder/dct.json', dct)
        write_txt('dctFolder/dct.txt', dct)
        write_txt('dctFolder/q_friends_list.txt', q_friends_list)
        write_txt('dctFolder/q_friends_set.txt', q_friends_set)
        write_txt('dctFolder/q_info_list.txt', q_info_list)
        write_txt('dctFolder/del_friends_set.txt', del_friends_set)
        write_txt('dctFolder/all_friends_set.txt', all_friends_set)
        write_txt('dctFolder/all_info_set.txt', all_info_set)

        if flag is True:
            break

    if flag is True:
        break

    print('waiting...')
    time.sleep(86400)

print('\n', len(dct))
print('\ntime = ', time.time() - start_time)
