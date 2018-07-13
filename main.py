import login
import class_data
import time
import os

turmas = [] #Lista de objetos de turmas processadas

try:
    files = os.listdir('progress_saved_list_id_class')
except FileNotFoundError:
    os.mkdir('progress_saved_list_id_class')
    files = os.listdir('progress_saved_list_id_class')

if 'class_id_list.json' in os.listdir('progress_saved_list_id_class'):
    print('!previous progress found!\nYou wish load the previus progress?["S"] or ["n"]')
    option = input().strip(' ')

    if option.lower() == 'n':
        session_id_aut = login.get_authenticated_id()

        #initial id and final id
        initial_class = int(input('class initial:').strip(' '))
        final_class = int(input('class final:').strip(' '))
        #list of all class ids
        class_id_list = class_data.generate_ids(initial_class, final_class)
    else:
        class_id_list = class_data.load_progress_class_list('class_id_list')
        turmas = class_data.load_progress_class_list('turmas_processadas')
        print('progress load sucsses')
        session_id_aut = login.get_authenticated_id()


#caso não encontre nehum progresso anterior
else:
    session_id_aut = login.get_authenticated_id()

    #initial id and final id
    initial_class = int(input('class initial:').strip(' '))
    final_class = int(input('class final:').strip(' '))
    #list of all class ids
    class_id_list = class_data.generate_ids(initial_class, final_class)

#loop process each class
while class_id_list:
    #save a json of the list progress of class ids
    class_data.save_progress_class_list(class_id_list, 'class_id_list')
    actual_id_class = class_id_list.pop(0)

    while True:
        turma_html = class_data.get_class(actual_id_class, session_id_aut)

        if '<div id="nomeTurma"' in turma_html:
            turmas.append(class_data.process_class_info(turma_html, actual_id_class))
            class_data.save_progress_class_list(turmas, 'turmas_processadas')
            break
        else:
            continue

os.system('rm progress_saved_list_id_class/class_id_list.json')
