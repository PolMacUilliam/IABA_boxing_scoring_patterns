###############################################################################################################
# Filename: dB_dataFile_compiler.py
# Author: Paul Williamson
# Date: 08/09/2017
###############################################################################################################
# IMPORT MODULES HERE
###############################################################################################################
import glob
import sys
import time
import os
import datetime
import time
import tkinter
from tkinter import filedialog
import random
# Get current date
now = datetime.datetime.now()


###############################################################################################################
# DECLARE FUNCTIONS
###############################################################################################################
def returnNotMatches(old_version, new_version):
    return [x for x in new_version if x not in old_version]

def printing(text,fileobject):
    print(text)
    fileobject.write(text)

###############################################################################################################
# PICK DATALOG FOLDER
###############################################################################################################
#  Get user to pick data folder i.e. folder holding all the CP files to be processed
root = tkinter.Tk()
root.withdraw()
datapath=filedialog.askdirectory(title="Select DATALOG folder with CSV datalog files...")
root.destroy()
if not datapath:
    sys.exit("You cancelled!!!") # handle dialog cancel event


###############################################################################################################
# GET DATALOG FOLDER CONTENTS AS A LIST
###############################################################################################################
datalog_directory_listing = glob.glob(datapath + '/*_table.csv')

# FIND THE TOTAL NUMBER OF CSV DATALOG FILES IN THE DATALOG FOLDER
number_of_datalog_csv_files_found = len(datalog_directory_listing)

if number_of_datalog_csv_files_found != 4: # Need all 4 datalog files to compile dB data files
    sys.exit("Incorrect number of datalog files found..."
             "\nSorry, this event cannot be added to the dBase at this time."
             "\nGOODBYE!") # handle incorrect number CSV files
else:
    event_db_log=open(datapath + '/event_db_log.txt','w')
    printing("\nThere was " + str( number_of_datalog_csv_files_found) + " datalog files found as follows:" ,event_db_log)
    for datalog_file_no in range(0,number_of_datalog_csv_files_found):
        printing( "\n -- " + str(datalog_file_no) + "  " + datalog_directory_listing[datalog_file_no], event_db_log)
    printing("\n\nProceeding...\n",event_db_log)

# DECLARE TEMPORARY VARIABLES TO HOLD DBASE RECORDS
list_of_dbase_competition_names=[]
list_of_dbase_boxers_names=[]
list_of_dbase_officials_names=[]
list_of_dbase_bout_numbers=[]
list_of_dbase_boutscores_numbers=[]





###############################################################################################################
# OPEN THE DATABASE FILE "COMPETITION_DBASE_TABLE.CSV" IN THE PROCESS_LOG FOLDER
###############################################################################################################
with open("C:/_project/log/competition_dbase_table.csv","r+") as competition_dbase_table:
    list_of_records_from_competition_dbase_table = competition_dbase_table.readlines()

    # get log number of last record added to dbase
    last_log_number_created = int(list_of_records_from_competition_dbase_table[-1].split(";")[0])
    # strip column headings & dummy record
    list_of_records_from_competition_dbase_table = list_of_records_from_competition_dbase_table[2:]

    #print("\nThe last 'competition_dbase_table' record in DATABASE is: %s."%last_log_number_created) # display last log number

number_of_dbase_competition_records = len(list_of_records_from_competition_dbase_table)
printing("\nCOMPETITIONS: Number of competitions by name currently in database: " + str(number_of_dbase_competition_records) + "\n" + "-"*50, event_db_log)

# get list of all DATABASE competition name records.
for competition_index in range (0,number_of_dbase_competition_records):
    dbase_current_record = list_of_records_from_competition_dbase_table[competition_index].rstrip("\n").split(";" )[1]
    #print(str(competition_index+1) + ": " + dbase_current_record) # display current list
    list_of_dbase_competition_names.append(dbase_current_record) # create temp list to hold current dbase list

# get current state of list for comparison later
current_list = list_of_dbase_competition_names[:]

################################################################################################################
# OPEN "COMPETITION_DATALOG_TABLE.CSV" IN THE CURRENT EVENT'S DATALOG FOLDER
################################################################################################################
with open(datalog_directory_listing[1]) as competition_data_table: # bouts_data_table file
    all_records_from_competitions_data_file = competition_data_table.readlines()

number_of_datalog_competition_records = len(all_records_from_competitions_data_file)
for competition_index in range(1,number_of_datalog_competition_records):
    # range starts at 1 because line 0 has all the column names

    # get all event names from the "bouts_data_table.csv" in the current event's DATALOG folder
    datalog_current_record = all_records_from_competitions_data_file[competition_index].rstrip("\n").split(";" )

    # get info for current event
    current_competition_name = datalog_current_record[1]
    current_startdate = datalog_current_record[2]
    current_enddate = datalog_current_record[3]
    current_venue = datalog_current_record[4]

    # check if current competition is already in dbase, if it is pass
    if current_competition_name in list_of_dbase_competition_names:
        pass
    # if current competition is not in dbase, add it
    else:
        current_log_number = last_log_number_created+1
        last_log_number_created+=1
        list_of_dbase_competition_names.append(current_competition_name)

        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/competition_dbase_table.csv","a+") as competition_dbase_table:
            competition_dbase_table.write("\n"+str(current_log_number)
                                            +";"+current_competition_name
                                            +";"+current_venue
                                            +";"+current_startdate
                                            +";"+current_enddate)

        # ************ THIS IS WHERE THIS RECORD CAN BE ADDED INTO THE DBASE ************ #

