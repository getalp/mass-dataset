import sys, glob, codecs


# (english, french, spanish,_)
NAMES = [('Matthew', 'Matthieu', 'San_Mateo', 'S_Mateus'), ('Mark', 'Marc', 'San_Marcos', 'S_Marcos'),
         ('Luke', 'Luc', 'San_Lucas', 'S_Lucas'), ('John', 'Jean', 'San_Juan', 'S_Joao'),
         ('Acts', 'Actes', 'Hechos', 'Atos'), ('Romans', 'Romains', 'Romanos'),
         ('Corinthians', 'Corinthiens', 'Corintios'), ('Galatians', 'Galates', 'Galatas'),
         ('Ephesians', 'Ephesiens', 'Efesios'), ('Philippians', 'Philippiens', 'Filipenses'),
         ('Colossians', 'Colossiens', 'Colosenses', 'Colossenses'), ('Thess', 'Thess', 'Tes', 'Tess'),
         ('Timothy', 'Timothee', 'Timoteo'), ('Titus', 'Tite', 'Tito'), ('Philemon', 'Philemon', 'Filemon'),
         ('Hebrews', 'Hebreux', 'Hebreos', 'Hebreus'), ('James', 'Jacques', 'Santiago', 'S_Tiago'),
         ('Peter', 'Pierre', 'San_Pedro', 'Pedro'), ('Jude', 'Jean', 'Judas', 'S_Judas'), ('Jude', 'Jude', 'Judas', 'S_Judas'),
         ('Revelation', 'Apocalypse', 'Apocalipsis', 'Apocalipse')]

KEYS = {"es": "SPNBDAN1DA","hu":"HUNHBSN1DA","ru":"RUSS76N2DA","ro": "RONDCVN1DA", "en": "ENGESVN1DA", "eu": "EUSEABN1DA", "fi": "FIN38VN1DA", "fr": "FRNTLSN2DA"}


# input example: B05___07_Hechos______SPNBDAN1DA_verse_46.txt

def get_key(string, language):
    key = string.split("/")[-1].split("___")[1].split("______")[0].split("__")[0]
    key = key.split("_"+KEYS[language])#[0] 
    if len(key) == 1:
        key = key[0].split(KEYS[language])
    key = key[0]
    key = key.split("_")[1:]
    return "_".join(key)

def fix_name(path, language):
    key = get_key(path, language)
    index = 2 if language != "fr" else 1
    for chapter_names in NAMES:
        if chapter_names[index] == key:
            return path.replace(key, chapter_names[0])
        elif chapter_names[index] == key[1:]: # number before name
            return path.replace(key[1:], chapter_names[0])
    print(path, key)
    raise Exception("Correspondence not found")

def clean_path(string, language):
    string = string.replace(KEYS[language],"")
    while "__" in string:
        string = string.replace("__","_")
    string = string.replace(".txt", "."+language)
    string = "_".join(string.split("_")[1:]) #remove the B at the beginning, which is not a shared id
    return string.split("/")[-1]

def write_content(source, target):
    content = [line for line in codecs.open(source, "r", "utf-8")]
    with codecs.open(target,"w","utf-8") as output_file:
        for line in content:
            output_file.write(line)

def write_id(f_name, name):
    with open(f_name,"a") as id_file:
        id_file.write(name.split(".")[0] + "\n")

def generate():
    raw_folder = glob.glob(sys.argv[1] + "/*")
    target_folder = sys.argv[2]
    language_key = sys.argv[3]
    for path in raw_folder:
        if language_key in ["es","eu","fr"]:
            new_name = fix_name(path, language_key)
        else:
            new_name = path
        new_name = clean_path(new_name, language_key) #.split("/")[-1]
        write_content(path, "/".join([target_folder, new_name]))
        write_id(language_key + ".ids", new_name)



if __name__ == "__main__":
    generate()
