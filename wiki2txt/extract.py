from wiki2txt.helpers import print_green, print_cyan,print_red, print_yellow, index_to_type,wget,clear_soup_text
from wiki2txt.constants import output_dir,types_auth
from bs4 import BeautifulSoup
from termcolor import colored
from tqdm import tqdm
import subprocess
import os
import sys
from datetime import datetime

def extract():

    index_type_auth=None

    print_green('Bienvenido a wiki2txt.\n ')

    while index_type_auth == None:

        print_green(f'Tipos de AUTENTICACION de la wiki (1-{len(types_auth)}):')
        for index,type in enumerate(types_auth): 
            print_yellow(f'{index+1}.{type}')

        try:    
            index_type_auth=int(input(colored('Seleccione uno:  ', 'green')))
        except ValueError:
            print_red('Tiene que seleccionar el número correspondiente.\n\n')
            index_type_auth=None
            continue
        
    
        if index_type_auth>len(types_auth) or index_type_auth==0:
            print_red('No ha seleccionado ningún tipo.\n\n')
            index_type_auth=None
            continue

        index_type_auth-=1 #para que corresponda con el index de la array

    print_yellow(f'La auth seleccionada es: {index_to_type(index_type_auth)}')    

    url=None

    while url ==None:
        
        url=input(colored('Indique la URL de la wiki:  ', 'green'))
        if len(url)==0:
            url=None
            print_red('No puede estar vacío.\n\n')

    name_dir_output=None
    while name_dir_output ==None:
        
        name_dir_output=input(colored('Indique nombre que quiere que tenga la carpeta de salida ', 'green'))
        if len(name_dir_output)==0:
            name_dir_output=None
            print_red('No puede estar vacío.\n\n') 


    print_yellow(f' NOMBRE CARPTA SALIDA: {name_dir_output}')
    print_yellow(f'URL: {url}')



    wget_command=wget(index_type_auth, url)

    dir_results=f'{output_dir}/{datetime.now().strftime('%Y%m%d%H%M%S')} {name_dir_output}'
    dir_results_wget=f'{dir_results}/wget'

    os.makedirs(dir_results_wget, exist_ok=True)
    # os.chdir(dir_results_wget)
    try:
        subprocess.call(wget_command, shell=True,cwd=dir_results_wget)
    except subprocess.CalledProcessError:
        print_red('Ha ocurrido un error con el wget.')
        sys.exit(1)
    with open(f'{dir_results}/final_text.txt', 'a') as f_final:
        # Recorrer recursivo
        for root, dirs, files in tqdm(os.walk(dir_results_wget), desc='Processing to txt'):
            for file in files:
                if file.endswith(".html"):
                    html=None
                    with open(f'{root}/{file}', "r", encoding='UTF-8') as f:
                        html=f.read()
                    
                    soup=BeautifulSoup(html, 'html.parser')
                    soup_header=soup.select_one('#firstHeading')
                    soup_content=soup.select_one('#mw-content-text')
                   
                 
                    f_final.write(f'\n<===================={file}======================>\n')
                    f_final.write(clear_soup_text(soup_header)) if soup_header else print_red('No ha encontrado header en', file)
                    f_final.write(clear_soup_text(soup_content)) if soup_content else print_red('No ha encontrado contente en', file)
                    f_final.write(f'\n<===================={file}//END=================>\n')
                    
                    path_without_root= "/".join(root.split("/")[6:])
                    path_tree_txt=f'{dir_results}/text_tree/{path_without_root}'  
                    os.makedirs(path_tree_txt, exist_ok=True)
                    with open(f'{path_tree_txt}/{file}.txt', 'a') as f:
                        if soup_header:
                            f.write(clear_soup_text(soup_header))
                        if soup_content:    
                            f.write(clear_soup_text(soup_content))

    print_cyan('La salida se ha generado en : \n '+ dir_results)

                



    



        