# get current state of list now to see if anything has changed
updated_list = list_of_dbase_competition_names[:]

# compare current list with updated list
newly_added = returnNotMatches(current_list,updated_list)
if newly_added != []:
    printing("\nAdded following competitions:",event_db_log)
    for index in range(0,len(newly_added)):
        printing("\n -- " + newly_added[index] + "\n", event_db_log)
else:
    printing("\n -- NO NEW COMPETITIONS ADDED.", event_db_log)
    #printing("\nNumber of Database records is: " + str(len(updated_list)), event_db_log)





###############################################################################################################
# OPEN THE DATABASE FILE "BOXERS_DBASE_TABLE.CSV" IN THE PROCESS_LOG FOLDER
###############################################################################################################
with open("C:/_project/log/boxers_dbase_table.csv","r+") as boxers_dbase_table:
    list_of_records_from_boxers_dbase_table = boxers_dbase_table.readlines()

    # get log number of last record added to dbase
    last_log_number_created = int(list_of_records_from_boxers_dbase_table[-1].split(";")[0])
    # strip column headings and dummy record
    list_of_records_from_boxers_dbase_table = list_of_records_from_boxers_dbase_table[2:]

    #print("\nThe last 'boxers_dbase_table' record  in DATABASE is: %s."%last_log_number_created)

number_of_dbase_boxer_records = len(list_of_records_from_boxers_dbase_table)
printing("\n\nBOXERS: Number of boxers by name currently in database: " + str(number_of_dbase_boxer_records) + "\n" + "-"*50, event_db_log)

# get list of all DATABASE boxers name records.
for boxer_index in range (0,number_of_dbase_boxer_records):
    dbase_current_record = list_of_records_from_boxers_dbase_table[boxer_index].rstrip("\n").split(";")[1]
    list_of_dbase_boxers_names.append(dbase_current_record) # create temp list to hold current dbase list

# get current state of list for comparison later
current_list = list_of_dbase_boxers_names[:]

###############################################################################################################
# OPEN "BOXERS_DATALOG_TABLE.CSV" IN THE CURRENT EVENT'S DATALOG FOLDER
###############################################################################################################
with open(datalog_directory_listing[2]) as boxers_data_table:
    all_records_from_boxers_data_file = boxers_data_table.readlines()

number_of_datalog_boxer_records = len(all_records_from_boxers_data_file)
for this_boxer_record in range(1,number_of_datalog_boxer_records):
    # range starts at 1 because line 0 has all the column names
    # get all boxers names from the "boxers_data_table.csv" in the current event's DATALOG folder
    datalog_current_record = all_records_from_boxers_data_file[this_boxer_record].rstrip("\n").split(";" )

    # get info for boxers in current record
    redboxer = datalog_current_record[1]
    redclub = datalog_current_record[2]
    blueboxer = datalog_current_record[3]
    blueclub = datalog_current_record[4]

    # check if current red boxer is already in dbase
    if redboxer in list_of_dbase_boxers_names:
        pass
    # if current red boxer is not in dbase add it
    else:
        current_log_number = last_log_number_created+1
        last_log_number_created+=1
        list_of_dbase_boxers_names.append(redboxer)

        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/boxers_dbase_table.csv","a+") as boxers_dbase_table:
            boxers_dbase_table.write("\n"+str(current_log_number)
                                              +";"+redboxer
                                              +";"+redclub)

            # ************ THIS IS WHERE THIS RECORD CAN BE ADDED INTO THE DBASE ************ #

    # check if current blue boxer is already in dbase
    if blueboxer in list_of_dbase_boxers_names:
        pass
    # if current blue boxer is not in dbase add it
    else:
        current_log_number = last_log_number_created+1
        last_log_number_created+=1
        list_of_dbase_boxers_names.append(blueboxer)

        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/boxers_dbase_table.csv","a+") as boxers_dbase_table:
            boxers_dbase_table.write("\n"+str(current_log_number)
                                              +";"+blueboxer
                                              +";"+blueclub)
            # ************ THIS IS WHERE THIS RECORD CAN BE ADDED INTO THE DBASE ************ #

# get current state of list now to see if anything has changed
updated_list = list_of_dbase_boxers_names[:]

# compare current list with updated list
newly_added = returnNotMatches(current_list,updated_list)
if newly_added != []:
    printing("\nAdded following boxers:", event_db_log)
    for index in range(0,len(newly_added)):
        printing("\n -- " + newly_added[index], event_db_log)
else:
    printing("\n -- NO NEW BOXERS ADDED.", event_db_log)
    # printing("\nNumber of Database records is: " + str(len(updated_list)), event_db_log)





###############################################################################################################
# OPEN THE DATABASE FILE "OFFICIALS_DBASE_TABLE.CSV" IN THE PROCESS_LOG FOLDER
###############################################################################################################
with open("C:/_project/log/officials_dbase_table.csv","r+") as officials_dbase_table:
    list_of_records_from_officials_dbase_table = officials_dbase_table.readlines()

    # get log number of last record added to dbase
    last_log_number_created = int(list_of_records_from_officials_dbase_table[-1].split(";")[0])
    # strip column headings and dummy record
    list_of_records_from_officials_dbase_table = list_of_records_from_officials_dbase_table[2:]

    #print("\nThe last 'officials_dbase_table' record  previously created was: %s."%last_log_number_created) # display number of records

number_of_dbase_official_records=len(list_of_records_from_officials_dbase_table)
printing("\n\nOFFICIALS: Number of officials by name currently in database: " + str(number_of_dbase_official_records) + "\n" + "-"*50, event_db_log)

