###############################################################################################################
# Filename: c73_ResultsFileParser.py
# Author: Paul Williamson
# Date: 14/08/2017
########################################################################################################################
# IMPORT MODULES HERE
########################################################################################################################
import glob
import sys
import os
import datetime
import time
import tkinter
from tkinter import ttk
from tkinter import filedialog
# Get current date
now = datetime.datetime.now()
# *****************************************************************

########################################################################################################################
# DECLARE FUNCTION
########################################################################################################################
def printing(text,fileobject):
    print(text)
    fileobject.write(text)
# *****************************************************************

########################################################################################################################
# PICK DATA FOLDER
########################################################################################################################
#  Get user to pick data folder i.e. folder holding all the CP files to be processed
file_dialog_root = tkinter.Tk()
file_dialog_root.withdraw()
datapath=filedialog.askdirectory(title="Select folder with C73.cp event files...")
if not datapath:
    print("You cancelled!!! Goodbye") # eventlog does not exist here
    sys.exit("") # handle dialog cancel event
else:
    eventlog=open(datapath + '/eventlog.txt','w')
    printing("Proceeding...",eventlog)
# *****************************************************************


# GET DATA FOLDER CONTENTS AS A LIST
########################################################################################################################
datafile_directory_list = glob.glob(datapath + '/*.cp')
# find the total number of data files in data folder
number_of_cp_files = len(datafile_directory_list)
# *****************************************************************


# INDICATE CURRENT WORKING DIRECTORY
########################################################################################################################
#current_working_directory = os.getcwd()
#print("\nCurrent working directory is: ",current_working_directory)
# *****************************************************************


# CREATE NEW PATH FOR DATALOG FOLDER FOR THE LOGS OF PROCESSED FILES
# at the same location of the actual data files
########################################################################################################################
logpath = str(datapath + '/datalog')
if not os.path.exists(logpath):
    os.makedirs(logpath)
    printing("\nNew datalog directory will be created here: " + logpath, eventlog)
else: printing("\nCurrent datalog directory already exists here: " + logpath, eventlog)
# *****************************************************************


# INITIALISE VARIABLES HERE
########################################################################################################################
# init some program variables
token = '['
event_data = []
file_errors = 0
data_format = ""


# OPEN PROCESS LOG NOW - AT BEGINNING OF DATA CAPTURE PROCESS
########################################################################################################################
#print("\nOpening process log...",file=eventlog,flush="TRUE")
print("\nOpening process log...")
with open('C:/_project/log/process_data.log', 'r+') as processlog:
    # read all lines of the process log file in as a list (of lines)
    list_of_process_log_lines = processlog.readlines()
    #print("List of lines from process log:\n",list_of_process_log_lines)
    # capture the LAST log entry index value as an integer
    last_log_number_created = int(list_of_process_log_lines[-1].split(";")[0])
    #print(" -- Last log entry was: ",last_log_number_created,file=eventlog,flush="TRUE")
    printing("\n -- Last log entry was: " + str(last_log_number_created), eventlog)
    processlog.write("\n") # create whitespace in the process log between events

progressbar_root = tkinter.Tk()
progressbar_value=0
progressbar = ttk.Progressbar(progressbar_root,
                              orient='horizontal',
                              length="10c",
                              mode='determinate',
                              maximum = number_of_cp_files+1,
                              variable=progressbar_value)
