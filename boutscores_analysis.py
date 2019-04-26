###############################################################################################################
# Filename: boutscores_analysis.py
# Author: Paul Williamson
# Date: 15/11/2017
# ###############################################################################################################
# IMPORT MODULES/PACKAGES
###############################################################################################################
###############################################################################################################
import sys
import socket
import tkinter
from tkinter import filedialog
import pandas as pd
import numpy as np

pd.set_option('display.width', 3000)
pd.options.display.max_rows = None
pd.options.display.max_columns = None

hostname=(socket.gethostname())
print(hostname)

###############################################################################################################
###############################################################################################################
# PICK DATALOG FOLDER
###############################################################################################################
###############################################################################################################
#  Get user to pick dbase folder i.e. folder holding database files to be written/inserted into sql server db

root = tkinter.Tk()
root.withdraw()
datapath=filedialog.askdirectory(title="Select DBASE folder with dbase_table files...")
root.destroy()
if not datapath:
    sys.exit("You cancelled!!!") # handle dialog cancel event

# Otherwise display datapath selected
print(datapath)
print("*"*100,"\n") # JUST WHITESPACE

###############################################################################################################
# READ & ANALYSE BOUTS_DBASE_TABLE FILE
###############################################################################################################

bouts_dataframe = pd.read_csv(datapath+"/bouts_dbase_table.csv", sep=';')
bouts_dataframe.set_index('pk_bout_index', inplace=True)
#print(bouts_dataframe)

boutscores_dataframe = pd.read_csv(datapath+"/boutscores_dbase_table.csv", sep=';')
boutscores_dataframe.set_index('pk_boutscores_index', inplace=True)
#print(boutscores_dataframe)

# JOIN BOUTs DATAFRAME TO SCORES DATAFRAME FOR ANALYSIS LATER
#-----------------------------------------------------------------------------------------------------------------------
huge_df = pd.concat([bouts_dataframe, boutscores_dataframe], axis=1)
#print(huge_df)

# ADD OVERALL SCORES COLUMNS FOR ANALYSIS
#-----------------------------------------------------------------------------------------------------------------------
huge_df["j1_redscore"] = huge_df["J1r1"] + huge_df["J1r2"] + huge_df["J1r3"] + huge_df["J1r4"]
huge_df["j1_bluescore"] = huge_df["J1b1"] + huge_df["J1b2"] + huge_df["J1b3"] + huge_df["J1b4"]
huge_df["j2_redscore"] = huge_df["J2r1"] + huge_df["J2r2"] + huge_df["J2r3"] + huge_df["J2r4"]
huge_df["j2_bluescore"] = huge_df["J2b1"] + huge_df["J2b2"] + huge_df["J2b3"] + huge_df["J2b4"]
huge_df["j3_redscore"] = huge_df["J3r1"] + huge_df["J3r2"] + huge_df["J3r3"] + huge_df["J3r4"]
huge_df["j3_bluescore"] = huge_df["J3b1"] + huge_df["J3b2"] + huge_df["J3b3"] + huge_df["J3b4"]
huge_df["j4_redscore"] = huge_df["J4r1"] + huge_df["J4r2"] + huge_df["J4r3"] + huge_df["J4r4"]
huge_df["j4_bluescore"] = huge_df["J4b1"] + huge_df["J4b2"] + huge_df["J4b3"] + huge_df["J4b4"]
huge_df["j5_redscore"] = huge_df["J5r1"] + huge_df["J5r2"] + huge_df["J5r3"] + huge_df["J5r4"]
huge_df["j5_bluescore"] = huge_df["J5b1"] + huge_df["J5b2"] + huge_df["J5b3"] + huge_df["J5b4"]

######################################################################################################################