# GET full DATABASE list of all officials name records range starts at 1 because line 0 has all the column names
for officials_record in range (0,number_of_dbase_official_records):
    dbase_current_record = list_of_records_from_officials_dbase_table[officials_record].rstrip("\n").split(";")[1]
    list_of_dbase_officials_names.append(dbase_current_record) # create temp list to hold current dbase list

# get current state of list for comparison later
current_list = list_of_dbase_officials_names[:]

###############################################################################################################
# OPEN "OFFICIALS_DATALOG_TABLE.CSV" IN THE CURRENT EVENT'S DATALOG FOLDER
###############################################################################################################
with open(datalog_directory_listing[3]) as officials_data_table:
    all_records_from_officials_data_file = officials_data_table.readlines()

number_of_datalog_officials_records = len(all_records_from_officials_data_file)
for this_bout_record in range(1,number_of_datalog_officials_records):
    # range starts at 1 because line 0 has all the column names
    # get all officials names from the "officials_data_table.csv" in the current event's DATALOG folder
    datalog_current_record = all_records_from_officials_data_file[this_bout_record].rstrip("\n").split(";" )

    # get info for officials in current record
    referee = datalog_current_record[1]
    refereeclub = datalog_current_record[2]
    judge1 = datalog_current_record[3]
    judge1club = datalog_current_record[4]
    judge2 = datalog_current_record[5]
    judge2club = datalog_current_record[6]
    judge3 = datalog_current_record[7]
    judge3club = datalog_current_record[8]
    judge4 = datalog_current_record[9]
    judge4club = datalog_current_record[10]
    judge5 = datalog_current_record[11]
    judge5club = datalog_current_record[12]

    if referee in list_of_dbase_officials_names:
        pass
    else:
        current_log_number = last_log_number_created+1
        last_log_number_created+=1
        list_of_dbase_officials_names.append(referee)

        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/officials_dbase_table.csv","a+") as officials_dbase_table:
            officials_dbase_table.write("\n"+str(current_log_number)
                                              +";"+referee
                                              +";"+refereeclub)

# ************ THIS IS WHERE THIS RECORD CAN BE ADDED INTO THE DBASE ************ #

    if judge1 in list_of_dbase_officials_names:
        pass
    else:
        current_log_number = last_log_number_created+1
        last_log_number_created+=1
        list_of_dbase_officials_names.append(judge1)

        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/officials_dbase_table.csv","a+") as officials_dbase_table:
            officials_dbase_table.write("\n"+str(current_log_number)
                                              +";"+judge1
                                              +";"+judge1club)

# ************ THIS IS WHERE THIS RECORD CAN BE ADDED INTO THE DBASE ************ #

    if judge2 in list_of_dbase_officials_names:
        pass
    else:
        current_log_number = last_log_number_created+1
        last_log_number_created+=1
        list_of_dbase_officials_names.append(judge2)

        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/officials_dbase_table.csv","a+") as officials_dbase_table:
            officials_dbase_table.write("\n"+str(current_log_number)
                                              +";"+judge2
                                              +";"+judge2club)

# ************ THIS IS WHERE THIS RECORD CAN BE ADDED INTO THE DBASE ************ #

    if judge3 in list_of_dbase_officials_names:
        pass
    else:
        current_log_number = last_log_number_created+1
        last_log_number_created+=1
        list_of_dbase_officials_names.append(judge3)

        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/officials_dbase_table.csv","a+") as officials_dbase_table:
            officials_dbase_table.write("\n"+str(current_log_number)
                                              +";"+judge3
                                              +";"+judge3club)

# ************ THIS IS WHERE THIS RECORD CAN BE ADDED INTO THE DBASE ************ #

    if judge4 in list_of_dbase_officials_names:
        pass
    else:
        current_log_number = last_log_number_created+1
        last_log_number_created+=1
        list_of_dbase_officials_names.append(judge4)

        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/officials_dbase_table.csv","a+") as officials_dbase_table:
            officials_dbase_table.write("\n"+str(current_log_number)
                                              +";"+judge4
                                              +";"+judge4club)

# ************ THIS IS WHERE THIS RECORD CAN BE ADDED INTO THE DBASE ************ #

    if judge5 in list_of_dbase_officials_names:
        pass
    else:
        current_log_number = last_log_number_created+1
        last_log_number_created+=1
        list_of_dbase_officials_names.append(judge5)

        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/officials_dbase_table.csv","a+") as officials_dbase_table:
            officials_dbase_table.write("\n"+str(current_log_number)
                                              +";"+judge5
                                              +";"+judge5club)

# get current state of list now to see if anything has changed
updated_list = list_of_dbase_officials_names[:]

# compare current list with updated list
newly_added = returnNotMatches(current_list,updated_list)
if newly_added != []:
    printing("\nAdded following officials:", event_db_log)
    for index in range(0,len(newly_added)):
        printing("\n -- " + newly_added[index], event_db_log)
else:
    printing("\n -- NO NEW OFFICIALS ADDED.", event_db_log)
    #printing("Number of Database records is: " + str(len(updated_list)), event_db_log)





###############################################################################################################
# OPEN THE DATABASE FILE "BOUTS_DBASE_TABLE.CSV" IN THE PROCESS_LOG FOLDER
###############################################################################################################
with open("C:/_project/log/bouts_dbase_table.csv","r+") as bouts_dbase_table:
    list_of_records_from_bouts_dbase_table = bouts_dbase_table.readlines()
    list_of_records_from_bouts_dbase_table = list_of_records_from_bouts_dbase_table[1:] # strip column headings
    #print("Current list_of_records_from_bouts_dbase_table:\n",list_of_records_from_bouts_dbase_table)

    # get log number of last record added to dbase
    last_log_number_created = int(list_of_records_from_bouts_dbase_table[-1].split(";")[0])

    list_of_records_from_bouts_dbase_table = list_of_records_from_bouts_dbase_table[1:] # strip dummy line