progressbar.pack(expand=1)
progressbar.start()
progressbar.update()
##########################################################################################
# MAIN LOOP TO PROCESS ALL C73.CP FILES FOUND IN THE DATA FOLDER SELECTED ABOVE
##########################################################################################
# FOR loop to parse all files in data folder. The range is from
# 0 up to the total number of data files in the data folder
for current_cp_file_no in range(0,number_of_cp_files):


    # IF LOG FILES DON'T EXIST CREATE THEM NOW, THESE LOG FILES WILL
    # BE UPDATED AFTER EACH RESULT FILE GETS PROCESSED
    # Run the following code if this is the first C73.cp file
    if current_cp_file_no == 0:

        bouts_logpath = logpath+"/bouts_data_table.csv"
        with open(bouts_logpath, "w+") as bouts_data_table:
            bouts_data_table.write("current_log_number;"
                                          "competition_name;"
                                          "competition_firstday;"
                                          "competition_lastday;"
                                          "competition_venue;"
                                          "competition_session_num;"
                                          "competition_session_name;"
                                          "competition_bout_date;"
                                          "competition_bout_time;"
                                          "competition_bout_number;"
                                          "competition_bout_weight_class;"
                                          "competition_bout_weight (KG);"
                                          "competition_bout_gender;"
                                          "competition_bout_groupname;"
                                          "red_boxer_name;red_club;"
                                          "blue_boxer_name;blue_club;"
                                          "referee_name; referee_nat;"
                                          "judge1_name; judge1_nat;"
                                          "judge2_name; judge2_nat;"
                                          "judge3_name; judge3_nat;"
                                          "judge4_name; judge4_nat;"
                                          "judge5_name; judge5_nat;"
                                          "data_format;"
                                          "number_of_rounds;"
                                          "result_text;"
                                          "winner")
            printing("\n -- Bouts data table is here: " + bouts_logpath, eventlog)

        boxers_logpath = logpath+"/boxers_data_table.csv"
        with open(boxers_logpath, "w+") as boxers_data_table:
            boxers_data_table.write("current_log_number;"
                                    "red_boxer_name;"
                                    "red_club;"
                                    "blue_boxer_name;"
                                    "blue_club;"
                                    "winner_name")
            printing("\n -- Boxers data table is here: " + boxers_logpath, eventlog)

        boutscores_logpath = logpath+"/boutscores_data_table.csv"
        with open(boutscores_logpath, "w+") as boutscores_data_table:
            boutscores_data_table.write("current_log_number;"
                                        "J1r1;J1b1;J2r1;J2b1;J3r1;J3b1;J4r1;J4b1;J5r1;J5b1;kdr1;kdb1;wr1;wb1;"
                                        "ix1r1;ix1b1;ix2r1;ix2b1;ix3r1;ix3b1;ix4r1;ix4b1;ix5r1;ix5b1;"
                                        "J1r2;J1b2;J2r2;J2b2;J3r2;J3b2;J4r2;J4b2;J5r2;J5b2;kdr2;kdb2;wr2;wb2;"
                                        "ix1r2;ix1b2;ix2r2;ix2b2;ix3r2;ix3b2;ix4r2;ix4b2;ix5r2;ix5b2;"
                                        "J1r3;J1b3;J2r3;J2b3;J3r3;J3b3;J4r3;J4b3;J5r3;J5b3;kdr3;kdb3;wr3;wb3;"
                                        "ix1r3;ix1b3;ix2r3;ix2b3;ix3r3;ix3b3;ix4r3;ix4b3;ix5r3;ix5b3;"
                                        "J1r4;J1b4;J2r4;J2b4;J3r4;J3b4;J4r4;J4b4;J5r4;J5b4;kdr4;kdb4;wr4;wb4;"
                                        "ix1r4;ix1b4;ix2r4;ix2b4;ix3r4;ix3b4;ix4r4;ix4b4;ix5r4;ix5b4")
            printing("\n -- Boutscores data table is here: " + boutscores_logpath, eventlog)

        officials_logpath = logpath+"/officials_data_table.csv"
        with open(officials_logpath, "w+") as officials_data_table:
            officials_data_table.write("current_log_number;"
                                       "referee_name; referee_nat;"
                                       "judge1_name; judge1_nat;"
                                       "judge2_name; judge2_nat;"
                                       "judge3_name; judge3_nat;"
                                       "judge4_name; judge4_nat;"
                                       "judge5_name; judge5_nat")
            printing("\n -- Officials data table is here: " + officials_logpath, eventlog)

    # Initialise empty variables used in the main FOR loop
    this_bout_data = []
    cp_file_sections = []
    this_bout_scores_string = ""

