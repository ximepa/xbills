__author__ = 'ximepa'
import requests
#from django.conf import settings


def main(search=None):
    response_auth = requests.post('http://oll.tv/ispAPI/auth2/', data={
        'login': 'mtel',
        'password': 'x_g~-5~(;ZY'
    })
    response_content = response_auth.json()
    #print response_auth.json()
    response_get_user_list = requests.post('http://oll.tv/ispAPI/getUserList/', data={
        #'account': '6200',
	'offset': '',
        'hash': response_content['hash']
    })
    get_user_list_json = response_get_user_list.json()
    print get_user_list_json
    get_user_list = get_user_list_json['data']
    num = 0
    for i in get_user_list:
        print str(num) + '. ' + i['account'] + ' ' + i['firstname'] + ' ' + i['lastname']
        num = num + 1

if __name__ == "__main__":
    main()
