import glob
import os.path, time
import datetime
import csv
import tkinter
from tkinter import filedialog

now = datetime.datetime.now()

print("Open my csv log here...")
#C:\Users\Cenit\Documents\PW\9_Projects\Major_project\Data\proc_data.log.txt
with open('C:/Users/Cenit/Documents/PW/9_Projects/Major_project/Data/proc_data.log', 'r') as mylog:
    list_of_lines = mylog.read().splitlines() # read log file in as list of lines

    # capture last log entry index value from previous processing as integer
    last_log_created = int(list_of_lines[-1].split(",")[0])
    print("Last log entry was: ",last_log_created,"\n")

# Get user to pick data folder i.e. folder holding all the CP files to be processed
root = tkinter.Tk()
root.withdraw()
my_path=filedialog.askdirectory()
my_processed_files_path = my_path + '//processed files'
root.destroy()

# get data folder contents as a list
dirlist = glob.glob(my_path + '/*.cp')

# init program variables
token = '['
num_cp_files = len(dirlist) # find number of data files in directory
event_data = []

# read through & parse all files in data folder
# range is 0 to total number of data files in the data folder
for current_cp_file_no in range(0,num_cp_files):

    # initialise the log number for the next input file
    current_log = last_log_created + 1
    last_log_created +=1 #
    date_input_file_was_created = time.ctime(os.path.getmtime(my_path))
    #log_file_processed =
    this_bout_data = [] # init empty array
    cp_file_sections = [] # init empty array

    print("Current log entry is: ",current_log)
    with open(dirlist[current_cp_file_no], "rt") as cp_file_input: # iterate through folder

        filename = "C"+cp_file_input.name.strip(my_path+'\\').strip(".cp") # filename with extra chars sliced off
        print("Current CP filename is: ",filename)
        for line in cp_file_input.readlines(): # readlines returns a list of lines input

            if line.startswith(token): # if current line starts with start token...

                if len(this_bout_data)>0:
                    # if bout data is not empty (note: it will be on first run)
                    cp_file_sections.append(this_bout_data) # append bout data

                # bout_data = [line[len(token):]] # full line with token char sliced off
                this_bout_data = [line[0:]] # full line with token char [0] included

            else: # if current line doesn't start with start token
                this_bout_data.append(line)

        if len(this_bout_data)>0: # if bout data is not empty (note: it will be on first run)
            cp_file_sections.append(this_bout_data) # array with ALL bout data sections extracted

    print ("Current file's data is:  ",cp_file_sections)
    #print ("Number of sections in this bout data: ",len(cp_file_sections))

    # extract 'definition' data from current cp_file input
    definition = cp_file_sections[2]
    definition = definition[1:len(definition)-1]
    #print("[Definition] section in full: ",definition)

    # **********************************************************************************
    # Get all 'bout specific' data section names from the [Definition]
    # section as a list.
    definition_dict = {}
    definition = enumerate(definition)
    for key, value in definition:

        # split the value element into a 2 element list [section-name, section-value]
        value = value.split("=")

        # re-assign all the dict keys with all the section-names
        key = value[0]
        # re-assign the dict values with the section-values
        value = value[1]

        # build dictionary by iteratively adding each new key,value pair
        definition_dict.update({key:value})
        # this puts all the section names in a list
        list_of_definition_keys = list(definition_dict.keys())

    # print [Definition] section
    # print("[Definition] section of this file as a dictionary: ",definition_dict)
    # print("List of keys in [Definition] section of this file : ",list_of_definition_keys)

    #  This list is used to find the indices of all the 'bout specific' data sections.
    if list_of_definition_keys.index("CombPoints"): # Check if [CombPoints] section exists in the CP file
        success = True

        # add 3 to current index value account for the format of the CP file
        combPoints_index = list_of_definition_keys.index("CombPoints") + 3;
        # print("This file's combPoints index is: ",combPoints_index)
        combPoints_data = cp_file_sections[combPoints_index] # extract specific scores data using the index value
        # print("This bout's combPoint scores are: ",combPoints_data)
        number_of_rounds = len(combPoints_data)-2 # get the number of rounds implied from scores data available

        # add 3 to current index value account for the format of the CP file
        bouts_index = list_of_definition_keys.index("Bouts") + 3;
        # extract specific bout data using the index value
        bouts_data = cp_file_sections[bouts_index][1].split(";")[:]
        print("There was %d round(s) in this bout." % number_of_rounds)

        #print("This bouts boxer data is: ",bouts_data)
        red_boxer = bouts_data[13]
        red_club = bouts_data[14]
        blue_boxer = bouts_data[19]
        blue_club = bouts_data[20]
        print("Boxers Names (red VS blue): ",red_boxer," ("+red_club+") - VS - ",blue_boxer," ("+blue_club+")")

        actual_scores = combPoints_data[1:len(combPoints_data)-1]
        # print("...And the actual scores are: ",actual_scores)

        # The following sequence is used to parse the specific judges scoresper round from the CP files
        rnd=1
        this_rnd_scores=[]
        #print() # create some whitespace in output for clarity
        while rnd <= number_of_rounds:

            # have to use rnd-1 here due to list indices starting at 0
            this_rnd_scores = actual_scores[rnd-1]

            this_rnd_scores = this_rnd_scores.split(";")

            j1 = this_rnd_scores[3:5]
            #print("judge 1 scored rd %d: %s" % (rnd+1,j1))
            j2 = this_rnd_scores[5:7]
            #print("judge 2 scored rd %d: %s" % (rnd+1,j2))
            j3 = this_rnd_scores[7:9]
            #print("judge 3 scored rd %d: %s" % (rnd+1,j3))
            j4 = this_rnd_scores[9:11]
            #print("judge 4 scored rd %d: %s" % (rnd+1,j4))
            j5 = this_rnd_scores[11:13]
            #print("judge 5 scored rd %d: %s" % (rnd+1,j5))
            this_rnd_scores = [j1,j2,j3,j4,j5]
            print("Round %d scores were: %s" % (rnd,this_rnd_scores))

            rnd +=1

    else:
        success = False
        print("No combPoints found, check this file: ",filename)

    #combPoints section does not exist, need to redirect

    # close the input CP file
    cp_file_input.close()

    if success:

        print(" *** File processed", end="...\u2713 Bout data extracted")

        current_log_string = str(current_log) + \
                             ", " + str(my_path) + ", " \
                             + str(filename) + ", " \
                             + str(date_input_file_was_created) + ", " \
                             + str(now.strftime("%Y-%m-%d %H:%M"))

        print("\n *** Log updated", end="...\u2713 " + str(current_log_string) + "\n")

        # THIS IS WHERE I NEED TO UPDATE THE LOG FILE

    else:

        current_log_string = + "Check CP file: " + ", " \
                             + str(my_path) + ", " \
                             + str(filename) + ", " \
                             + str(date_input_file_was_created) + ", " \
                             + str(now.strftime("%Y-%m-%d %H:%M"))

        print("\n*** Error: Log NOT updated",end="...\u274c "+str(current_log_string)+"\n")

    # create a spacer for clarity when displaying output
    print(" **************************************************************************\n")

