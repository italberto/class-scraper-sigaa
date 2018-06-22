import requests
import getpass


def get_new_cookie():
    url = 'https://sigaa.ufpi.br/sigaa/verTelaLogin.do'

    while True:
        try:
            r = requests.get(url, timeout=5)
            print('Cookie gerado;')
        except:
            continue
        else:
            break

    cookie_i = r.headers['Set-Cookie'].find('JSESSIONID=') + 11
    cookie_f = r.headers['Set-Cookie'].find('; Path=/; Secure')

    return r.headers['Set-Cookie'][cookie_i:cookie_f]


def get_authenticated_id():

    session_id = get_new_cookie()

    url = 'http://sigaa.ufpi.br/sigaa/logar.do?dispatch=logOn'

    while True:
        username = input('username: ').strip(' ')
        password = input('password: ').strip(' ')

        payload = {
            'user.login' : username,
            'user.senha' : password,
            }
        cookies = {
            'JSESSIONID' : session_id
            }

        while True:
            try:
                r = requests.post(url, data=payload, cookies=cookies, timeout=5)
            except:
                continue
            else:
                break

        if ("rio e/ou senha inv" not in r.text) and 'username: "' in r.text:
            return session_id
        else:
            continue
