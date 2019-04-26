import glob
import os.path, time
import datetime
import csv
import tkinter
from tkinter import filedialog

# Get current date
now = datetime.datetime.now()


# PICK DATA FOLDER
########################################################################################################################
#  Get user to pick data folder i.e. folder holding all the CP files to be processed
root = tkinter.Tk()
root.withdraw()
my_path=filedialog.askdirectory()
my_processed_files_path = my_path + '//processed files'
root.destroy()
# get data folder contents as a list
dirlist = glob.glob(my_path + '/*.cp')
#

# OPEN LOGGER
########################################################################################################################
print("Open my csv log here...")
#C:\Users\Cenit\Documents\PW\9_Projects\Major_project\Data\proc_data.log.txt
mylog = open('C:/Users/Cenit/Documents/PW/9_Projects/Major_project/Data/proc_data.log', 'r+')
# read lines of log file in as list of lines
list_of_lines = mylog.readlines()

# capture the very last log entry index value from previous processing as integer
last_log_number_created = int(list_of_lines[-1].split(",")[0])
print("Last log entry was: ",last_log_number_created,"\n")

# INITIALISE VARIABLES HERE
########################################################################################################################
# init some program variables
token = '['
num_cp_files = len(dirlist) # find number of data files in directory
event_data = []


