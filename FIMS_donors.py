"""FIMS_donors
Export FIMS "Donors - Full Information" report to find donor records and
calculate the length of the "Donor-Comment" field
"""

import os
import pandas as pd
import re
import openpyxl

flag_comments = False
current_id = ''
current_comments = ''
result_list = list()

id_code = r'ID Code:  '
comments = r'| Comments: '
end_comments = r'|------'

ref_file = os.path.abspath(r'data/donors.txt')

def check_line(line, starts_with):
    str_len = len(starts_with)
    return line[str_len:]

with open(ref_file, encoding='ISO-8859-1') as f:
    for line in f:

        # Remove special characters
        line = re.sub('\f', '', line)

        # Find lines beginning with "ID Code:"
        if id_code in line: #line.startswith(line_starters[0]):   # 'ID Code:'
            if len(current_comments) > 1000:
                result_list.append((current_id, len(current_comments), current_comments))
                # print('current id ' + current_id
                #       + ' | Comments Len: ' + str(len(current_comments)))
            current_id = line[10:17].rstrip()
            # Clear existing comment
            current_comments = ''
            flag_comments = False
        elif comments in line: #line.startswith(line_starters[1]): # Comments, beginning
            flag_comments = True
            # current_comments = check_line(line, line_starters[1])
        elif end_comments in line: #line.startswith(line_starters[2]): # End of Comments, "|----"
            flag_comments = False
        elif flag_comments == True:
            current_comments = current_comments + line

        # print(line)

df_results = pd.DataFrame(result_list, columns=['DonorID', 'CommentLen', 'Comments'])
# print(df_results.head())
df_results.sort_values('CommentLen', ascending = False, inplace = True)
print(df_results.head(50))
