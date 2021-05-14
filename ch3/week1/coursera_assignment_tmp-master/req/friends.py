import requests
import json
import datetime

def req_id(name):
    token = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
    payload = {'v':'5.71','access_token':token, 'user_ids':name}
    r = requests.get('https://api.vk.com/method/users.get', params=payload)
    uid = json.loads(r.text)['response'][0]['id']
    return uid

def req_friends(uid):
    token = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
    payload = {'v':'5.71','access_token':token, 'user_id':uid, 'fields': 'bdate'}
    r = requests.get('https://api.vk.com/method/friends.get', params=payload)
    friends = json.loads(r.text)['response']['items'] # list of friends(dict)
    return friends

def calc_age(uid):
    friends = req_friends(req_id(uid))
    res = [()]
    out = {}
    now = datetime.datetime.now()
    year = now.year
    for friend in friends:
        bd = friend.get('bdate')
        if bd is not None:
            try:
                bd_date = datetime.datetime.strptime(bd, "%d.%m.%Y")
                old = year - bd_date.year
                out[old] = out.get(old, 0) + 1
            except ValueError:
                pass
            
    for k, v in out.items():
        res.append((k,v))

    res.remove(())
    res.sort()
    res.sort(key=lambda x:x[1],reverse=True)

    return res



if __name__ == '__main__':
    res = calc_age("verminoid")
    print(res)