number_of_dbase_bouts_records=len(list_of_records_from_bouts_dbase_table)
printing("\n\nBOUTS: Number of bouts currently recorded in database: " + str(number_of_dbase_bouts_records) + "\n" + "-"*50, event_db_log)

# GET full DATABASE list of all bouts' log number records
for bout_record in range (0,number_of_dbase_bouts_records):
    dbase_current_record = list_of_records_from_bouts_dbase_table[bout_record].rstrip("\n").split(";")
    list_of_dbase_bout_numbers.append(dbase_current_record[0]) # create temp list to hold current dbase list

# get current state of list for comparison later
current_list = list_of_dbase_bout_numbers[:]
#print(current_list)

###############################################################################################################
# OPEN "BOUTS_DATALOG_TABLE.CSV" IN THE CURRENT EVENT'S DATALOG FOLDER
###############################################################################################################
with open(datalog_directory_listing[1]) as bouts_data_table: # bouts_data file
    all_new_records_from_bouts_data_file = bouts_data_table.readlines()

number_of_new_datalog_bouts_records = len(all_new_records_from_bouts_data_file) # exclude column headings
#print("Number of possible new bouts: ",number_of_new_datalog_bouts_records)
for this_bout_record in range(1,number_of_new_datalog_bouts_records):
    # range starts at 1 because line 0 has all the column names
    # get all bouts from the "bouts_data_table.csv" in the current event's DATALOG folder
    datalog_current_record = all_new_records_from_bouts_data_file[this_bout_record].rstrip("\n")

    # get info for current record
    datalog_current_record=datalog_current_record.split(";")
    current_bout_log_number = datalog_current_record[0]

    if current_bout_log_number in list_of_dbase_bout_numbers:
        pass
    else:
        list_of_dbase_bout_numbers.append(current_bout_log_number)              #0
        current_bout_competition_name = datalog_current_record[1]               #1
        current_bout_competition_session_num = datalog_current_record[5]        #2
        current_bout_competition_session_name = datalog_current_record[6]       #3
        current_bout_competition_bout_date = datalog_current_record[7]          #4
        current_bout_competition_bout_time = datalog_current_record[8]          #5
        current_bout_competition_bout_number = datalog_current_record[9]        #6
        current_bout_competition_bout_weight_class = datalog_current_record[10] #7
        current_bout_competition_bout_weight_KG = datalog_current_record[11]    #8
        current_bout_competition_bout_gender = datalog_current_record[12]       #9
        current_bout_competition_bout_groupname = datalog_current_record[13]    #10
        current_bout_red_boxer_name = datalog_current_record[14]                #11
        current_bout_red_club = datalog_current_record[15]                      #12
        current_bout_blue_boxer_name = datalog_current_record[16]               #13
        current_bout_blue_club = datalog_current_record[17]                     #14
        current_bout_referee_name = datalog_current_record[18]                  #15
        current_bout_referee_nat = datalog_current_record[19]                   #16
        current_bout_judge1_name = datalog_current_record[20]                   #17
        current_bout_judge1_nat = datalog_current_record[21]                    #18
        current_bout_judge2_name = datalog_current_record[22]                   #19
        current_bout_judge2_nat = datalog_current_record[23]                    #20
        current_bout_judge3_name = datalog_current_record[24]                   #21
        current_bout_judge3_nat = datalog_current_record[25]                    #22
        current_bout_judge4_name = datalog_current_record[26]                   #23
        current_bout_judge4_nat = datalog_current_record[27]                    #24
        current_bout_judge5_name = datalog_current_record[28]                   #25
        current_bout_judge5_nat = datalog_current_record[29]                    #26
        current_bout_data_format = datalog_current_record[30]                   #27
        current_bout_number_of_rounds = datalog_current_record[31]              #28
        current_bout_result_text = datalog_current_record[32]                   #29
        current_bout_winner = datalog_current_record[33]                        #30

        datalog_current_record = str(current_bout_log_number)+";"\
                                 + str(current_bout_competition_name)+";"\
                                 + str(current_bout_competition_session_num)+";"\
                                 + str(current_bout_competition_session_name)+";"\
                                 + str(current_bout_competition_bout_date)+";"\
                                 + str(current_bout_competition_bout_time)+";"\
                                 + str(current_bout_competition_bout_number)+";"\
                                 + str(current_bout_competition_bout_weight_class)+";"\
                                 + str(current_bout_competition_bout_weight_KG)+";"\
                                 + str(current_bout_competition_bout_gender)+";"\
                                 + str(current_bout_competition_bout_groupname)+";"\
                                 + str(current_bout_red_boxer_name)+";"\
                                 + str(current_bout_red_club)+";"\
                                 + str(current_bout_blue_boxer_name)+";"\
                                 + str(current_bout_blue_club)+";"\
                                 + str(current_bout_referee_name)+";"\
                                 + str(current_bout_referee_nat)+";"\
                                 + str(current_bout_judge1_name)+";"\
                                 + str(current_bout_judge1_nat)+";"\
                                 + str(current_bout_judge2_name)+";"\
                                 + str(current_bout_judge2_nat)+";"\
                                 + str(current_bout_judge3_name)+";"\
                                 + str(current_bout_judge3_nat)+";"\
                                 + str(current_bout_judge4_name)+";"\
                                 + str(current_bout_judge4_nat)+";"\
                                 + str(current_bout_judge5_name)+";"\
                                 + str(current_bout_judge5_nat)+";"\
                                 + str(current_bout_data_format)+";"\
                                 + str(current_bout_number_of_rounds)+";"\
                                 + str(current_bout_result_text)+";"\
                                 + str(current_bout_winner)
        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/bouts_dbase_table.csv","a+") as bouts_dbase_table:
            bouts_dbase_table.write("\n"+str(datalog_current_record))