# UPDATE PROGRESS BAR
###############################################################################################################################
    progressbar_value = current_cp_file_no
    progressbar.update()

    # initialise the log number for the next input file
    current_log_number = last_log_number_created + 1 # set current log number
    printing("\nCurrent log entry is: " + str(current_log_number), eventlog)
    last_log_number_created += 1 # increment last log number by 1
    date_input_cp_file_was_created = \
        time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(datapath)))

    # Open the current individual C73.cp file
    with open(datafile_directory_list[current_cp_file_no], "r") as cp_file_input:

        # filename with extra chars sliced off
        filename = cp_file_input.name.strip(datapath).strip("\\")+"cp"
        printing("\nCurrent C73.cp filename is: " + filename, eventlog)

        # readlines returns an iterative list of all the lines in the cp_file_input
        for line in cp_file_input.readlines():

            # if current line starts with the start token...
            if line.startswith(token):

                if len(this_bout_data)>0:
                    # if length of the list "this_bout_data" is NOT empty
                    # (note: it will be empty on the first run)
                    cp_file_sections.append(this_bout_data) # append bout data

                # this_bout_data = [line[len(token):]] # full line with token char sliced off
                this_bout_data = [line[0:]] # full line with token char [0] included

            else: # if current line doesn't start with start token
                this_bout_data.append(line)

        # if bout data is not empty (note: it will be on first run)
        if len(this_bout_data) > 0:
            # array with ALL Data Sections extracted
            cp_file_sections.append(this_bout_data)

    #print ("Current cp_file sections are:  ",cp_file_sections)
    #print ("Number of sections in this bout data: ",len(cp_file_sections))

    # extract 'definition' data from current cp_file input
    definition = cp_file_sections[2] # pull out the definitions section
    definition = definition[1:] # remove definitions section name at element[0]
    definition.pop() # remove the last element from the definition (newline char)
    #print("The [Definition] section data is: ",definition)

    # Get all the required data_section names from the [Definition]
    # section as a dictionary.
    definition_dict = {}
    definition = enumerate(definition)
    for key, value in definition:
        # split the value element into a 2 element list [section-name, section-values]
        value = value.split("=")
        # re-assign all the dict key with the section-name
        key = value[0]
        # re-assign the dict value with the section-value
        value = value[1]
        # build new dictionary by iteratively adding each new key,value pair
        definition_dict.update({key:value})

    # This puts all the section names in a list
    # This list is then used to find the indices of all the 'bout specific' data sections.
    list_of_definition_keys = list(definition_dict.keys())

    # Check if [CombPoints] section exists in the CP file
    # If it exists then this current file can be processed
    try:
        if list_of_definition_keys.index("CombPoints"):
            combPoints_exists = True # [CombPoints] section exists in definition list so CP file can be processed
            printing("\nCombPoints Found: YES\n", eventlog)
    except ValueError:
        #combPoints section does not exist, need to redirect
        combPoints_exists = False
        printing("\n*** Error: CombPoints Found: NO...check this file: " + filename + " ***\n", eventlog)

    # IF [COMBPOINTS] SECTION IS FOUND THEN THIS INPUT CP FILE CAN BE PROCESSED...
    if combPoints_exists:

        # add 3 to the current index values to account for the usual format of the CP files
        reportCode_section_index = list_of_definition_keys.index("ReportCode") + 3;
        competition_section_index = list_of_definition_keys.index("Competition") + 3;
        combPoints_section_index = list_of_definition_keys.index("CombPoints") + 3;
        bouts_section_index = list_of_definition_keys.index("Bouts") + 3;
        officials_section_index = list_of_definition_keys.index("Judges") + 3;
        sessions_section_index = list_of_definition_keys.index("Sessions") + 3;

        # [ReportCode]: Get definition of all data blocks in Reportcode section
        reportCode_section_definitions = definition_dict["ReportCode"].split(";")
        reportCode_data = cp_file_sections[reportCode_section_index][1:][0].split(";")
        #print("\nThe [reportCode] section definitions: ",reportCode_section_definitions)
        #print("-- The [reportCode] section data is: ",reportCode_data)

        # [Competition]: Get definition of all data blocks in Competition section
        competition_section_definitions = definition_dict["Competition"].split(";")
        competition_data = cp_file_sections[competition_section_index][1:][0].split(";")
        #print("\nThe [Competition] section definitions: ",competition_section_definitions)
        #print("-- The [Competition] section data is: ",competition_data)

        # [Sessions]: Get definition of all data blocks in Sessions section
        sessions_section_definitions = definition_dict["Sessions"].rstrip("\n")
        sessions_section_definitions = sessions_section_definitions.split(";")
        sessions_data = cp_file_sections[sessions_section_index][1:][0].split(";")
        sessions_data.pop()
        #print("The [Sessions] section definitions: ",sessions_section_definitions)
        #print("-- The [sessions] section data: ",sessions_data)

        # Venue info is found in the [Sessions] section... Why???
        competition_venue_index = sessions_section_definitions.index("Venue")
        competition_venue = sessions_data[competition_venue_index]

        competition_name_index = competition_section_definitions.index("CompName")
        competition_name = competition_data[competition_name_index]

        printing("\nThe competition was: " + competition_name, eventlog)

        competition_firstday_index = competition_section_definitions.index("FirstDay")
        competition_firstday = competition_data[competition_firstday_index]
        competition_lastday_index = competition_section_definitions.index("LastDay")
        competition_lastday = competition_data[competition_lastday_index]

        printing("\nThe competition dates were: %s to %s" % (competition_firstday,competition_lastday), eventlog)

        competition_session_num_index = sessions_section_definitions.index("Session")
        competition_session_num = sessions_data[competition_session_num_index]
        competition_session_name_index = sessions_section_definitions.index("Name")
        competition_session_name = sessions_data[competition_session_name_index]
        competition_bout_number_index = competition_section_definitions.index("CurrentBout")
        competition_bout_number = competition_data[competition_bout_number_index]

        printing("\nThe venue for the competition was: " + competition_venue, eventlog)

        printing("\nThis was bout number %s of the competition, which took place during session (%s) %s"
                  % (competition_bout_number, competition_session_num, competition_session_name), eventlog)

        competition_bout_date_index = competition_section_definitions.index("UpdDate")
        competition_bout_date = competition_data[competition_bout_date_index]
        competition_bout_time_index = competition_section_definitions.index("UpdTime")
        competition_bout_time = competition_data[competition_bout_time_index][0:8]

        printing("\nThe date and time for the bout was: %s %s" % (competition_bout_date,competition_bout_time), eventlog)

        # [CombPoints]: Get definition of all data blocks in CombPoints section
        combPoints_section_definitions = definition_dict["CombPoints"].rstrip("\n")#
        combPoints_section_definitions = combPoints_section_definitions.split(";")

        # extract specific scores data using the index value
        combPoints_data = cp_file_sections[combPoints_section_index][1:] # drop section name
        combPoints_data.pop() # remove the last '\n' char element from list
        #print("\nThe [CombPoints] section definitions: ",combPoints_section_definitions)
        #print("-- The [CombPoint] section data is: ",combPoints_data)

        # Each line/element in combPoint data is the data for a single round
        # => Number of lines/elements = number of rounds
        number_of_rounds= len(combPoints_data)
        for round in range(0,number_of_rounds):
            combPoints_data[round] = combPoints_data[round].rstrip("\n")
            #print("-- Round %d [CombPoints] data: %s" % (round+1,combPoints_data[round]))

        # [Bouts] get definition of all data blocks in Bouts section
        bouts_section_definitions = definition_dict["Bouts"].split(";")
        bouts_data = cp_file_sections[bouts_section_index][1:][0].split(";")
        #print("\nThe [bouts] section definitions: ",bouts_section_definitions)
        #print("-- The [bouts] section data is: ",bouts_data)

        # extract specific bout data using the index value
        competition_bout_weight_class_index = bouts_section_definitions.index("WClass")
        competition_bout_weight_class = bouts_data[competition_bout_weight_class_index]
        competition_bout_weight_index = bouts_section_definitions.index("Weight")
        competition_bout_weight = bouts_data[competition_bout_weight_index]
        competition_bout_gender_index = bouts_section_definitions.index("Gender")
        competition_bout_gender = bouts_data[competition_bout_gender_index]
        competition_bout_groupname_index = bouts_section_definitions.index("GroupName")
        competition_bout_groupname = bouts_data[competition_bout_groupname_index]

        printing("\nThe category-weight-class for this bout was: %s %s %skg" % (competition_bout_gender,
                                                                           competition_bout_groupname,
                                                                           competition_bout_weight_class), eventlog)

        # [Judges] get definition of all data blocks in Judges section
        officials_section_definitions = definition_dict["Judges"].split(";")
        # extract specific Judges data using the index value
        officials_data = cp_file_sections[officials_section_index][1].split(";")
        #print("\nThe [Judges] section definitions: ",officials_section_definitions)
        #print("-- The [Judges] section data is: ",officials_data)

        # use the definitions from the judges section to
        # get specific data for each official involved
        # ------------------------------------------------------------------------
        referee_name_index = officials_section_definitions.index("NameRef")
        referee_name = officials_data[referee_name_index]
        referee_nat_index = officials_section_definitions.index("NatRef")
        referee_nat = officials_data[referee_nat_index]
        # ------------------------------------------------------------------------
        judge1_name_index = officials_section_definitions.index("NameJG1")
        judge1_name = officials_data[judge1_name_index]
        judge1_nat_index = officials_section_definitions.index("NatJG1")
        judge1_nat = officials_data[judge1_nat_index]
        # ------------------------------------------------------------------------
        judge2_name_index = officials_section_definitions.index("NameJG2")
        judge2_name = officials_data[judge2_name_index]
        judge2_nat_index = officials_section_definitions.index("NatJG2")
        judge2_nat = officials_data[judge2_nat_index]
        # ------------------------------------------------------------------------
        judge3_name_index = officials_section_definitions.index("NameJG3")
        judge3_name = officials_data[judge3_name_index]
        judge3_nat_index = officials_section_definitions.index("NatJG3")
        judge3_nat = officials_data[judge3_nat_index]
        # ------------------------------------------------------------------------
        judge4_name_index = officials_section_definitions.index("NameJG4")
        judge4_name = officials_data[judge4_name_index]
        judge4_nat_index = officials_section_definitions.index("NatJG4")
        judge4_nat = officials_data[judge4_nat_index]
        # ------------------------------------------------------------------------
        judge5_name_index = officials_section_definitions.index("NameJG5")
        judge5_name = officials_data[judge5_name_index]
        judge5_nat_index = officials_section_definitions.index("NatJG5\n")
        judge5_nat = officials_data[judge5_nat_index].strip("\n")
        # ------------------------------------------------------------------------
        printing("\n\nOfficials for this bout:"
                + "\n -- Referee: " + referee_name + " ("+referee_nat+")"
                + "\n -- Judge1: "+ judge1_name + " ("+judge1_nat+")"
                + "\n -- Judge2: "+ judge2_name + " ("+judge2_nat+")"
                + "\n -- Judge3: "+ judge3_name + " ("+judge3_nat+")"
                + "\n -- Judge4: "+ judge4_name + " ("+judge4_nat+")"
                + "\n -- Judge5: "+ judge5_name + " ("+judge5_nat+")", eventlog)

        # use the definitions from the bouts section
        # to get specific data about the boxers involved
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
        # ------------------------------------------------------------------------
        winner_index = bouts_section_definitions.index("Winner")
        winner_data = bouts_data[winner_index]
        result_index = bouts_section_definitions.index("Result")
        result_data = bouts_data[result_index]
        # ------------------------------------------------------------------------
        printing("\n\nBoxers in this bout:"
                + "\n -- Red corner: "
                + red_NR + ". " + red_boxer_name + " ("+red_club+")"
                + "\n -- Blue corner: "
                + blue_NR + ". " +  blue_boxer_name + " ("+blue_club+")", eventlog)

        # If pre-2017 data: Get the judge number indices for those judges
        # that were only considered for the result
        if len(combPoints_section_definitions)>52:
            data_format = "5-of-5J"
            ix1_index = combPoints_section_definitions.index("IX1")
            ix2_index = combPoints_section_definitions.index("IX2")
            ix3_index = combPoints_section_definitions.index("IX3")
            ix4_index = combPoints_section_definitions.index("IX4")
            ix5_index = combPoints_section_definitions.index("IX5")
            #print(" --> Round %s's five scores were: %s" % (this_round_number+1, this_round_scores))
        else:
            data_format = "3-of-5J"
            ix1_index = combPoints_section_definitions.index("IX1")
            ix2_index = combPoints_section_definitions.index("IX2")
            ix3_index = combPoints_section_definitions.index("IX3")

        # get the number of rounds implied from the scores data that is available
        printing("\n\nThis bout had %d round(s) and the score format was %s:" % (number_of_rounds, data_format), eventlog)

        # The following sequence is used to get the indices of the specific judges'
        # scores per round (i.e. per line) of the CombPoints section
        j1_redscore_index = combPoints_section_definitions.index("PR1")
        j1_bluescore_index = combPoints_section_definitions.index("PB1")
        j2_redscore_index = combPoints_section_definitions.index("PR2")
        j2_bluescore_index = combPoints_section_definitions.index("PB2")
        j3_redscore_index = combPoints_section_definitions.index("PR3")
        j3_bluescore_index = combPoints_section_definitions.index("PB3")
        j4_redscore_index = combPoints_section_definitions.index("PR4")
        j4_bluescore_index = combPoints_section_definitions.index("PB4")
        j5_redscore_index = combPoints_section_definitions.index("PR5")
        j5_bluescore_index = combPoints_section_definitions.index("PB5")
        kd_red_index = combPoints_section_definitions.index("KDR")
        kd_blue_index = combPoints_section_definitions.index("KDB")
        warn_red_index = combPoints_section_definitions.index("WRN")
        warn_blue_index = combPoints_section_definitions.index("WBN")

        # EXTRACT EACH ROUND'S ACTUAL SCORE DATA FROM EACH ROUND'S DATA
        # a FOR loop to iterate through all rounds-score data in combPoints section
        for this_round_number in range(0,number_of_rounds):

            # Initialise the list "this_round_scores" which is used to hold each rounds actual scores
            this_round_scores=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

            # each round's scores are contained in each single element of the combPoints_data
            this_round_scores_data = combPoints_data[this_round_number]#.rstrip("\n")
            this_round_scores_data = this_round_scores_data.split(";")

            j1_redscore = this_round_scores_data[j1_redscore_index]
            j1_bluescore = this_round_scores_data[j1_bluescore_index]
            j2_redscore = this_round_scores_data[j2_redscore_index]
            j2_bluescore = this_round_scores_data[j2_bluescore_index]
            j3_redscore = this_round_scores_data[j3_redscore_index]
            j3_bluescore = this_round_scores_data[j3_bluescore_index]
            j4_redscore = this_round_scores_data[j4_redscore_index]
            j4_bluescore = this_round_scores_data[j4_bluescore_index]
            j5_redscore = this_round_scores_data[j5_redscore_index]
            j5_bluescore = this_round_scores_data[j5_bluescore_index]
            kd_red = this_round_scores_data[kd_red_index]
            kd_blue = this_round_scores_data[kd_blue_index]
            warn_red = this_round_scores_data[warn_red_index]
            warn_blue = this_round_scores_data[warn_blue_index]

            # This structure is used to combine the individual judges scores into one (round)list
            if data_format=="5-of-5J":
                this_round_scores = \
                    [j1_redscore,j1_bluescore,  #0, 1
                    j2_redscore,j2_bluescore,   #2, 3
                    j3_redscore,j3_bluescore,   #4, 5
                    j4_redscore,j4_bluescore,   #6, 7
                    j5_redscore,j5_bluescore,   #8, 9
                    kd_red, kd_blue,            #10, 11
                    warn_red,warn_blue,         #12, 13
                    j1_redscore,j1_bluescore, # ix1  #14, 15
                    j2_redscore,j2_bluescore, # ix2  #16, 17
                    j3_redscore,j3_bluescore, # ix3  #18, 19
                    j4_redscore,j4_bluescore, # ix4  #20, 21
                    j5_redscore,j5_bluescore] # ix5  #22, 23

                #print("\nRound %d:\n The scores string: %s" % (this_round_number+1, this_round_scores_data))
                printing("\nRound %d:" % (this_round_number+1), eventlog)

            elif data_format == "3-of-5J":
                this_round_scores = \
                    [j1_redscore,j1_bluescore,  #0, 1
                    j2_redscore,j2_bluescore,   #2, 3
                    j3_redscore,j3_bluescore,   #4, 5
                    j4_redscore,j4_bluescore,   #6, 7
                    j5_redscore,j5_bluescore,   #8, 9
                    kd_red, kd_blue,            #10, 11
                    warn_red,warn_blue,         #12, 13
                    0,0, # ix1                  #14, 15
                    0,0, # ix2                  #16, 17
                    0,0, # ix3                  #18, 19
                     -4,-4, # ix4 not used      #20, 21
                     -5,-5] # ix5 not used      #22, 23

                #print("\nRound %d's five scores were: %s" % (this_round_number+1, this_round_scores))

                ix1_data = int(this_round_scores_data[ix1_index]); # print(" -- ix1 is: ",ix1_data);
                ix2_data = int(this_round_scores_data[ix2_index]); # print(" -- ix2 is: ",ix2_data);
                ix3_data = int(this_round_scores_data[ix3_index]); # print(" -- ix3 is: ",ix3_data);

                printing("\nRound %d:\n -- The 3 Judges used: J%d, J%d and J%d\n" %
                         (this_round_number+1,ix1_data, ix2_data, ix3_data), eventlog)

                # ix1_scores: copy scores to ix1
                if ix1_data == 1:
                    this_round_scores[14:16] = this_round_scores[0:2]
                elif ix1_data == 2:
                    this_round_scores[14:16] = this_round_scores[2:4]
                elif ix1_data == 3:
                    this_round_scores[14:16] = this_round_scores[4:6]
                elif ix1_data == 4:
                    this_round_scores[14:16] = this_round_scores[6:8]
                elif ix1_data == 5:
                    this_round_scores[14:16] = this_round_scores[8:10]

                # ix2_scores: copy scores to ix2
                if ix2_data == 1:
                    this_round_scores[16:18] = this_round_scores[0:2]
                elif ix2_data == 2:
                    this_round_scores[16:18] = this_round_scores[2:4]
                elif ix2_data == 3:
                    this_round_scores[16:18] = this_round_scores[4:6]
                elif ix2_data == 4:
                    this_round_scores[16:18] = this_round_scores[6:8]
                elif ix2_data == 5:
                    this_round_scores[16:18] = this_round_scores[8:10]

                # ix3_scores: copy scores to ix3
                if ix3_data == 1:
                    this_round_scores[18:20] = this_round_scores[0:2]
                elif ix3_data == 2:
                    this_round_scores[18:20] = this_round_scores[2:4]
                elif ix3_data == 3:
                    this_round_scores[18:20] = this_round_scores[4:6]
                elif ix3_data == 4:
                    this_round_scores[18:20] = this_round_scores[6:8]
                elif ix3_data == 5:
                    this_round_scores[18:20] = this_round_scores[8:10]

            # this FOR loop iterates through this_round_scores to
            # add-in zeros where data is blank.
            for value_index in range (0,len(this_round_scores)):
                if this_round_scores[value_index] =="":# blank field
                    this_round_scores[value_index]="0"

            # Convert this_round_scores into a string
            this_round_scores_string = ';'.join(str(score) for score in this_round_scores)
            printing(" -- The scores string: %s" % (this_round_scores_string),eventlog)

            # compile the scores from ALL the rounds in the bout as one long string
            this_bout_scores_string = this_bout_scores_string + this_round_scores_string + ";"

        # the [:-1] at the end is to remove the extra " ; " char from the string
        # which was added during "this_bout_scores" string compile above
        this_bout_scores_string = this_bout_scores_string[:-1]
        printing("\n\nThis bout's overall scores string is:\n -- " + this_bout_scores_string, eventlog)

        # Declare a dictionary to use to retrieve the winner's name
        opponents = {"1": red_boxer_name, "2": blue_boxer_name}

        # this extracts the winner:  1= red boxer, 2= blue boxer
        winner_name = opponents.get(winner_data, "Default: No winner")
        printing("\n\nResult:\n -- Winner: %s\n -- Decision: %s\n -- Round: %d" %
                 (winner_name,result_data,number_of_rounds), eventlog)

    # close the input CP file
    cp_file_input.close()

