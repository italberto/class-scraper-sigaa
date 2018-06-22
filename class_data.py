import json, requests
import html
def generate_ids(initial, final):
    return [ x for x in range(initial, final+1)]

def save_progress_class_list(list_class_id, name_file):
    with open('progress_saved_list_id_class/'+name_file+'.json', 'w') as write_file:
        json.dump(list_class_id, write_file)

def load_progress_class_list(nome_file):
    with open('progress_saved_list_id_class/' + nome_file + '.json', 'r') as write_file:
        return json.load(write_file)

def get_class(id, cookie):
    url = 'https://sigaa.ufpi.br/sigaa/ufpi/portais/discente/discente.jsf'

    payload = {
        'form_acessarTurmaVirtual' : 'form_acessarTurmaVirtual',
        'idTurma' : id,
        'form_acessarTurmaVirtual:turmaVirtual' : 'form_acessarTurmaVirtual:turmaVirtual',
        'javax.faces.ViewState': 'j_id1',
        }
    cookies = {
        'JSESSIONID' : cookie,
        }

    while True:
        try:
            print('Requesting class id : ' + str(id) + ';')
            r = requests.post(url, data=payload, cookies=cookies, timeout=5)
        except requests.exceptions.ReadTimeout:
            print('Requesting class id : ' + str(id) + '[Error, requesting again;]')
            continue
        else:
            return r.text

def process_class_info(html_class, id):

    turma = {}
    turma['id'] = str(id)

    html_info = html_class.split('id="nomeTurma"')[1]
    html_info = html_info.split('</div>')[0]

    html_list = html_info.split('<p id=')[1:]

    #codigo da turma
    turma_i = html_list[0].find('">')+2
    turma_f = html_list[0].find('</p>')
    turma['codigo'] = html.unescape(html_list[0][turma_i:turma_f])

    #nome da turma
    turma_i = html_list[1].find('">')+2
    turma_f = html_list[1].find('</p>')
    turma['nome'] = html.unescape(html_list[1][turma_i:turma_f])

    #periodo da turma
    turma_i = html_list[2].find('">')+2
    turma_f = html_list[2].find('</p>')
    turma['periodo'] = html.unescape(html_list[2][turma_i:turma_f])

    #polo da turma
    turma_i = html_list[3].find('">')+2
    turma_f = html_list[3].find('</p>')
    turma['polo'] = html.unescape(html_list[3][turma_i:turma_f])

    print('\t' + turma['codigo'] + turma['nome'] + turma['periodo'] + turma['polo'])

    return turma