# ************ THIS IS WHERE THIS RECORD CAN BE ADDED INTO THE DBASE ************ #

# get current state of list now to see if anything has changed
updated_list = list_of_dbase_bout_numbers[:]

# compare current list with updated list
newly_added = returnNotMatches(current_list,updated_list)
if newly_added != []:
    printing("\nAdded following bout lognums:", event_db_log)
    for index in range(0,len(newly_added)):
        printing("\n -- " + newly_added[index], event_db_log)
else:
    printing("\n -- NO NEW BOUTS ADDED.", event_db_log)
    # print("\nNumber of Database records is: " + str(len(updated_list)),event_db_log)






###############################################################################################################
# OPEN THE DATABASE FILE "BOUTSCORES_DBASE_TABLE.CSV" IN THE PROCESS_LOG FOLDER
###############################################################################################################
with open("C:/_project/log/boutscores_dbase_table.csv","r+") as boutscores_dbase_table:
    list_of_records_from_boutscores_dbase_table = boutscores_dbase_table.readlines()
    list_of_records_from_boutscores_dbase_table = list_of_records_from_boutscores_dbase_table[1:] # strip column headings
    #print("Current list_of_records_from_boutscores_dbase_table:\n",list_of_records_from_boutscores_dbase_table)

    # get log number of last record added to dbase
    last_log_number_created = int(list_of_records_from_boutscores_dbase_table[-1].split(";")[0])

    list_of_records_from_boutscores_dbase_table = list_of_records_from_boutscores_dbase_table[1:] # strip dummy line

number_of_dbase_boutscores_records=len(list_of_records_from_boutscores_dbase_table)
printing("\n\nBOUTSCORES: Number of boutscores currently recorded in database: " + str(number_of_dbase_boutscores_records) + "\n" + "-"*50, event_db_log)

# GET full DATABASE list of all bouts' log number records
for bout_record in range (0,number_of_dbase_boutscores_records):
    dbase_current_record = list_of_records_from_boutscores_dbase_table[bout_record].rstrip("\n").split(";")
    list_of_dbase_boutscores_numbers.append(dbase_current_record[0]) # create temp list to hold current dbase list

# get current state of list for comparison later
current_list = list_of_dbase_boutscores_numbers[:]
#print(current_list)

###############################################################################################################
# OPEN "BOUTSCORES_DATALOG_TABLE.CSV" IN THE CURRENT EVENT'S DATALOG FOLDER
###############################################################################################################
with open(datalog_directory_listing[0]) as boutscores_data_table: # bouts_data file
    all_new_records_from_boutscores_data_file = boutscores_data_table.readlines()

