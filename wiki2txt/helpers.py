
from termcolor import colored
from wiki2txt.constants import types_auth


def print_green(txt):
    print( colored(txt, 'green'))

def print_red(txt):
    print( colored(txt, 'red'))

def print_cyan(txt):
    print(colored(txt, 'cyan'))

def print_yellow(txt):
    print( colored(txt, 'yellow'))

def index_to_type(index):
    return types_auth[index]


def wget(index_type_auth, url):
    print_cyan(f'Creando wget con auth tipo : {index_to_type(index_type_auth)}')
    match index_type_auth:
        case 0:
            wget=f'wget --mirror      --convert-links      --adjust-extension      --page-requisites      --no-parent      "{url}"'
            print_cyan(wget)
            return wget
        case 1:
            user=input(colored('Introduzca el usuario: ', 'yellow'))
            passw=input(colored('Introduzca el password: ', 'yellow'))
            wget=f'wget  --user={user} --password={passw}  --mirror --convert-links      --adjust-extension      --page-requisites      --no-parent      "{url}"'
            print_cyan(wget)
            return wget

def clear_soup_text(soup):
        text=soup.get_text(separator='\n') ## añade demasiado \n
        clean_lines=[line.strip() for line in text.splitlines() if line.strip()!='']
        clean_text='\n'.join(clean_lines)
        return clean_text