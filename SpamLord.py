import sys
import os
import re
import pprint

my_first_pat = '(\w+)@(\w+).edu'

 
email_patterns = [
    '(?P<name>[A-Za-z0-9_.-]+)\s*@\s*(?P<domain>[A-Za-z_. -]+(edu|com|org|net|gov))',
    '(?P<name>[A-Za-z0-9_.-]+)\s*@\s*(?P<domain>[A-Za-z_. -]+\.br)\W',
     
    '(?P<name>[A-Za-z0-9_.-]+)\s*%40\s*(?P<domain>[A-Za-z_.-]+\.(edu|com|org|net|gov))',
    '(?P<name>[A-Za-z0-9_.-]+)\s*%40\s*(?P<domain>[A-Za-z_.-]+\.br)\W',

    '(?P<name>[A-Za-z0-9_.-]+)\s+\<*\(*[aA][tT]\>*\)*\s+(?P<domain>[A-Za-z_. ;<>()-]+ (edu|org|gov))',

    '(?P<name>[A-Za-z0-9_.-]+)\s+\<*\(*[aA][tT]\>*\)*\s+(?P<domain>[A-Za-z_. ;<>()-]+ com )',
     r'(?P<name>[A-Za-z0-9_.-]+)\s+\<*\(*[aA][tT]\>*\)*\s+(?P<domain>[A-Za-z_. ;<>()-]+ net )',
     r'(?P<name>[A-Za-z0-9_.-]+)\s+\<*\(*[aA][tT]\>*\)*\s+(?P<domain>[A-Za-z_. ;<>()-]+ br )', 

'(?P<name>[A-Za-z0-9_.-]+)[ <(_]+at symbol[>)_ ]+(?P<domain>[A-Za-z_. ;<>()-]+(?:edu))\W',
'(?P<name>[A-Za-z0-9_.-]+)[ <(_]+[aA][tT]*[>)_ ]+(?P<domain>[A-Za-z_. ;<>()-]+(?:edu))\W',

 '(?P<name>[A-Za-z0-9_.-]+)<[/span()]*>\s+[aA][tT]\s+<[A-Za-z0-9()= ]*>(?P<domain>[A-Za-z_. ;<>()-]+edu)',
 '(?P<name>[A-Za-z0-9_.-]+)\s+\[please add [aA][tT] sign here\]\s+(?P<domain>[\[\]A-Za-z_. ;<>()-]+edu)',


   '(?P<name>[A-Za-z0-9_.-]+)\s+[aA][tT]\s+(?P<domain>[A-Za-z_.-;]+\.(edu|com|org|net|gov))',
   '(?P<name>[A-Za-z0-9_.-]+)\s+[aA][tT]\s+(?P<domain>[A-Za-z_.-;]+\.br)\W',


   '(?P<name>[A-Za-z0-9_.-]+)\s*\[[aA][tT]\]\s*(?P<domain>[A-Za-z_.-;]+\.(edu|com|org|net|gov))',
   '(?P<name>[A-Za-z0-9_.-]+)\s*\[[aA][tT]\]\s*(?P<domain>[A-Za-z_.-;]+\.br)\W',



        '(?P<name>[A-Za-z0-9_.-]+)\s*\([aA][tT]\)\s*(?P<domain>[A-Za-z_.-;]+\.(edu|com|org|net|gov))',
        '(?P<name>[A-Za-z0-9_.-]+)\s*\([aA][tT]\)\s*(?P<domain>[A-Za-z_.-;]+\.br)\W',

     '(?P<name>[A-Za-z0-9_.-]+)\s+[\[\]A-Za-z ]+\s+[aA][tT]\s+[\[\]A-Za-z ]+\s+(?P<domain>cse[\[\]A-Za-z_.; <>()-]+edu)',
'(?P<name>[A-Za-z0-9_.-]+)\s+[\[\]A-Za-z ]+\s+[aA][tT]\s+[\[\]A-Za-z ]+\s+(?P<domain>tamu[\[\]A-Za-z_.; <>()-]+edu)',

     r'write_mail\(\"(?P<domain>[A-Za-z_.-]+)\",\"(?P<name>[A-Za-z0-9_.-]+)\"\)',
      r'mail_link\(\"(?P<name>[A-Za-z_.-]+)\",[ ]*\"(?P<domain>[A-Za-z0-9_.-]+)\"',
      r'obfuscate\(\'(?P<domain>[A-Za-z_.-]+)\',[ ]*\'(?P<name>[A-Za-z0-9_.-]+)\'\)']