number_of_new_datalog_boutscores_records = len(all_new_records_from_boutscores_data_file) # exclude column headings
#print("Number of possible new bouts: ",number_of_new_datalog_bouts_records)
for this_bout_record in range(1,number_of_new_datalog_boutscores_records):
    # range starts at 1 because line 0 has all the column names
    # get all bouts from the "bouts_data_table.csv" in the current event's DATALOG folder
    datalog_current_record = all_new_records_from_boutscores_data_file[this_bout_record].rstrip("\n")

    # get info for current record
    datalog_current_record=datalog_current_record.split(";")
    current_bout_log_number = datalog_current_record[0]

    current_bout_J1r1 = 0
    current_bout_J1b1 = 0
    current_bout_J2r1 = 0
    current_bout_J2b1 = 0
    current_bout_J3r1 = 0
    current_bout_J3b1 = 0
    current_bout_J4r1 = 0
    current_bout_J4b1 = 0
    current_bout_J5r1 = 0
    current_bout_J5b1 = 0
    current_bout_kdr1 = 0
    current_bout_kdb1 = 0
    current_bout_wr1 = 0
    current_bout_wb1 = 0
    current_bout_ix1r1 = 0
    current_bout_ix1b1 = 0
    current_bout_ix2r1 = 0
    current_bout_ix2b1 = 0
    current_bout_ix3r1 = 0
    current_bout_ix3b1 = 0
    current_bout_ix4r1 = 0
    current_bout_ix4b1 = 0
    current_bout_ix5r1 = 0
    current_bout_ix5b1 = 0

    current_bout_J1r2 = 0
    current_bout_J1b2 = 0
    current_bout_J2r2 = 0
    current_bout_J2b2 = 0
    current_bout_J3r2 = 0
    current_bout_J3b2 = 0
    current_bout_J4r2 = 0
    current_bout_J4b2 = 0
    current_bout_J5r2 = 0
    current_bout_J5b2 = 0
    current_bout_kdr2 = 0
    current_bout_kdb2 = 0
    current_bout_wr2 = 0
    current_bout_wb2 = 0
    current_bout_ix1r2 = 0
    current_bout_ix1b2 = 0
    current_bout_ix2r2 = 0
    current_bout_ix2b2 = 0
    current_bout_ix3r2 = 0
    current_bout_ix3b2 = 0
    current_bout_ix4r2 = 0
    current_bout_ix4b2 = 0
    current_bout_ix5r2 = 0
    current_bout_ix5b2 = 0

    current_bout_J1r3 = 0
    current_bout_J1b3 = 0
    current_bout_J2r3 = 0
    current_bout_J2b3 = 0
    current_bout_J3r3 = 0
    current_bout_J3b3 = 0
    current_bout_J4r3 = 0
    current_bout_J4b3 = 0
    current_bout_J5r3 = 0
    current_bout_J5b3 = 0
    current_bout_kdr3 = 0
    current_bout_kdb3 = 0
    current_bout_wr3 = 0
    current_bout_wb3 = 0
    current_bout_ix1r3 = 0
    current_bout_ix1b3 = 0
    current_bout_ix2r3 = 0
    current_bout_ix2b3 = 0
    current_bout_ix3r3 = 0
    current_bout_ix3b3 = 0
    current_bout_ix4r3 = 0
    current_bout_ix4b3 = 0
    current_bout_ix5r3 = 0
    current_bout_ix5b3 = 0

    current_bout_J1r4 = 0
    current_bout_J1b4 = 0
    current_bout_J2r4 = 0
    current_bout_J2b4 = 0
    current_bout_J3r4 = 0
    current_bout_J3b4 = 0
    current_bout_J4r4 = 0
    current_bout_J4b4 = 0
    current_bout_J5r4 = 0
    current_bout_J5b4 = 0
    current_bout_kdr4 = 0
    current_bout_kdb4 = 0
    current_bout_wr4 = 0
    current_bout_wb4 = 0
    current_bout_ix1r4 = 0
    current_bout_ix1b4 = 0
    current_bout_ix2r4 = 0
    current_bout_ix2b4 = 0
    current_bout_ix3r4 = 0
    current_bout_ix3b4 = 0
    current_bout_ix4r4 = 0
    current_bout_ix4b4 = 0
    current_bout_ix5r4 = 0
    current_bout_ix5b4 = 0

    if current_bout_log_number in list_of_dbase_boutscores_numbers:
        pass # already in dbase so do nothing
    else:
        list_of_dbase_boutscores_numbers.append(current_bout_log_number)              #0
        if len(datalog_current_record)>=25:
            # round 1
            current_bout_J1r1 = datalog_current_record[1]           #1
            current_bout_J1b1 = datalog_current_record[2]           #2
            current_bout_J2r1 = datalog_current_record[3]           #3
            current_bout_J2b1 = datalog_current_record[4]           #4
            current_bout_J3r1 = datalog_current_record[5]           #5
            current_bout_J3b1 = datalog_current_record[6]           #6
            current_bout_J4r1 = datalog_current_record[7]           #7
            current_bout_J4b1 = datalog_current_record[8]           #8
            current_bout_J5r1 = datalog_current_record[9]           #9
            current_bout_J5b1 = datalog_current_record[10]          #10
            current_bout_kdr1 = datalog_current_record[11]          #11
            current_bout_kdb1 = datalog_current_record[12]          #12
            current_bout_wr1 = datalog_current_record[13]           #13
            current_bout_wb1 = datalog_current_record[14]           #14
            current_bout_ix1r1 = datalog_current_record[15]         #15
            current_bout_ix1b1 = datalog_current_record[16]         #16
            current_bout_ix2r1 = datalog_current_record[17]         #17
            current_bout_ix2b1 = datalog_current_record[18]         #18
            current_bout_ix3r1 = datalog_current_record[19]         #19
            current_bout_ix3b1 = datalog_current_record[20]         #20
            current_bout_ix4r1 = datalog_current_record[21]         #21
            current_bout_ix4b1 = datalog_current_record[22]         #22
            current_bout_ix5r1 = datalog_current_record[23]         #23
            current_bout_ix5b1 = datalog_current_record[24]         #24

        if len(datalog_current_record)>=49:
            # round 2
            current_bout_J1r2 = datalog_current_record[25]          #25
            current_bout_J1b2 = datalog_current_record[26]          #26
            current_bout_J2r2 = datalog_current_record[27]          #27
            current_bout_J2b2 = datalog_current_record[28]          #28
            current_bout_J3r2 = datalog_current_record[29]          #29
            current_bout_J3b2 = datalog_current_record[30]          #30
            current_bout_J4r2 = datalog_current_record[31]
            current_bout_J4b2 = datalog_current_record[32]
            current_bout_J5r2 = datalog_current_record[33]
            current_bout_J5b2 = datalog_current_record[34]
            current_bout_kdr2 = datalog_current_record[35]
            current_bout_kdb2 = datalog_current_record[36]
            current_bout_wr2 = datalog_current_record[37]
            current_bout_wb2 = datalog_current_record[38]
            current_bout_ix1r2 = datalog_current_record[39]
            current_bout_ix1b2 = datalog_current_record[40]
            current_bout_ix2r2 = datalog_current_record[41]
            current_bout_ix2b2 = datalog_current_record[42]
            current_bout_ix3r2 = datalog_current_record[43]
            current_bout_ix3b2 = datalog_current_record[44]
            current_bout_ix4r2 = datalog_current_record[45]
            current_bout_ix4b2 = datalog_current_record[46]
            current_bout_ix5r2 = datalog_current_record[47]
            current_bout_ix5b2 = datalog_current_record[48]

        if len(datalog_current_record) >=73:
            # round 3
            current_bout_J1r3 = datalog_current_record[49]
            current_bout_J1b3 = datalog_current_record[50]
            current_bout_J2r3 = datalog_current_record[51]
            current_bout_J2b3 = datalog_current_record[52]
            current_bout_J3r3 = datalog_current_record[53]
            current_bout_J3b3 = datalog_current_record[54]
            current_bout_J4r3 = datalog_current_record[55]
            current_bout_J4b3 = datalog_current_record[56]
            current_bout_J5r3 = datalog_current_record[57]
            current_bout_J5b3 = datalog_current_record[58]
            current_bout_kdr3 = datalog_current_record[59]
            current_bout_kdb3 = datalog_current_record[60]
            current_bout_wr3 = datalog_current_record[61]
            current_bout_wb3 = datalog_current_record[62]
            current_bout_ix1r3 = datalog_current_record[63]
            current_bout_ix1b3 = datalog_current_record[64]
            current_bout_ix2r3 = datalog_current_record[65]
            current_bout_ix2b3 = datalog_current_record[66]
            current_bout_ix3r3 = datalog_current_record[67]
            current_bout_ix3b3 = datalog_current_record[68]
            current_bout_ix4r3 = datalog_current_record[69]
            current_bout_ix4b3 = datalog_current_record[70]
            current_bout_ix5r3 = datalog_current_record[71]
            current_bout_ix5b3 = datalog_current_record[72]

        if len(datalog_current_record) ==97:
            # round 4
            current_bout_J1r4 = datalog_current_record[73]
            current_bout_J1b4 = datalog_current_record[74]
            current_bout_J2r4 = datalog_current_record[75]
            current_bout_J2b4 = datalog_current_record[76]
            current_bout_J3r4 = datalog_current_record[77]
            current_bout_J3b4 = datalog_current_record[78]
            current_bout_J4r4 = datalog_current_record[79]
            current_bout_J4b4 = datalog_current_record[80]
            current_bout_J5r4 = datalog_current_record[81]
            current_bout_J5b4 = datalog_current_record[82]
            current_bout_kdr4 = datalog_current_record[83]
            current_bout_kdb4 = datalog_current_record[84]
            current_bout_wr4 = datalog_current_record[85]
            current_bout_wb4 = datalog_current_record[86]
            current_bout_ix1r4 = datalog_current_record[87]
            current_bout_ix1b4 = datalog_current_record[88]
            current_bout_ix2r4 = datalog_current_record[89]
            current_bout_ix2b4 = datalog_current_record[90]
            current_bout_ix3r4 = datalog_current_record[91]
            current_bout_ix3b4 = datalog_current_record[92]
            current_bout_ix4r4 = datalog_current_record[93]
            current_bout_ix4b4 = datalog_current_record[94]
            current_bout_ix5r4 = datalog_current_record[95]
            current_bout_ix5b4 = datalog_current_record[96]

        datalog_current_record = str(current_bout_log_number)+";"\
                                 + str(current_bout_J1r1)+";"\
								 + str(current_bout_J1b1)+";"\
								 + str(current_bout_J2r1)+";"\
								 + str(current_bout_J2b1)+";"\
								 + str(current_bout_J3r1)+";"\
								 + str(current_bout_J3b1)+";"\
								 + str(current_bout_J4r1)+";"\
								 + str(current_bout_J4b1)+";"\
								 + str(current_bout_J5r1)+";"\
								 + str(current_bout_J5b1)+";"\
								 + str(current_bout_kdr1)+";"\
								 + str(current_bout_kdb1)+";"\
								 + str(current_bout_wr1)+";"\
								 + str(current_bout_wb1)+";"\
								 + str(current_bout_ix1r1)+";"\
								 + str(current_bout_ix1b1)+";"\
								 + str(current_bout_ix2r1)+";"\
								 + str(current_bout_ix2b1)+";"\
								 + str(current_bout_ix3r1)+";"\
								 + str(current_bout_ix3b1)+";"\
								 + str(current_bout_ix4r1)+";"\
								 + str(current_bout_ix4b1)+";"\
								 + str(current_bout_ix5r1)+";"\
								 + str(current_bout_ix5b1)+";"\
        \
                                 + str(current_bout_J1r2)+";"\
                                 + str(current_bout_J1b2)+";"\
								 + str(current_bout_J2r2)+";"\
								 + str(current_bout_J2b2)+";"\
								 + str(current_bout_J3r2)+";"\
								 + str(current_bout_J3b2)+";"\
								 + str(current_bout_J4r2)+";"\
								 + str(current_bout_J4b2)+";"\
								 + str(current_bout_J5r2)+";"\
								 + str(current_bout_J5b2)+";"\
								 + str(current_bout_kdr2)+";"\
								 + str(current_bout_kdb2)+";"\
								 + str(current_bout_wr2)+";"\
								 + str(current_bout_wb2)+";"\
								 + str(current_bout_ix1r2)+";"\
								 + str(current_bout_ix1b2)+";"\
								 + str(current_bout_ix2r2)+";"\
								 + str(current_bout_ix2b2)+";"\
								 + str(current_bout_ix3r2)+";"\
								 + str(current_bout_ix3b2)+";"\
								 + str(current_bout_ix4r2)+";"\
								 + str(current_bout_ix4b2)+";"\
								 + str(current_bout_ix5r2)+";"\
								 + str(current_bout_ix5b2)+";"\
        \
                                 + str(current_bout_J1r3)+";"\
                                 + str(current_bout_J1b3)+";"\
								 + str(current_bout_J2r3)+";"\
								 + str(current_bout_J2b3)+";"\
								 + str(current_bout_J3r3)+";"\
								 + str(current_bout_J3b3)+";"\
								 + str(current_bout_J4r3)+";"\
								 + str(current_bout_J4b3)+";"\
								 + str(current_bout_J5r3)+";"\
								 + str(current_bout_J5b3)+";"\
								 + str(current_bout_kdr3)+";"\
								 + str(current_bout_kdb3)+";"\
								 + str(current_bout_wr3)+";"\
								 + str(current_bout_wb3)+";"\
								 + str(current_bout_ix1r3)+";"\
								 + str(current_bout_ix1b3)+";"\
								 + str(current_bout_ix2r3)+";"\
								 + str(current_bout_ix2b3)+";"\
								 + str(current_bout_ix3r3)+";"\
								 + str(current_bout_ix3b3)+";"\
								 + str(current_bout_ix4r3)+";"\
								 + str(current_bout_ix4b3)+";"\
								 + str(current_bout_ix5r3)+";"\
								 + str(current_bout_ix5b3)+";"\
        \
                                 + str(current_bout_J1r4)+";"\
                                 + str(current_bout_J1b4)+";"\
								 + str(current_bout_J2r4)+";"\
								 + str(current_bout_J2b4)+";"\
								 + str(current_bout_J3r4)+";"\
								 + str(current_bout_J3b4)+";"\
								 + str(current_bout_J4r4)+";"\
								 + str(current_bout_J4b4)+";"\
								 + str(current_bout_J5r4)+";"\
								 + str(current_bout_J5b4)+";"\
								 + str(current_bout_kdr4)+";"\
								 + str(current_bout_kdb4)+";"\
								 + str(current_bout_wr4)+";"\
								 + str(current_bout_wb4)+";"\
								 + str(current_bout_ix1r4)+";"\
								 + str(current_bout_ix1b4)+";"\
								 + str(current_bout_ix2r4)+";"\
								 + str(current_bout_ix2b4)+";"\
								 + str(current_bout_ix3r4)+";"\
								 + str(current_bout_ix3b4)+";"\
								 + str(current_bout_ix4r4)+";"\
								 + str(current_bout_ix4b4)+";"\
								 + str(current_bout_ix5r4)+";"\
								 + str(current_bout_ix5b4)

        # WRITE 'NEW' RECORD TO DBASE
        with open("C:/_project/log/boutscores_dbase_table.csv","a+") as boutscores_dbase_table:
            boutscores_dbase_table.write("\n"+str(datalog_current_record))

