# jsonify_departments.py

# Description: Given a text file of department names, the script writes a json
# representation of the data to departments.json
# Author: Ian Zapolsky (10/17/13)

import sys

def jsonify(filename):
    unformatted = open(filename, 'r');
    formatted = open('departments.json', 'w')
    pk_count = 1;

    # setup
    formatted.write('[\n')

    for line in unformatted:

        formatted.write('\t{\n')
        formatted.write('\t\t"model": "course.departmentmodel",\n')

        concat = '\t\t"pk": '+str(pk_count)+',\n'
        formatted.write(concat)
        formatted.write('\t\t"fields": {\n')
        pk_count += 1
        
        # NOTE: str.rstrip() chops off the trailing '\n' character in line

        concat = '\t\t\t"name": "'+line.rstrip()+'",\n'
        formatted.write(concat)

        concat = '\t\t\t"slug": "'+slugify(line.rstrip())+'"\n'
        formatted.write(concat)
        formatted.write('\t\t}\n')
        formatted.write('\t},\n')

    # final bracket
    formatted.write(']\n')


def slugify(string):
    result = ''
    for c in string:
        if ord(c) >= ord('A') and ord(c) <= ord('Z'):
            result += chr(ord(c)+32)
        elif ord(c) == ord(' '):
            result += chr(ord('-'))
        elif ord(c) == ord('\'') or ord(c) == ord(','):
            pass
        elif ord(c) == ord('+'):
            result += 'and'
        else:
            result += c
    return result

jsonify("departments.txt")