number_patterns=['\D+[+1\.]*[(]*([\d]{3})[)-/. ]+([\d]{3})[-/. ]+([\d]{4})\D+']

special_patterns=['[A-Z0-9]+[ <(_]+(dot)+[ <(_]+[A-Z0-9]+[ <(_]*dot[ <(_]*[A-Z0-9]+[ <(_]+[aA][tT]*[>)_ ]+[A-Z0-9]*[ <(_]*(dot)*[ <(_]*[A-Z0-9]+[ <(_]*dot[ <(_]*(edu|com)',
'[A-Z0-9]+[ <(_]*dot[ <(_]*[A-Z0-9]+[ <(_]+[aA][tT]*[>)_ ]+[A-Z0-9]*[ <(_]*(dot)*[ <(_]*[A-Z0-9]+[ <(_]*dot[ <(_]*(edu|com)']

""" 
TODO
This function takes in a filename along with the file object (actually
a StringIO object) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    flag_tel=0
    line_queue=[]
    for line in f:
        line_queue.append(line.strip())
        if len(line_queue)==1:
            continue
        if len(line_queue)>2:
            line_queue.pop(0)
        
        lines= " "+" ".join(line_queue)+" "
        flag_mail=1
        flag_special=1
        for pattern in special_patterns:
            if flag_special==1:
                for match in re.finditer(pattern, lines, flags=re.IGNORECASE):
                    special_email=match.group()
                    special_email=re.sub('[ <>\[\]\(\)_]*dot[ <>\[\]\(\)_]*', '.', special_email, flags=re.IGNORECASE)
                    special_email=re.sub('[ <>\[\]\(\)_]+at[ <>\[\]\(\)_]+', '@', special_email, flags=re.IGNORECASE)
                    res.append((name, 'e',special_email.strip()))
                    flag_special=0
        for pattern in email_patterns:
            if flag_mail==1 and flag_special==1:
                for match in re.finditer(pattern, lines, flags=re.IGNORECASE):
                    if not re.match("(?:blog|website)",match.group('name'), flags=re.IGNORECASE):
                        email_name=match.group('name')
                        email_name=re.sub('[ <>\[\]\(\)_]*dot[ <>\[\]\(\)]*', '.', email_name, flags=re.IGNORECASE)
                        email_name=re.sub('\s+', '', email_name, flags=re.IGNORECASE)
                        email_domain=match.group('domain')
                        email_domain=re.sub('[ <>\[\]\(\)_]*dot[ <>\[\]\(\)_]*', '.', email_domain, flags=re.IGNORECASE)
                        email_domain=re.sub('\s+', '', email_domain, flags=re.IGNORECASE)
                        email_domain=re.sub(';', '.', email_domain, flags=re.IGNORECASE)
                        res.append((name, 'e',(email_name +'@'+email_domain).strip()))
                        flag_mail=0
        for pattern in number_patterns:
                if re.search(r'ph|p:|tel|office|voice', lines, flags=re.IGNORECASE):
                    flag_tel=1
                if re.search(r'FAX', lines, flags=re.IGNORECASE):
                    lines=lines[: re.search(r'FAX', lines, flags=re.IGNORECASE).end()]
                    for match in re.finditer(pattern, lines,flags=re.IGNORECASE):
                        res.append((name, 'p',  match.group(1)+'-'+match.group(2)+'-'+ match.group(3)))
                    flag_tel=0
                if flag_tel==1:
                    for match in re.finditer(pattern, lines, flags=re.IGNORECASE):
                        res.append((name, 'p',  match.group(1)+'-'+match.group(2)+'-'+ match.group(3)))
    return res

"""
You should not need to edit this function, nor should you alter
its interface
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r', encoding = "ISO-8859-1")
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print('Guesses (%d): ' % len(guess_set))
    #pp.pprint(guess_set)
    #print('Gold (%d): ' % len(gold_set))
    #pp.pprint(gold_set)
    print('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print('usage:\tSpamLord.py <data_dir> <gold_file>')
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])