huge_df["round_1_red_scores"] = huge_df["J1r1"] + huge_df["J2r1"] + huge_df["J3r1"] + huge_df["J4r1"] + huge_df["J5r1"]
huge_df["round_1_blue_scores"] = huge_df["J1b1"] + huge_df["J2b1"] + huge_df["J3b1"] + huge_df["J4b1"] + huge_df["J5b1"]
huge_df["round_2_red_scores"] = huge_df["J1r2"] + huge_df["J2r2"] + huge_df["J3r2"] + huge_df["J4r2"] + huge_df["J5r2"]
huge_df["round_2_blue_scores"] = huge_df["J1b2"] + huge_df["J2b2"] + huge_df["J3b2"] + huge_df["J4b2"] + huge_df["J5b2"]
huge_df["round_3_red_scores"] = huge_df["J1r3"] + huge_df["J2r3"] + huge_df["J3r3"] + huge_df["J4r3"] + huge_df["J5r3"]
huge_df["round_3_blue_scores"] = huge_df["J1b3"] + huge_df["J2b3"] + huge_df["J3b3"] + huge_df["J4b3"] + huge_df["J5b3"]
huge_df["round_4_red_scores"] = huge_df["J1r4"] + huge_df["J2r4"] + huge_df["J3r4"] + huge_df["J4r4"] + huge_df["J5r4"]
huge_df["round_4_blue_scores"] = huge_df["J1b4"] + huge_df["J2b4"] + huge_df["J3b4"] + huge_df["J4b4"] + huge_df["J5b4"]

#huge_df.to_csv(datapath+"/stats/huge_df.csv",sep=';') # just used to check output of DATAFRAME BUILD above

########################################################################################################################
# ANALYSIS: 3x ROUNDS - 5x JUDGES - WP only decisions
########################################################################################################################
print("*"*24,"  ANALYSIS: 3x ROUNDS - 5x JUDGES - WP decisions  ","*"*24)
listof_3r_5j_wp_df = huge_df[( huge_df["number_of_rounds"] == 3 ) & ( huge_df["data_format"]== "5-of-5J" ) & ( huge_df["result_text"] == "WP" )]
num_bouts = len(listof_3r_5j_wp_df)
listof_3r_5j_wp_df = listof_3r_5j_wp_df.fillna(0)
listof_3r_5j_wp_df.to_csv(datapath+"/stats/boutscores_3r_5j_wp_df.csv",sep=';') # just used to check output of DATAFRAME BUILD above
#print(listof_3r_5j_wp_df)
#-----------------------------------------------------------------------------------------------------------------------


print("\nNUMBER OF CONTESTS ANALYSED:",num_bouts)
print("-"*100)
print("-"*100)
# RED winner Vs BLUE winner
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_bout = listof_3r_5j_wp_df["winner"]\
    [ listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] ]
num_red_win_bout = len(listof_all_red_win_bout)
print("Total RED corner winners: %d (%.2f%%)" % (num_red_win_bout,((num_red_win_bout/num_bouts)*100)))

listof_all_blue_win_bout = listof_3r_5j_wp_df["winner"]\
        [ listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] ]
num_blue_win_bout = len(listof_all_blue_win_bout)
print("Total BLUE corner winners: %d (%.2f%%)" % (num_blue_win_bout,((num_blue_win_bout/num_bouts)*100)))

# REMOVE ANY NO-WIN DUMMY RECORDS FROM ANALYSIS
#-----------------------------------------------------------------------------------------------------------------------
listof_all_NO_win_bout = listof_3r_5j_wp_df["winner"]\
    [( listof_3r_5j_wp_df["winner"] != listof_3r_5j_wp_df["red_boxer_name"])\
    & ( listof_3r_5j_wp_df["winner"] != listof_3r_5j_wp_df["blue_boxer_name"])]
num_NO_win_bouts = len(listof_all_NO_win_bout)

if num_NO_win_bouts >0:
    print("Total NO corner winners: %d (%.2f%%)" % (num_NO_win_bouts,((num_NO_win_bouts/num_bouts)*100)))
    print("\nlistof_all_NO_win_bout:\n",listof_all_NO_win_bout)
    num_bouts = num_bouts - num_NO_win_bouts
    print("\nCORRECTED - NUMBER OF CONTESTS ANALYSED: ",num_bouts)

print("-"*100)
print("-"*100)


# COUNT NUMBER OF TIMES WINNER OF ROUND 1 ALSO WON BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_rd1_win_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )].value_counts()
num_red_rd1_win_win = len(listof_all_red_win_rd1_win_bout)
print("Number in RED corner who won Rd1 and won the bout:",num_red_rd1_win_win)

