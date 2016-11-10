__author__ = 'ximepa'
import requests
#from django.conf import settings


def main():
    response_auth = requests.post('http://oll.tv/ispAPI/auth2/', data={
        'login': 'mtel',
        'password': ''
    })
    search = raw_input('Enter uid or push enter: ')
    search1 = raw_input('Enter uid or push enter: ')
    response_content = response_auth.json()
    response_get_user_list = requests.post('http://oll.tv/ispAPI/deviceExists/', data={
	'mac': search,
        'serial_number': search1,
        'hash': response_content['hash']
    })
    print response_get_user_list
    print response_get_user_list.json()
    get_user_list_json = response_get_user_list.json()
    get_user_list = get_user_list_json['data']
    print get_user_list
    num = 0
    for i in get_user_list:
        print str(num) + '. ' + i['serial_number']
        num = num + 1

if __name__ == "__main__":
    main()