# ADD RECORD TO EVENT CSV FILES
###############################################################################################################################
    if combPoints_exists:
        printing("\n\nDatafile processed, bout data extracted...",eventlog)

        # update data tables here
        with open(bouts_logpath, "a+") as bouts_data_table:
            bouts_data_table.write("\n"+str(current_log_number)
                                          +";"+ competition_name
                                          +";"+ competition_firstday
                                          +";"+ competition_lastday
                                          +";"+ competition_venue
                                          +";"+ competition_session_num
                                          +";"+ competition_session_name
                                          +";"+ competition_bout_date
                                          +";"+ competition_bout_time
                                          +";"+ competition_bout_number
                                          +";"+ competition_bout_weight_class
                                          +";"+ competition_bout_weight
                                          +";"+ competition_bout_gender
                                          +";"+ competition_bout_groupname
                                          +";"+red_boxer_name
                                          +";"+red_club
                                          +";"+blue_boxer_name
                                          +";"+blue_club
                                          +";"+referee_name+";"+referee_nat
                                          +";"+judge1_name+";"+judge1_nat
                                          +";"+judge2_name+";"+judge2_nat
                                          +";"+judge3_name+";"+judge3_nat
                                          +";"+judge4_name+";"+judge4_nat
                                          +";"+judge5_name+";"+judge5_nat
                                          +";"+ data_format
                                          +";"+ str(number_of_rounds)
                                          +";"+ result_data
                                          +";"+winner_name
                                          )
            printing("\n -- Bouts data table updated: " + bouts_logpath, eventlog)
        with open(boxers_logpath, "a+") as boxers_data_table:
            boxers_data_table.write("\n"+str(current_log_number)
                                    +";"+red_boxer_name
                                    +";"+red_club
                                    +";"+blue_boxer_name
                                    +";"+blue_club
                                    +";"+winner_name)
            printing("\n -- Boxers data table updated: " + boxers_logpath, eventlog)
        with open(officials_logpath, "a+") as officials_data_table:
            officials_data_table.write("\n"+str(current_log_number)
                                    +";"+referee_name+";"+referee_nat
                                    +";"+judge1_name+";"+judge1_nat
                                    +";"+judge2_name+";"+judge2_nat
                                    +";"+judge3_name+";"+judge3_nat
                                    +";"+judge4_name+";"+judge4_nat
                                    +";"+judge5_name+";"+judge5_nat
                                    )
            printing("\n -- Officials data table updated: " + officials_logpath, eventlog)
        with open(boutscores_logpath, "a+") as boutscores_data_table:
            boutscores_data_table.write("\n"+ str(current_log_number)
                                        + ";" + this_bout_scores_string
                                        )
            printing("\n -- Boutscores data table updated: " + boutscores_logpath, eventlog)

        # UPDATE THE PROCESS LOG FILE
        current_log_string = str(current_log_number)+";"\
                             +str(datapath) + ";"\
                             + str(filename)+ ";"\
                             +str(date_input_cp_file_was_created)+";"\
                             + str(now.strftime("%d-%m-%Y @ %H:%M"))

        with open('C:/_project/log/process_data.log', 'a+') as processlog:
            processlog.write("\n"+str(current_log_string))
            #printing("\n\nThis string has been added to the process log:\n"+current_log_string, eventlog)
            printing("\n\nProcess log updated...\n -- " + current_log_string, eventlog)
    else:
        number_of_cp_files -= 1
        file_errors +=1
        last_log_number_created -= 1
        current_log_string = "Check CP file: " + str(datapath) + "/" + str(filename)
        printing("\nError: Process log NOT updated..."+"\n -- "+current_log_string, eventlog)


# Create WHITESPACE for clarity when displaying output in console
###############################################################################################################################
    printing(("\n" + ("*" * 130))*2, eventlog)
# *****************************************************************
    # create single array with all event data
    # CURRENTLY NOT USED
    event_data.append(cp_file_sections)
# *****************************************************************


# CLOSE PROCESS LOG NOW - AT END OF DATA CAPTURE PROCESS
# close method not necessary now since file manager open method is now used
########################################################################################################################
#processlog.close()
# *****************************************************************


# OUTPUT MESSAGES TO SCREEN TO INDICATE DATA CAPTURE PROCESS COMPLETE
########################################################################################################################
printing("\n\nTotal files processed correctly: " + str(number_of_cp_files), eventlog)
printing("\nTotal files processed with errors: " + str(file_errors), eventlog)
printing("\nLast file processed was: " + filename, eventlog)
printing("\nLast process log entry (no errors only):\n -- " + current_log_string, eventlog)
# *****************************************************************
printing(("\n" + ("*" * 130))*2, eventlog)
eventlog.close()
file_dialog_root.destroy()
progressbar_root.destroy()