listof_all_blue_win_rd1_win_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_blue_scores"] > listof_3r_5j_wp_df["round_1_red_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )].value_counts()
num_blue_rd1_win_win = len(listof_all_blue_win_rd1_win_bout)
print("Number in BLUE corner who won Rd1 and won the bout:",num_blue_rd1_win_win)

total_rd1_win_win = num_red_rd1_win_win + num_blue_rd1_win_win
print("Total who won Rd1 and won the bout: %d (%.2f%%)" % (total_rd1_win_win,((total_rd1_win_win/num_bouts)*100)))

# COUNT NUMBER OF TIMES LOSER OF ROUND 1 ALSO WON BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_lose_rd1_win_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_blue_scores"] > listof_3r_5j_wp_df["round_1_red_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )].value_counts()
num_red_rd1_lose_win = len(listof_all_red_lose_rd1_win_bout)
print("\nNumber in RED corner who lost Rd1 and won the bout:",num_red_rd1_lose_win)

listof_all_blue_lose_rd1_win_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )].value_counts()
num_blue_rd1_lose_win = len(listof_all_blue_lose_rd1_win_bout)
print("Number in BLUE corner who lost Rd1 and won the bout:",num_blue_rd1_lose_win)

total_rd1_lose_win = num_red_rd1_lose_win + num_blue_rd1_lose_win
print("Total who lost Rd1 but won the bout: %d (%.2f%%)" % (total_rd1_lose_win,((total_rd1_lose_win/num_bouts)*100)))

# HOW DOES WINNING ROUND 1 DETERMINE BOUT WINNER:
#-----------------------------------------------------------------------------------------------------------------------
total_win_check_rd1 = total_rd1_win_win + total_rd1_lose_win
print("\nHOW DOES WINNING ROUND 1 DETERMINE BOUT WINNER: %.2f%%" % ((total_rd1_win_win/total_win_check_rd1) * 100))

print("-"*100)
print("-"*100)

# COUNT NUMBER OF TIMES ROUND 1 WINNER LOST BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_rd1_lose_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )].value_counts()
num_red_rd1_win_lose = len(listof_all_red_win_rd1_lose_bout)
print("\nNumber in RED corner who won Rd1 and lost the bout:",num_red_rd1_win_lose)

listof_all_blue_win_rd1_lose_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_blue_scores"] > listof_3r_5j_wp_df["round_1_red_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )].value_counts()
num_blue_rd1_win_lose = len(listof_all_blue_win_rd1_lose_bout)
print("Number in BLUE corner who won Rd1 and lost the bout:",num_blue_rd1_win_lose)

total_rd1_win_lose = num_red_rd1_win_lose + num_blue_rd1_win_lose
print("Total who won Rd1 but lost the bout: %d (%.2f%%)" % (total_rd1_win_lose,((total_rd1_win_lose/num_bouts)*100)))

# COUNT NUMBER OF TIMES ROUND 1 LOSER LOST BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_lose_rd1_lose_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] < listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_red_rd1_lose_lose = len(listof_all_red_lose_rd1_lose_bout)
print("\nNumber in RED corner who lost Rd1 and lost the bout:",num_red_rd1_lose_lose)

listof_all_blue_lose_rd1_lose_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_blue_rd1_lose_lose = len(listof_all_blue_lose_rd1_lose_bout)
print("Number in BLUE corner who lost Rd1 and lost the bout:",num_blue_rd1_lose_lose)

total_rd1_lose_lose = num_red_rd1_lose_lose + num_blue_rd1_lose_lose
print("Total who lost Rd1 and lost the bout: %d (%.2f%%)" % (total_rd1_lose_lose,((total_rd1_lose_lose/num_bouts)*100)))

# HOW DOES LOSING ROUND 1 DETERMINE BOUT LOSER:
#-----------------------------------------------------------------------------------------------------------------------
total_lose_check_rd1 = total_rd1_win_lose + total_rd1_lose_lose
print("\nHOW DOES LOSING ROUND 1 DETERMINE BOUT LOSER: %.2f%%" % ((total_rd1_lose_lose/total_lose_check_rd1) * 100))

print("-"*100)
print("-"*100)

# FURTHER ANALYSIS...
print("\n\nFURTHER ANALYSIS...")
# COUNT NUMBER OF TIMES ROUNDS 1 & 2 WINNER WON BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_rd12_win_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] > listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] < listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_red_rd12_win_win = len(listof_all_red_win_rd12_win_bout)