# *****************************************************************
    # print() # create whitespace o/p
    # create single array with all event data
    event_data.append(cp_file_sections)
# *****************************************************************


print("Number of files read: ",num_cp_files)
#filename = filename.strip("data\\")
print("Last file processed was: ",filename)
print("Last log entry:", current_log,
      " Filename:", filename,
      " File created:",date_input_file_was_created,
      " File processed:",now.strftime("%Y-%m-%d %H:%M"))












'''

#    competition = cp_file_sections[5]
    #competition = competition.split
#    print("competition name is: ",competition)
    # extract headline
#    headline = cp_file_sections[4]
#    print("headline is: ",headline)
    # extract result code
#    legend = cp_file_sections[7]
#    print("result of this bout: ",legend)



reportCode_Index = [i for i, s in enumerate(definition) if 'ReportCode=' in s]
reportCode_Index=reportCode_Index[0] # only get value of index
print("reportCode_Index is: ",reportCode_Index)

headline_Index = [i for i, s in enumerate(definition) if 'Headline=' in s]
headline_Index=headline_Index[0] # only get value of index
print("headline_Index is: ",headline_Index)

Competition_Index = [i for i, s in enumerate(definition) if 'Competition=' in s]
Competition_Index=Competition_Index[0] # only get value of index
print("Competition_Index is: ",Competition_Index)

config_Index = [i for i, s in enumerate(definition) if 'config=' in s]
config_Index=config_Index[0] # only get value of index
print("config_Index is: ",config_Index)

TeamInfo_Index = [i for i, s in enumerate(definition) if 'TeamInfo=' in s]
TeamInfo_Index=int(TeamInfo_Index) # only get value of index
print("TeamInfo_Index is: ",TeamInfo_Index)

Sessions_Index = [i for i, s in enumerate(definition) if 'Sessions=' in s]
Sessions_Index=Sessions_Index[0] # only get value of index
print("Sessions_Index is: ",Sessions_Index)

Bouts_Index = [i for i, s in enumerate(definition) if 'Bouts=' in s]
print("Bouts_Index is: ",Bouts_Index)

Remis_Index = [i for i, s in enumerate(definition) if 'Remis=' in s]
print("Remis_Index is: ",Remis_Index)

Judges_Index = [i for i, s in enumerate(definition) if 'Judges=' in s]
print("Judges_Index is: ",Judges_Index)

IndTotal_Index = [i for i, s in enumerate(definition) if 'IndTotal=' in s]
print("IndTotal_Index is: ",IndTotal_Index)

CombPoints_Index = [i for i, s in enumerate(definition) if 'CombPoints=' in s]
print("CombPoints_Index is: ",CombPoints_Index)

DetailScores_Index = [i for i, s in enumerate(definition) if 'DetailScores=' in s]
print("DetailScores_Index is: ",DetailScores_Index)

Message_Index = [i for i, s in enumerate(definition) if 'Message=' in s]
print("Message_Index is: ",Message_Index)

Notes_Index = [i for i, s in enumerate(definition) if 'Notes=' in s]
print("Notes_Index is: ",Notes_Index)

LegendHead_Index = [i for i, s in enumerate(definition) if 'LegendHead=' in s]
LegendHead_Index=LegendHead_Index[0] # only get value of index
print("LegendHead_Index is: ",LegendHead_Index)

Legend_Index = [i for i, s in enumerate(definition) if 'Legend=' in s]
Legend_Index=Legend_Index[0] # only get value of index
print("Legend_Index is: ",Legend_Index)

ReportProp_Index = [i for i, s in enumerate(definition) if 'ReportProp=' in s]
ReportProp_Index=ReportProp_Index[0] # only get value of index
print("ReportProp_Index is: ",ReportProp_Index)
'''
'''






'''

'''
print("\nnumber of files read:\n",num_cp_files)
print ("\nlast cp file read:\n",cp_file_sections)
print ("\nlast cp file read - extracted from event_data:\n",event_data[31])


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

headline = cp_file_sections[4]
print(headline)

competition = cp_file_sections[5]
print(competition)

teamInfo = cp_file_sections[7]
print(teamInfo)

sessions = cp_file_sections[8]
print(sessions)

bouts = cp_file_sections[9]
print(bouts)

officials = cp_file_sections[11]
print(officials)

combPoints = cp_file_sections[13]
print(combPoints)

detailScores = cp_file_sections[14]
print(detailScores)

legend = cp_file_sections[18]
print(legend)

'''