# ************ THIS IS WHERE THIS RECORD CAN BE ADDED INTO THE DBASE ************ #

# get current state of list now to see if anything has changed
updated_list = list_of_dbase_boutscores_numbers[:]

# compare current list with updated list
newly_added = returnNotMatches(current_list,updated_list)
if newly_added != []:
    printing("\nAdded following boutscores lognums:", event_db_log)
    for index in range(0,len(newly_added)):
        printing("\n -- " + newly_added[index], event_db_log)
else:
    printing("\n -- NO NEW BOUTSCORES ADDED.", event_db_log)
    # print("\nNumber of Database records is: " + str(len(updated_list)),event_db_log)


###############################################################################################################
# Display size of each DBASE file post processing
###############################################################################################################
printing("\n\n"+"-"*50, event_db_log)
with open("C:/_project/log/competition_dbase_table.csv","r+") as competition_dbase_table:
    list_of_records_from_competition_dbase_table = competition_dbase_table.readlines()
    list_of_records_from_competition_dbase_table = list_of_records_from_competition_dbase_table[2:] # strip col headings & dummy record
    printing("\nNumber of competitions by name in DBASE: " + str(len(list_of_records_from_competition_dbase_table)),event_db_log)

with open("C:/_project/log/boxers_dbase_table.csv","r+") as boxers_dbase_table:
    list_of_records_from_boxers_dbase_table = boxers_dbase_table.readlines()
    list_of_records_from_boxers_dbase_table = list_of_records_from_boxers_dbase_table[2:] # strip col headings and dummy record
    printing("\nNumber of boxers by name in DBASE: " + str(len(list_of_records_from_boxers_dbase_table)), event_db_log)