# MAIN LOOP TO PROCESS ALL C73.CP FILES FOUND IN THE DATA FOLDER SELECTED ABOVE
########################################################################################################################
# read through & parse all files in data folder
# range is 0 to total number of data files in the data folder
for current_cp_file_no in range(0,num_cp_files):

    # initialise the log number for the next input file
    current_log_number = last_log_number_created + 1
    last_log_number_created += 1
    date_input_cp_file_was_created = time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(my_path)))
    this_bout_data = [] # init empty array
    cp_file_sections = [] # init empty array

    print("Current log entry is: ",current_log_number)

    # iterate through folder
    with open(dirlist[current_cp_file_no], "rt") as cp_file_input:

        # filename with extra chars sliced off
        filename = "C"+cp_file_input.name.strip(my_path+'\\').strip(".cp")
        print("Current C73.cp filename is: ",filename)

        # readlines returns an iterative list of lines input from the cp_file_input
        for line in cp_file_input.readlines():

            # if current line starts with the start token...
            if line.startswith(token):

                if len(this_bout_data)>0:
                    # if length of the list "this_bout_data" is NOT empty
                    # (note: it will be empty on the first run)
                    cp_file_sections.append(this_bout_data) # append bout data

                # bout_data = [line[len(token):]] # full line with token char sliced off
                this_bout_data = [line[0:]] # full line with token char [0] included

            else: # if current line doesn't start with start token
                this_bout_data.append(line)

        # if bout data is not empty (note: it will be on first run)
        if len(this_bout_data) > 0:
            # array with ALL Data Sections extracted
            cp_file_sections.append(this_bout_data)

    print ("Current file's data is:  ",cp_file_sections)
    #print ("Number of sections in this bout data: ",len(cp_file_sections))

    # extract 'definition' data from current cp_file input
    definition = cp_file_sections[2]
    definition = definition[1:]
    definition.pop()
    #definition = definition[1:len(definition)-1]
    #print("\nThe [Definition] section data: ",definition)

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
    #  This list is used to find the indices of all the 'bout specific' data sections.
    list_of_definition_keys = list(definition_dict.keys())

    # print [Definition] section
    # print("[Definition] section of this file as a dictionary: ",definition_dict)
    # print("List of keys in [Definition] dictionary: ",list_of_definition_keys)

    if list_of_definition_keys.index("CombPoints"): # Check if [CombPoints] section exists in the CP file

        success = True

        # add 3 to the current index values to account for the format of the CP files
        reportCode_section_index = list_of_definition_keys.index("ReportCode") + 3;
        competition_section_index = list_of_definition_keys.index("Competition") + 3;
        combPoints_section_index = list_of_definition_keys.index("CombPoints") + 3;
        bouts_section_index = list_of_definition_keys.index("Bouts") + 3;
        officials_section_index = list_of_definition_keys.index("Judges") + 3;

        # get definition of all data blocks in Reportcode section
        reportCode_section_definitions = definition_dict["ReportCode"].split(";")
        #print("\nThe [reportCode] section definitions: ",reportCode_section_definitions)
        # extract specific scores data using the index value
        reportCode_data = cp_file_sections[reportCode_section_index][1:][0].split(";")
        #reportCode_data[:-1] = reportCode_data[:-1].rstrip("\n")
        #print("-- The [reportCode] section data is: ",reportCode_data)

        # get definition of all data blocks in competition section
        competition_section_definitions = definition_dict["Competition"].split(";")
        #print("\nThe [Competition] section definitions: ",competition_section_definitions)
        # extract specific scores data using the index value
        competition_data = cp_file_sections[competition_section_index][1:][0].split(";")
        #print("-- The [Competition] section data is: ",competition_data)

        # get definition of all data blocks in combPoints section
        combPoints_section_definitions = definition_dict["CombPoints"].split(";")
        #print("\nThe [CombPoints] section definitions: ",combPoints_section_definitions)
        # extract specific scores data using the index value
        # grab everything including section name and final newline char
        combPoints_data = cp_file_sections[combPoints_section_index][1:]
        combPoints_data.pop(-1) # remove the '\n' char element from list
        #print("-- The [CombPoint] section data is: ",combPoints_data)
        number_of_rounds= len(combPoints_data)

        # strip section name and final newline char from data
        #actual_scores = combPoints_data[0:len(combPoints_data)-1]
        # print("...And the actual scores are: ",actual_scores)

        # get definition of all data blocks in bouts section
        bouts_section_definitions = definition_dict["Bouts"].split(";")
        print("\nThe [bouts] section definitions: ",bouts_section_definitions)
        # extract specific bout data using the index value
        bouts_data = cp_file_sections[bouts_section_index][1:][0].split(";")
        print("-- The [bouts] section data is: ",bouts_data)

        # get definition of all data blocks in Judges section
        officials_section_definitions = definition_dict["Judges"].split(";")
        #print("\nThe [Judges] section definitions: ",officials_section_definitions)
        # extract specific Judges data using the index value
        officials_data = cp_file_sections[officials_section_index][1].split(";")
        #print("-- The [Judges] section data is: ",officials_data)

        referee_name_index = officials_section_definitions.index("NameRef")
        referee_name = officials_data[referee_name_index]
        referee_nat_index = officials_section_definitions.index("NatRef")
        referee_nat = officials_data[referee_nat_index]

        judge1_name_index = officials_section_definitions.index("NameJG1")
        judge1_name = officials_data[judge1_name_index]
        judge1_nat_index = officials_section_definitions.index("NatJG1")
        judge1_nat = officials_data[judge1_nat_index]

        judge2_name_index = officials_section_definitions.index("NameJG2")
        judge2_name = officials_data[judge2_name_index]
        judge2_nat_index = officials_section_definitions.index("NatJG2")
        judge2_nat = officials_data[judge2_nat_index]

        judge3_name_index = officials_section_definitions.index("NameJG3")
        judge3_name = officials_data[judge3_name_index]
        judge3_nat_index = officials_section_definitions.index("NatJG3")
        judge3_nat = officials_data[judge1_nat_index]

        judge4_name_index = officials_section_definitions.index("NameJG4")
        judge4_name = officials_data[judge4_name_index]
        judge4_nat_index = officials_section_definitions.index("NatJG4")
        judge4_nat = officials_data[judge1_nat_index]

        judge5_name_index = officials_section_definitions.index("NameJG5")
        judge5_name = officials_data[judge5_name_index]
        judge5_nat_index = officials_section_definitions.index("NatJG5\n")
        judge5_nat = officials_data[judge1_nat_index]

        # get each official specific data
        print("\nOfficials for this bout:"
              + "\n -- Referee: " + referee_name + " ("+referee_nat+")"
              + "\n -- Judge1: "+ judge1_name + " ("+judge1_nat+")"
              + "\n -- Judge2: "+ judge2_name + " ("+judge2_nat+")"
              + "\n -- Judge3: "+ judge3_name + " ("+judge3_nat+")"
              + "\n -- Judge4: "+ judge4_name + " ("+judge4_nat+")"
              + "\n -- Judge5: "+ judge5_name + " ("+judge5_nat+")")

        # get each boxer specific data
        red_name_index = bouts_section_definitions.index("NameRed")
        red_boxer_name = bouts_data[red_name_index]
        red_club_index = bouts_section_definitions.index("NatRed")
        red_club = bouts_data[red_club_index]
        red_NR_index = bouts_section_definitions.index("NrRed")
        red_NR = bouts_data[red_NR_index]
        # ------------------------------------------------------------------------
        blue_name_index = bouts_section_definitions.index("NameBlue")
        blue_boxer_name = bouts_data[blue_name_index]
        blue_club_index = bouts_section_definitions.index("NatBlue")
        blue_club = bouts_data[blue_club_index]
        blue_NR_index = bouts_section_definitions.index("NrBlue")
        blue_NR = bouts_data[blue_NR_index]

        winner_index = bouts_section_definitions.index("Winner")
        winner_data = bouts_data[winner_index]

        print("\nBoxers in this bout:"
            + "\n -- Red corner: " + red_NR + " " + red_boxer_name + " ("+red_club+")"
            + "\n -- Blue corner: " + blue_NR + " " +  blue_boxer_name + " ("+blue_club+")")

        # get the number of rounds implied from the scores data that is available
        print("\nThere was %d round(s) in this bout.\n" % number_of_rounds)

        # The following sequence is used to parse the specific judges
        # scores per round from the CP files
        rnd_num=1
        this_rnd_scores=[]
        for rnd_num in range(1,number_of_rounds+1):

            # have to use rnd-1 here due to list indices starting at 0
            this_rnd_scores = combPoints_data[rnd_num-1]
            this_rnd_scores = this_rnd_scores.split(";")

            # extract individual judges' scores from the scores data
            # as separate two element lists
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

            # combine the individual judges scores lists into one list again
            this_rnd_scores = [j1,j2,j3,j4,j5]
            print("Round %d scores were: %s" % (rnd_num, this_rnd_scores))

            # next round
            rnd_num += 1

        opponents = {red_NR: "Red corner " + red_boxer_name + " (" + red_club +")",
                     blue_NR: "Blue corner " +  blue_boxer_name+ " (" + blue_club +")"}
        winner_name = opponents.get(winner_data, "Nr no. "+ winner_data)
        print("\n -- Winner is: ",winner_name )

    else:
        #combPoints section does not exist, need to redirect
        success = False
        print("No combPoints found, check this file: ",filename)

    # close the input CP file
    cp_file_input.close()



