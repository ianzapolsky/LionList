# jsonify_courses.py

# Description: Given a directory of text files, where each text file contains a
# list of the courses within a certain department, the script writes a json
# representation of the data to courses.json
# Author: Ian Zapolsky (10/17/13)

import os
import sys

class JSonifier:
   
    def __init__(self):
        self.pk_count = 1

    def jsonify_all(self):
        courses = open('../courses.json', 'w')

        # setup
        courses.write('[\n')
        pk_count = 1

        for filename in os.listdir('.'):
            if filename[-3:] == 'txt':
                courses.write(self.jsonify(filename))

        # cleanup
        courses.write(']\n')


    def jsonify(self, filename):
        print 'jsonifying '+filename+'...'

        unformatted = open(filename, 'r')
        result = ''
        pk_string = unformatted.readline().rstrip()
        pk = int(pk_string)

        for line in unformatted:
        
            if (len(line) <= 2):
                pass
            else:
                result += '\t{\n'
                result += '\t\t"model": "course.coursemodel",\n'
                result += '\t\t"pk": '+str(self.pk_count)+',\n'
                self.pk_count += 1
                result += '\t\t"fields": {\n'
                result += '\t\t\t"name": "'+line.rstrip()+'",\n'
                result += '\t\t\t"slug": "'+self.slugify(line.rstrip())+'",\n'
                result += '\t\t\t"department": "'+str(pk)+'"\n'
                result +=('\t\t}\n')
                result +=('\t},\n')
    
        return result


    def slugify(self, string):
        result = ''
        for c in string:
            if ord(c) >= ord('A') and ord(c) <= ord('Z'):
                result += chr(ord(c)+32)
            elif ord(c) == ord(' ') or ord(c) == ord('/'):
                result += chr(ord('-'))
            elif ord(c) == ord('+'):
                result += 'and'
            elif ord(c) == ord(',') or ord(c) == ord(':'):
                pass
            elif ord(c) == ord('\''):
                pass
            else:
                result += c
        return result


jsonifier = JSonifier()
jsonifier.jsonify_all()




