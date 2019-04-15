import sys, codecs, glob


def clean_punct(line):
    punctuation_swap =  [   ('“', '"'),
                            ('”', '"'),
                            ('’', ' '),
                            ('“', '"'),
                            ('‘', ' ')               
                        ]
    for pct_b, pct_a in punctuation_swap:
        line=line.replace(pct_b, pct_a)
    return line

def clean(line):
    while "  " in line: #remove double space
        line = line.replace("  "," ")
    line = line.replace("\t","") #remove tab
    line = clean_punct(line)
    line = line.lower()

    if line and line[0] == " ":
        line = line[1:]
    if line and line[-1] == " ":
        line = line[:-1]
    try:
        line = int(line) #verse
        return "" 
    except ValueError: #real text
        return line
    
    


def cleaner():
    input_files = glob.glob(sys.argv[1] + "/*." + sys.argv[3])
    output_folder = sys.argv[2] + "/" if sys.argv[2][-1] != "/" else sys.argv[2]

    for input_file in input_files:
        text = [line.strip() for line in codecs.open(input_file,'r','utf-8')][0] #the raw files have all the verses on a single line
        with codecs.open(output_folder + input_file.split("/")[-1], 'w', 'utf-8') as output:
            for possible_line in text.split("    "): #4 spaces
            #for possible_line in text:
               line = clean(possible_line)
               if line:
                  output.write(line  + " ")
            output.write("\n")





if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("USAGE: python3 clean_raw_txt.py <input_folder> <output_folder> <suffix>")
        sys.exit(1)
    cleaner()
