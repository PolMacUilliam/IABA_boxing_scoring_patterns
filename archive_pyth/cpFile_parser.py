import glob
from pprint import pprint

dirlist = glob.glob('data/*.cp')
#pprint(dirlist)

token = '['
num_cp_files = len(dirlist)
event_data = []
for current_cp_file_no in range(0,num_cp_files):

    bout_data = []
    cp_file_sections = []

    with open(dirlist[current_cp_file_no], "rt") as cp_file_input:
        # contents = cp_file_input.read()
        for line in cp_file_input.readlines():

            if line.startswith(token):

                if len(bout_data) > 0:
                    cp_file_sections.append(bout_data)
                bout_data = [line[len(token):]]

            else:
                bout_data.append(line)

        if len(bout_data) > 0:
            cp_file_sections.append(bout_data)

    print ("current bout data:  ",cp_file_sections)
    event_data.append(cp_file_sections)

# close the input CP file
cp_file_input.close()
print("\n\n\nall event data in one list:\n",event_data)
print("\nnumber of files read:\n",num_cp_files)

'''
print("\nnumber of files read:\n",num_cp_files)
print ("\nlast cp file read:\n",cp_file_sections)
print ("\nlast cp file read - extracted from event_data:\n",event_data[31])
'''




'''
#*************************************************************************
# I might use a dictionary here for holding file info at a later date
    bout_data = {
        'headline':4,
        'competition':5,
        'teamInfo':7,
        'sessions':8,
        'bouts':9,
        'officials':11,
        'combPoints':13,
        'detailScores':14,
        'legend':18}
#*************************************************************************

headline = file_sections[4]
print(headline)

competition = file_sections[5]
print(competition)

teamInfo = file_sections[7]
print(teamInfo)

sessions = file_sections[8]
print(sessions)

bouts = file_sections[9]
print(bouts)

officials = file_sections[11]
print(officials)

combPoints = file_sections[13]
print(combPoints)

detailScores = file_sections[14]
print(detailScores)

legend = file_sections[18]
print(legend)
'''