# UPDATE THE LOGGER
###############################################################################################################################
    if success:

        print("\n *** File processed", end="...\u2713 Bout data extracted")

        current_log_string = str(current_log_number) + \
                             ", " + str(my_path) + ", " \
                             + str(filename) + ", " \
                             + str(date_input_cp_file_was_created) + ", " \
                             + str(now.strftime("%d-%m-%Y @ %H:%M"))

        # UPDATE THE LOG FILE
        mylog.write("\n"+str(current_log_string))
        print("\n *** Log updated", end="...\u2713 " + current_log_string + "\n")

    else:

        num_cp_files -= 1
        current_log_string = + "Check CP file: " + ", " \
                             + str(my_path) + ", " \
                             + str(filename) + ", " \
                             + str(date_input_cp_file_was_created) + ", " \
                             + str(now.strftime("%d-%m-%Y @ %H:%M"))

        print("\n*** Error: Log NOT updated",end="...\u274c "+str(current_log_string)+"\n")

    # create a spacer for clarity when displaying output
    print(" **************************************************************************\n")

# *****************************************************************
    # print() # create whitespace o/p
    # create single array with all event data
    event_data.append(cp_file_sections)
# *****************************************************************

# close the logger file
mylog.close()
print("Number of files processed: ",num_cp_files)
#filename = filename.strip("data\\")
print("Last file processed was: ",filename)
print("Last log entry:", current_log_string)


'''

index_of_j1_red = 
index_of_j1_blue = 
index_of_j2_red = 
index_of_j2_blue =
index_of_j3_red = 
index_of_j3_blue =
index_of_j4_red = 
index_of_j4_blue =
index_of_j5_red = 
index_of_j5_blue =

'''

