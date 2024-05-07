import sys
import os


if len(sys.argv) == 1:
    print("option not selected")
    sys.exit()


def process_name(name, options):
    new_name = name
    for oper in options:
        if oper.startswith('-r='):
            old, new = oper[3:].split('->')
            new_name = new_name.replace(old, new, 1)
            
        if oper.startswith('-sub='):
            start, finish = oper[5:].split(':')
            if len(finish) == 0:
                new_name = new_name[int(start):]
            else:
                new_name = new_name[int(start):int(finish)]
                
        if oper.startswith('-z='):
            length = int(oper[3:])
            name = new_name
            while len(name) < length:
                name = '0' + name
            new_name = name
            
        if oper.startswith('-suff='):
            suffix = oper[6:]
            new_name = new_name + suffix
            
        if oper.startswith('--try-only'):
            try_only = True

    print(f'processed: "{name}" -> "{new_name}"')
    return new_name


def process_file(dir_name, file_name, options):
    new_name = process_name(file_name, options)
    try_only = False
    if '--try-only' in options:
        try_only = True

    if try_only == False:
        if file_name != new_name:
            print(f'renaming: "{file_name}" -> "{new_name}"')
            os.rename(os.path.join(dir_name, file_name), os.path.join(dir_name, new_name))
    
    
    
def process_dir(dir_name, options):
    print('processing dir "' + dir_name + '"')
    for name in os.listdir(dir_name):
        if os.path.isdir(os.path.join(dir_name, name)):
            process_file(dir_name, name, options)
            
            
            
def process_all(dir_name):
    options = sys.argv[1:]
    # recursive?
    if '-R' in options:
        print('starting recursive processing')
        process_dir(dir_name, options)
        for subdir_name in os.listdir(dir_name):
            process_all(os.path.join(dir_name, subdir_name))
    else:
        process_dir(dir_name, options)
        
        
if __name__ == '__main__':
    process_all('.')
        