listof_all_blue_win_rd12_win_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] < listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] < listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] > listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_blue_rd12_win_win = len(listof_all_blue_win_rd12_win_bout)

total_rd12_win_win = num_red_rd12_win_win + num_blue_rd12_win_win
print("Total who won Rd1 and Rd2, lost Rd3 and won bout: %d (%.2f%%)" % (total_rd12_win_win,((total_rd12_win_win/num_bouts)*100)))

# COUNT NUMBER OF TIMES ROUNDS 1 & 2 WINNER LOST BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_rd12_lose_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] > listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] < listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_red_rd12_win_lose = len(listof_all_red_win_rd12_lose_bout)

listof_all_blue_win_rd12_lose_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] < listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] < listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] > listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_blue_rd12_win_lose = len(listof_all_blue_win_rd12_lose_bout)

total_rd12_win_lose = num_red_rd12_win_lose + num_blue_rd12_win_lose
print("Total who won Rd1 and Rd2, lost Rd3 and lost bout: %d (%.2f%%)" % (total_rd12_win_lose,((total_rd12_win_lose/num_bouts)*100)))

print("-"*100)


# COUNT NUMBER OF TIMES ROUNDS 1 & 3 WINNER WON BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_rd13_win_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] < listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] > listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_red_rd13_win_win = len(listof_all_red_win_rd13_win_bout)

listof_all_blue_win_rd13_win_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] < listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] > listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] < listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_blue_rd13_win_win = len(listof_all_blue_win_rd13_win_bout)

total_rd13_win_win = num_red_rd13_win_win + num_blue_rd13_win_win
print("Total who won Rd1 and Rd3, lost Rd2 and won bout: %d (%.2f%%)" % (total_rd13_win_win,((total_rd13_win_win/num_bouts)*100)))

# COUNT NUMBER OF TIMES ROUNDS 1 & 3 WINNER BUT LOST BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_rd13_lose_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] < listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] > listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_red_rd13_win_lose = len(listof_all_red_win_rd13_lose_bout)

listof_all_blue_win_rd13_lose_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] < listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] > listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] < listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_blue_rd13_win_lose = len(listof_all_blue_win_rd13_lose_bout)

total_rd13_win_lose = num_red_rd13_win_lose + num_blue_rd13_win_lose
print("Total who won Rd1 and Rd3, lost Rd2 and lost bout: %d (%.2f%%)" % (total_rd13_win_lose,((total_rd13_win_lose/num_bouts)*100)))

print("-"*100)


# COUNT NUMBER OF TIMES ROUNDS 2 & 3 WINNER WON BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_rd23_win_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] < listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] > listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] > listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_red_rd23_win_win = len(listof_all_red_win_rd23_win_bout)

listof_all_blue_win_rd23_win_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] < listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] < listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_blue_rd23_win_win = len(listof_all_blue_win_rd23_win_bout)

total_rd23_win_win = num_red_rd23_win_win + num_blue_rd23_win_win
print("Total who won Rd2 and Rd3, lost Rd1 and won bout: %d (%.2f%%)" % (total_rd23_win_win,((total_rd23_win_win/num_bouts)*100)))

# COUNT NUMBER OF TIMES ROUNDS 2 & 3 WINNER LOST BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_rd23_lose_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] < listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] > listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] > listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_red_rd23_win_lose = len(listof_all_red_win_rd23_lose_bout)

listof_all_blue_win_rd23_lose_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] < listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] < listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_blue_rd23_win_lose = len(listof_all_blue_win_rd23_lose_bout)

total_rd23_win_lose = num_red_rd23_win_lose + num_blue_rd23_win_lose
print("Total who won Rd2 and Rd3, lost Rd1 and lost bout: %d (%.2f%%)" % (total_rd23_win_lose,((total_rd23_win_lose/num_bouts)*100)))

print("-"*100)


# COUNT NUMBER OF TIMES ROUNDS 1,2 & 3 WINNER WON BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_rd123_win_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] > listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] > listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_red_rd123_win_win = len(listof_all_red_win_rd123_win_bout)

listof_all_blue_win_rd123_win_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] < listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] < listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] < listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_blue_rd123_win_win = len(listof_all_blue_win_rd123_win_bout)

