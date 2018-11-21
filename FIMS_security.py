# Imports file from FIMS: Tools -> System Utilities -> Admin Utilities -> User Permissions Report.
#       Parses file, writes results to a normalized, tab-delimited *.CSV file.
# Note: Import file structure: First 61 characters are the "Activity" column, remaining
# characters contain comma-separated list of user IDs.

# See spreadsheet at:
# C:\Users\Mitchell.Hollberg\OneDrive - Community Foundation for Greater Atlanta\MH\FIMS\ADMIN\CFGA - FIMS Procedures\fims-security-module-listing.xlsx


import os
import re
from collections import OrderedDict

re_endline = re.compile('[,]$')     # Match comma at end of line
file_in = os.path.abspath(r'FIMS_User_Permissions_report.txt')
file_out = 'FIMS_Security_20170906.csv'
mydict = OrderedDict()
mystr = ''

# Read FIMS Security report: Skip irrelevant lines, build dict of "Activity:[UsersIds]"
with open(file_in) as f:
    for line in f:
        """ Skip 'filler' lines, aka...
            Activity                                                     AccessList
            ------------------------------------------------------------ ---------------------
             Newline ('\n') or page break/form feed ('\f\n')
        """
        if line == '\n' or line[:8] == 'Activity' or line[:3] == '---' or line == '\f\n':
            continue

        # Replace LEADING comma (replace don't remove to ensure 1st 61 characters == Activity column)
        if line[0] == ',':
            line = ' ' + line[1:]

        # Wrapped lines in input file ENDS with a comma (,). Save current string, append following
        if re.search(re_endline, line):
            mystr = mystr + line.rstrip()
            continue

        mystr += line.rstrip()
        activity = mystr[:61].strip()
        mydict[activity] = mystr[61:].split(',')
        mystr = ''

# Loop over clean dict: write 1 Row per "Activity/UserId" combination
with open(file_out, 'w') as f_out:
    f_out.write('Activity \t User \n')  #Write file header row, tab Delimited
    for key, values in mydict.items():
        for entry in values:
            f_out.write(''.join(key) + '\t' + entry.strip() + '\n')
