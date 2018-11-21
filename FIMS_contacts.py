"""FIMS_Contacts
Export FIMS "Contact - Full Information" report to find contact records
and measure/count the number of characters in the "Pro-Comments" field
"""

import os

flag_comments = False
current_contact = ''
current_id = ''
current_comments = ''
current_date = ''

line_starters = [r'Contact #: ',
                 r'  ID Code:',
                 r'  Contact Date: ',
                 r' Comments:']

ref_file = os.path.abspath(r'data/FIMS_Contact_Full_Information.txt')

def check_line(line, starts_with):
    str_len = len(starts_with)
    return line[str_len:]

with open(ref_file, encoding='utf8') as f:
    for line in f:
        # Find lines beginning with "Contact #:"
        """
        for starter in line_starters:
            if line.startswith(starter):
                print(starter + ' : ' + check_line(line, starter))
        """
        if line.startswith(line_starters[0]):   # 'Contact #'
            if len(current_comments) > 25734:
                print('Contact ID ' + current_contact + ' | current id ' + current_id
                      + 'Current Date: ' + current_date + ' | Comments Len: ' + str(len(current_comments)))
            current_contact = check_line(line, line_starters[0])
            flag_comments = False
        elif line.startswith(line_starters[1]): # ID Code
            current_id = check_line(line, line_starters[1])
        elif line.startswith(line_starters[2]): # Date
            current_date = check_line(line, line_starters[2])
        elif line.startswith(line_starters[3]):  # Comments:
            flag_comments = True
            current_comments = check_line(line, line_starters[3])
        elif flag_comments == True:
            current_comments = current_comments + line