total_rd123_win_win = num_red_rd123_win_win + num_blue_rd123_win_win
print("Total who won all three rounds and won bout: %d (%.2f%%)" % (total_rd123_win_win,((total_rd123_win_win/num_bouts)*100)))

# COUNT NUMBER OF TIMES WINNER OF ROUNDS 1,2 & 3 LOST BOUT
#-----------------------------------------------------------------------------------------------------------------------
listof_all_red_win_rd123_lose_bout = listof_3r_5j_wp_df["red_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] > listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] > listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] > listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["blue_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_red_rd123_win_lose = len(listof_all_red_win_rd123_lose_bout)

listof_all_blue_win_rd123_lose_bout = listof_3r_5j_wp_df["blue_boxer_name"]\
    [( listof_3r_5j_wp_df["round_1_red_scores"] < listof_3r_5j_wp_df["round_1_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_2_red_scores"] < listof_3r_5j_wp_df["round_2_blue_scores"] )\
    & ( listof_3r_5j_wp_df["round_3_red_scores"] < listof_3r_5j_wp_df["round_3_blue_scores"] )\
    & ( listof_3r_5j_wp_df["winner"] == listof_3r_5j_wp_df["red_boxer_name"] )\
    & ( listof_3r_5j_wp_df["result_text"]=="WP" )].value_counts()
num_blue_rd123_win_lose = len(listof_all_blue_win_rd123_lose_bout)

total_rd123_win_lose = num_red_rd123_win_lose + num_blue_rd123_win_lose


# THIS IS A LITLE KNOWN ANOMOLY THAT CAN OCCUR IN THE CURRENT AIBA SCORING SYSTEM SO DOCUMENT IT...
#-----------------------------------------------------------------------------------------------------------------------
# PRODUCE LIST OF CONTESTS WHERE WINNER OF ALL 3 ROUNDS ACTUALLY LOST BOUT
listof_all_red_win_rd123_lose_bout1 = listof_3r_5j_wp_df.query('round_1_red_scores > round_1_blue_scores\
                                                                & round_2_red_scores > round_2_blue_scores\
                                                                & round_3_red_scores > round_3_blue_scores\
                                                                & winner == blue_boxer_name')

listof_all_blue_win_rd123_lose_bout1 = listof_3r_5j_wp_df.query('round_1_red_scores < round_1_blue_scores\
                                                                & round_2_red_scores < round_2_blue_scores\
                                                                & round_3_red_scores < round_3_blue_scores\
                                                                & winner == red_boxer_name')

if total_rd123_win_lose>0:
    print("Total who won all three rounds but lost bout: %d (%.2f%%)" % (total_rd123_win_lose,((total_rd123_win_lose/num_bouts)*100)))
    print("\nlistOfRED_rd123_win_lose:\n",listof_all_red_win_rd123_lose_bout1)
    print("\nlistOfBLUE_rd123_win_lose:\n",listof_all_blue_win_rd123_lose_bout1)
print("-"*100)


# COUNT NUMBER OF TIMES WINNER OF MOST or ALL ROUNDS WON/LOST BOUT
#-----------------------------------------------------------------------------------------------------------------------
total_most_or_all_rds_win_win = total_rd23_win_win + total_rd13_win_win + total_rd123_win_win
print("\nTotal who won ALL or MOST rounds and WON the bout: %d (%.2f%%)" % (total_most_or_all_rds_win_win,((total_most_or_all_rds_win_win/num_bouts)*100)))

total_most_or_all_rds_win_lose = total_rd23_win_lose + total_rd13_win_lose + total_rd123_win_lose
print("Total who won ALL or MOST rounds and LOST the bout: %d (%.2f%%)" % (total_most_or_all_rds_win_lose,((total_most_or_all_rds_win_lose/num_bouts)*100)))

print("-"*100)
#-----------------------------------------------------------------------------------------------------------------------


#listof_3r_3j_wp_df = huge_df[( huge_df["number_of_rounds"] == 3 ) & ( huge_df["data_format"]== "3-of-5J" ) & ( huge_df["result_text"] == "WP" )]
#num_bouts = len(listof_3r_3j_wp_df)
#print(listof_3r_5j_wp_df)
#print("\nNUMBER OF CONTESTS ANALYSED:",num_bouts)