with open("C:/_project/log/officials_dbase_table.csv","r+") as officials_dbase_table:
    list_of_records_from_officials_dbase_table = officials_dbase_table.readlines()
    list_of_records_from_officials_dbase_table = list_of_records_from_officials_dbase_table[2:] # strip col headings and dummy record
    printing("\nNumber of officials by name in DBASE: " + str(len(list_of_records_from_officials_dbase_table)),event_db_log)

with open("C:/_project/log/bouts_dbase_table.csv","r+") as bouts_dbase_table:
    list_of_records_from_bouts_dbase_table = bouts_dbase_table.readlines()
    list_of_records_from_bouts_dbase_table = list_of_records_from_bouts_dbase_table[2:] # strip col headings and dummy record
    printing("\nNumber of bouts by lognum in DBASE: " + str(len(list_of_records_from_bouts_dbase_table)),event_db_log)

with open("C:/_project/log/boutscores_dbase_table.csv","r+") as boutscores_dbase_table:
    list_of_records_from_boutscores_dbase_table = boutscores_dbase_table.readlines()
    list_of_records_from_boutscores_dbase_table = list_of_records_from_boutscores_dbase_table[2:] # strip col headings and dummy record
    printing("\nNumber of boutscores by lognum in DBASE: " + str(len(list_of_records_from_boutscores_dbase_table)),event_db_log)

##############################################################################################################
event_db_log.close()
