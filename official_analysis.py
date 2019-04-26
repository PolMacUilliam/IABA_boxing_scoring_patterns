###############################################################################################################
# Filename: official_analysis.py
# Author: Paul Williamson
# Date: 06/11/2017
###############################################################################################################
# IMPORT MODULES/PACKAGES
###############################################################################################################
###############################################################################################################
import sys
import socket
import tkinter
from tkinter import filedialog
import pandas as pd
import numpy as np

pd.set_option('display.width', 1000)
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
print("\n","*"*100) # JUST WHITESPACE

###############################################################################################################
# READ & ANALYSE BOUTS_DBASE_TABLE FILE
###############################################################################################################

bouts_dataframe = pd.read_csv(datapath+"/bouts_dbase_table.csv", sep=';', index_col='pk_bout_index')
#bouts_dataframe.set_index('pk_bout_index', inplace=True)
#print(bouts_dataframe)

boutscores_dataframe = pd.read_csv(datapath+"/boutscores_dbase_table.csv", sep=';', index_col='pk_boutscores_index')
#boutscores_dataframe.set_index('pk_boutscores_index', inplace=True)
#print(boutscores_dataframe)

# JOIN BOUTS DATAFRAME TO BOUTSCORES DATAFRAME FOR ANALYSIS LATER
#-----------------------------------------------------------------------------------------------------------------------
big_df = pd.concat([bouts_dataframe, boutscores_dataframe], axis=1) # axis=0 > columns, axis=1 > rows
print("big_df.shape: ",big_df.shape)

# ADD OVERALL SCORES COLUMNS FOR ANALYSIS LATER
#-----------------------------------------------------------------------------------------------------------------------
big_df["j1_redscore"] = big_df["J1r1"] + big_df["J1r2"] + big_df["J1r3"] + big_df["J1r4"]
big_df["j1_bluescore"] = big_df["J1b1"] + big_df["J1b2"] + big_df["J1b3"] + big_df["J1b4"]
big_df["j2_redscore"] = big_df["J2r1"] + big_df["J2r2"] + big_df["J2r3"] + big_df["J2r4"]
big_df["j2_bluescore"] = big_df["J2b1"] + big_df["J2b2"] + big_df["J2b3"] + big_df["J2b4"]
big_df["j3_redscore"] = big_df["J3r1"] + big_df["J3r2"] + big_df["J3r3"] + big_df["J3r4"]
big_df["j3_bluescore"] = big_df["J3b1"] + big_df["J3b2"] + big_df["J3b3"] + big_df["J3b4"]
big_df["j4_redscore"] = big_df["J4r1"] + big_df["J4r2"] + big_df["J4r3"] + big_df["J4r4"]
big_df["j4_bluescore"] = big_df["J4b1"] + big_df["J4b2"] + big_df["J4b3"] + big_df["J4b4"]
big_df["j5_redscore"] = big_df["J5r1"] + big_df["J5r2"] + big_df["J5r3"] + big_df["J5r4"]
big_df["j5_bluescore"] = big_df["J5b1"] + big_df["J5b2"] + big_df["J5b3"] + big_df["J5b4"]

######################################################################################################################
# OFFICIALS DATAFRAME:
# Extract data (as a series) from the main input dataframe
# Each series will be a new column in the Officials stats dataframe
######################################################################################################################

# COUNT EACH OFFICIALS APPEARANCE AS REFEREE
#-----------------------------------------------------------------------------------------------------------------------
official_series_referee_num_bouts = big_df["referee_name"].value_counts()
#print("\nofficial_series_referee_num_bouts:\n",official_series_referee_num_bouts,type(official_series_referee_num_bouts),len(official_series_referee_num_bouts))
#official_df_referee_num_bouts = pd.DataFrame(official_series_referee_num_bouts) # not necessary, can concat series to dataframe

official_series_referee_num_rounds = big_df.groupby("referee_name")["number_of_rounds"].sum()
#print("\official_series_referee_num_rounds:  ",type(official_series_referee_num_rounds),len(official_series_referee_num_rounds))

official_series_referee_num_finals = big_df["referee_name"][big_df["competition_session_name"] == "Finals"].value_counts()
#print("\nofficial_series_referee_num_finals:  ",type(official_series_referee_num_finals),len(official_series_referee_num_finals))


# CALCULATE EACH OFFICIALS APPEARANCE AS A JUDGE PER SEAT, THEN GET OVERALL COUNT AS JUDGE
#-----------------------------------------------------------------------------------------------------------------------
official_series_j1_num_bouts = big_df["judge1_name"].value_counts()
official_series_j1_num_wp_bouts = big_df["judge1_name"][big_df["result_text"]=="WP"].value_counts()
official_series_j2_num_bouts = big_df["judge2_name"].value_counts()
official_series_j2_num_wp_bouts = big_df["judge2_name"][big_df["result_text"]=="WP"].value_counts()
official_series_j3_num_bouts = big_df["judge3_name"].value_counts()
official_series_j3_num_wp_bouts = big_df["judge3_name"][big_df["result_text"]=="WP"].value_counts()
official_series_j4_num_bouts = big_df["judge4_name"].value_counts()
official_series_j4_num_wp_bouts = big_df["judge4_name"][big_df["result_text"]=="WP"].value_counts()
official_series_j5_num_bouts = big_df["judge5_name"].value_counts()
official_series_j5_num_wp_bouts = big_df["judge5_name"][big_df["result_text"]=="WP"].value_counts()

official_series_j12_num_bouts = official_series_j1_num_bouts.add(official_series_j2_num_bouts, axis = "index",fill_value=0)
official_series_j123_num_bouts = official_series_j12_num_bouts.add(official_series_j3_num_bouts,axis = "index",fill_value=0)
official_series_j1234_num_bouts = official_series_j123_num_bouts.add(official_series_j4_num_bouts,axis = "index",fill_value=0)
official_series_j12345_num_bouts = official_series_j1234_num_bouts.add(official_series_j5_num_bouts,axis = "index",fill_value=0)
#print("\official_series_j12345_num_bouts:\n",official_series_j12345_num_bouts,type(official_series_j12345_num_bouts), len(official_series_j12345_num_bouts))

official_series_j12_num_wp_bouts = official_series_j1_num_wp_bouts.add(official_series_j2_num_wp_bouts,fill_value=0)
official_series_j123_num_wp_bouts = official_series_j12_num_wp_bouts.add(official_series_j3_num_wp_bouts,fill_value=0)
official_series_j1234_num_wp_bouts = official_series_j123_num_wp_bouts.add(official_series_j4_num_wp_bouts,fill_value=0)
official_series_j12345_num_wp_bouts = official_series_j1234_num_wp_bouts.add(official_series_j5_num_wp_bouts,fill_value=0)
#print("\official_series_j12345_num_wp_bouts:\n",official_series_j12345_num_wp_bouts,type(official_series_j12345_num_wp_bouts), len(official_series_j12345_num_wp_bouts))


#######################################################################################################################
#######################################################################################################################
# FOR JUDGES SCORING ANALYSIS JUST CONSIDER ALL WP DECISIONS WITH 3 ROUNDS
#######################################################################################################################
big_df = big_df[ ( big_df["result_text"] == "WP" ) & ( big_df["number_of_rounds"] == 3 ) ]
#big_df = big_df[ big_df["result_text"] == "WP" ]
print("adjusted big_df.shape: ",big_df.shape)
#######################################################################################################################
#######################################################################################################################



# CALCULATE THE TOTAL NUMBER OF ROUNDS EACH OFFICIAL HAS JUDGED IN COMPLETED BOUTS (3 ROUNDS AND WP RESULTS ONLY)
#-----------------------------------------------------------------------------------------------------------------------
official_series_j1_num_rounds = big_df.groupby("judge1_name")["number_of_rounds"].sum()
#print("\official_series_j1_num_rounds:\n",official_series_j1_num_rounds,type(official_series_j1_num_rounds), len(official_series_j1_num_rounds))
official_series_j2_num_rounds = big_df.groupby("judge2_name")["number_of_rounds"].sum()
#print("\official_series_j2_num_rounds:\n",official_series_j2_num_rounds,type(official_series_j2_num_rounds), len(official_series_j2_num_rounds))
official_series_j3_num_rounds = big_df.groupby("judge3_name")["number_of_rounds"].sum()
#print("\official_series_j3_num_rounds:\n",official_series_j3_num_rounds,type(official_series_j3_num_rounds), len(official_series_j3_num_rounds))
official_series_j4_num_rounds = big_df.groupby("judge4_name")["number_of_rounds"].sum()
#print("\official_series_j4_num_rounds: ",official_series_j4_num_rounds,type(official_series_j4_num_rounds), len(official_series_j4_num_rounds))
official_series_j5_num_rounds = big_df.groupby("judge5_name")["number_of_rounds"].sum()
#print("\official_series_j5_num_rounds: ",official_series_j5_num_rounds,type(official_series_j5_num_rounds), len(official_series_j5_num_rounds))

# ADD UP ALL VALUE COUNTS
#-----------------------------------------------------------------------------------------------------------------------
official_series_j12_num_rounds = official_series_j1_num_rounds.add(official_series_j2_num_rounds, axis = "index",fill_value=0)
#print("\official_series_j12_num_rounds:\n",official_series_j12_num_rounds,type(official_series_j12_num_rounds), len(official_series_j12_num_rounds))
official_series_j123_num_rounds = official_series_j12_num_rounds.add(official_series_j3_num_rounds, axis = "index",fill_value=0)
#print("\official_series_j123_num_rounds:\n",official_series_j123_num_rounds,type(official_series_j123_num_rounds), len(official_series_j123_num_rounds))
official_series_j1234_num_rounds = official_series_j123_num_rounds.add(official_series_j4_num_rounds, axis = "index",fill_value=0)
#print("\official_series_j1234_num_rounds:\n",official_series_j1234_num_rounds,type(official_series_j1234_num_rounds), len(official_series_j1234_num_rounds))
official_series_j12345_num_rounds = official_series_j1234_num_rounds.add(official_series_j5_num_rounds, axis = "index",fill_value=0)
#print("\official_series_j12345_num_rounds:\n",official_series_j12345_num_rounds,type(official_series_j12345_num_rounds), len(official_series_j12345_num_rounds))



######################################################################################################################################################
# BOUT RESULT CALCULATIONS: ALL SPLIT DECISIONS - CHECK NUMBER OF OCCURRENCES AS A JUDGE WHERE THEIR SCORE WAS ON WRONG SIDE OF BOUT RESULT
######################################################################################################################################################

# COUNT NUMBER OF TIMES JUDGE1 WAS WRONG
#-----------------------------------------------------------------------------------------------------------------------
j1_red_win_wrong = big_df["judge1_name"][( big_df["j1_redscore"] > big_df["j1_bluescore"] )\
                                        & ( big_df["winner"] == big_df["blue_boxer_name"])\
                                        & (big_df["result_text"]=="WP")].value_counts()

j1_blue_win_wrong = big_df["judge1_name"][(big_df["j1_bluescore"] > big_df["j1_redscore"])\
                                        & (big_df["winner"] == big_df["red_boxer_name"])\
                                        & (big_df["result_text"]=="WP")].value_counts()

official_series_j1_wrong = j1_red_win_wrong.add(j1_blue_win_wrong,fill_value=0)


# COUNT NUMBER OF TIMES JUDGE2 WAS WRONG
#-----------------------------------------------------------------------------------------------------------------------
j2_red_win_wrong = big_df["judge2_name"][( big_df["j2_redscore"] > big_df["j2_bluescore"] )\
                                        & ( big_df["winner"] == big_df["blue_boxer_name"])\
                                        & (big_df["result_text"]=="WP")].value_counts()

j2_blue_win_wrong = big_df["judge2_name"][(big_df["j2_bluescore"] > big_df["j2_redscore"])\
                                        & (big_df["winner"] == big_df["red_boxer_name"])\
                                        & (big_df["result_text"]=="WP")].value_counts()

official_series_j2_wrong = j2_red_win_wrong.add(j2_blue_win_wrong,fill_value=0)


# COUNT NUMBER OF TIMES JUDGE3 WAS WRONG
#-----------------------------------------------------------------------------------------------------------------------
j3_red_win_wrong = big_df["judge3_name"][( big_df["j3_redscore"] > big_df["j3_bluescore"] )\
                                        & ( big_df["winner"] == big_df["blue_boxer_name"])\
                                        & (big_df["result_text"]=="WP")].value_counts()

j3_blue_win_wrong = big_df["judge3_name"][(big_df["j3_bluescore"] > big_df["j3_redscore"])\
                                        & (big_df["winner"] == big_df["red_boxer_name"])\
                                        & (big_df["result_text"]=="WP")].value_counts()

official_series_j3_wrong = j3_red_win_wrong.add(j3_blue_win_wrong,fill_value=0)

# COUNT NUMBER OF TIMES JUDGE4 WAS WRONG
#-----------------------------------------------------------------------------------------------------------------------
j4_red_win_wrong = big_df["judge4_name"][( big_df["j4_redscore"] > big_df["j4_bluescore"] )\
                                        & ( big_df["winner"] == big_df["blue_boxer_name"])\
                                        & (big_df["result_text"]=="WP")].value_counts()

j4_blue_win_wrong = big_df["judge4_name"][(big_df["j4_bluescore"] > big_df["j4_redscore"])\
                                        & (big_df["winner"] == big_df["red_boxer_name"])\
                                        & (big_df["result_text"]=="WP")].value_counts()

official_series_j4_wrong = j4_red_win_wrong.add(j4_blue_win_wrong,fill_value=0)


# COUNT NUMBER OF TIMES JUDGE5 WAS WRONG
#-----------------------------------------------------------------------------------------------------------------------
j5_red_win_wrong = big_df["judge4_name"][( big_df["j5_redscore"] > big_df["j5_bluescore"] )\
                                        & ( big_df["winner"] == big_df["blue_boxer_name"])\
                                        & (big_df["result_text"]=="WP")].value_counts()

j5_blue_win_wrong = big_df["judge5_name"][(big_df["j5_bluescore"] > big_df["j5_redscore"])\
                                        & (big_df["winner"] == big_df["red_boxer_name"])\
                                        & (big_df["result_text"]=="WP")].value_counts()

official_series_j5_wrong = j5_red_win_wrong.add(j5_blue_win_wrong,fill_value=0)


# ADD UP TOTAL NUMBER OF TIMES EACH JUDGE WAS ON WRONG SIDE OF BOUT DECISION AND CALCULATE PERCENTAGE
#-----------------------------------------------------------------------------------------------------------------------
official_series_j12_wrong = official_series_j1_wrong.add(official_series_j2_wrong,fill_value=0)
official_series_j123_wrong = official_series_j12_wrong.add(official_series_j3_wrong,fill_value=0)
official_series_j1234_wrong = official_series_j123_wrong.add(official_series_j4_wrong,fill_value=0)
official_series_j12345_wrong = official_series_j1234_wrong.add(official_series_j5_wrong,fill_value=0)
official_series_percent_wrong = official_series_j12345_wrong/official_series_j12345_num_wp_bouts * 100


######################################################################################################################################################
# BOUT RESULT CALCULATIONS: ONLY 4:1 or 1:4 SPLIT DECISIONS CHECK NUMBER OF OCCURRENCES AS A JUDGE WHERE THEIR SCORE WAS ON WRONG SIDE OF BOUT RESULT
######################################################################################################################################################

# COUNT NUMBER OF TIMES JUDGE 1 WAS WRONG ON 4-1 DECISIONS
#-----------------------------------------------------------------------------------------------------------------------
j1_red_win_14_wrong = big_df["judge1_name"][( big_df["j1_redscore"] > big_df["j1_bluescore"] )\
                                        & ( big_df["j2_redscore"] < big_df["j2_bluescore"] )\
                                        & ( big_df["j3_redscore"] < big_df["j3_bluescore"] )\
                                        & ( big_df["j4_redscore"] < big_df["j4_bluescore"] )\
                                        & ( big_df["j5_redscore"] < big_df["j5_bluescore"] )\
                                        ].value_counts()

j1_blue_win_41_wrong = big_df["judge1_name"][( big_df["j1_redscore"] < big_df["j1_bluescore"] )\
                                        & ( big_df["j2_redscore"] > big_df["j2_bluescore"] )\
                                        & ( big_df["j3_redscore"] > big_df["j3_bluescore"] )\
                                        & ( big_df["j4_redscore"] > big_df["j4_bluescore"] )\
                                        & ( big_df["j5_redscore"] > big_df["j5_bluescore"] )\
                                        ].value_counts()

official_series_j1_14_41_wrong = j1_red_win_14_wrong.add(j1_blue_win_41_wrong,fill_value=0)

# COUNT NUMBER OF TIMES JUDGE 2 WAS WRONG ON 4-1 DECISIONS
#-----------------------------------------------------------------------------------------------------------------------
j2_red_win_14_wrong = big_df["judge2_name"][( big_df["j2_redscore"] > big_df["j2_bluescore"] )\
                                        & ( big_df["j1_redscore"] < big_df["j1_bluescore"] )\
                                        & ( big_df["j3_redscore"] < big_df["j3_bluescore"] )\
                                        & ( big_df["j4_redscore"] < big_df["j4_bluescore"] )\
                                        & ( big_df["j5_redscore"] < big_df["j5_bluescore"] )\
                                        ].value_counts()

j2_blue_win_41_wrong = big_df["judge2_name"][( big_df["j1_redscore"] < big_df["j1_bluescore"] )\
                                        & ( big_df["j2_redscore"] > big_df["j2_bluescore"] )\
                                        & ( big_df["j3_redscore"] > big_df["j3_bluescore"] )\
                                        & ( big_df["j4_redscore"] > big_df["j4_bluescore"] )\
                                        & ( big_df["j5_redscore"] > big_df["j5_bluescore"] )\
                                        ].value_counts()

official_series_j2_14_41_wrong = j2_red_win_14_wrong.add(j2_blue_win_41_wrong,fill_value=0)

# COUNT NUMBER OF TIMES JUDGE 3 WAS WRONG ON 4-1 DECISIONS
#-----------------------------------------------------------------------------------------------------------------------
j3_red_win_14_wrong = big_df["judge3_name"][( big_df["j3_redscore"] > big_df["j3_bluescore"] )\
                                        & ( big_df["j1_redscore"] < big_df["j1_bluescore"] )\
                                        & ( big_df["j2_redscore"] < big_df["j2_bluescore"] )\
                                        & ( big_df["j4_redscore"] < big_df["j4_bluescore"] )\
                                        & ( big_df["j5_redscore"] < big_df["j5_bluescore"] )\
                                        ].value_counts()

j3_blue_win_41_wrong = big_df["judge3_name"][( big_df["j3_redscore"] < big_df["j3_bluescore"] )\
                                        & ( big_df["j1_redscore"] > big_df["j1_bluescore"] )\
                                        & ( big_df["j2_redscore"] > big_df["j2_bluescore"] )\
                                        & ( big_df["j4_redscore"] > big_df["j4_bluescore"] )\
                                        & ( big_df["j5_redscore"] > big_df["j5_bluescore"] )\
                                        ].value_counts()

official_series_j3_14_41_wrong = j3_red_win_14_wrong.add(j3_blue_win_41_wrong,fill_value=0)

# COUNT NUMBER OF TIMES JUDGE 4 WAS WRONG ON 4-1 DECISIONS
#-----------------------------------------------------------------------------------------------------------------------
j4_red_win_14_wrong = big_df["judge4_name"][( big_df["j4_redscore"] > big_df["j4_bluescore"] )\
                                        & ( big_df["j1_redscore"] < big_df["j1_bluescore"] )\
                                        & ( big_df["j2_redscore"] < big_df["j2_bluescore"] )\
                                        & ( big_df["j3_redscore"] < big_df["j3_bluescore"] )\
                                        & ( big_df["j5_redscore"] < big_df["j5_bluescore"] )\
                                        ].value_counts()

j4_blue_win_41_wrong = big_df["judge4_name"][( big_df["j4_redscore"] < big_df["j4_bluescore"] )\
                                        & ( big_df["j1_redscore"] > big_df["j1_bluescore"] )\
                                        & ( big_df["j2_redscore"] > big_df["j2_bluescore"] )\
                                        & ( big_df["j3_redscore"] > big_df["j3_bluescore"] )\
                                        & ( big_df["j5_redscore"] > big_df["j5_bluescore"] )\
                                        ].value_counts()

official_series_j4_14_41_wrong = j4_red_win_14_wrong.add(j4_blue_win_41_wrong,fill_value=0)

# COUNT NUMBER OF TIMES JUDGE 5 WAS WRONG ON 4-1 DECISIONS
#-----------------------------------------------------------------------------------------------------------------------
j5_red_win_14_wrong = big_df["judge5_name"][( big_df["j5_redscore"] > big_df["j5_bluescore"] )\
                                        & ( big_df["j1_redscore"] < big_df["j1_bluescore"] )\
                                        & ( big_df["j2_redscore"] < big_df["j2_bluescore"] )\
                                        & ( big_df["j3_redscore"] < big_df["j3_bluescore"] )\
                                        & ( big_df["j4_redscore"] < big_df["j4_bluescore"] )\
                                        ].value_counts()

j5_blue_win_41_wrong = big_df["judge5_name"][( big_df["j5_redscore"] < big_df["j5_bluescore"] )\
                                        & ( big_df["j1_redscore"] > big_df["j1_bluescore"] )\
                                        & ( big_df["j2_redscore"] > big_df["j2_bluescore"] )\
                                        & ( big_df["j3_redscore"] > big_df["j3_bluescore"] )\
                                        & ( big_df["j4_redscore"] > big_df["j4_bluescore"] )\
                                        ].value_counts()

official_series_j5_14_41_wrong = j5_red_win_14_wrong.add(j5_blue_win_41_wrong,fill_value=0)

# ADD UP TOTAL NUMBER OF TIMES EACH JUDGE WAS WRONG IN 1-4 or 4-1 DECISIONS - AND CALCULATE PERCENTAGE
#-----------------------------------------------------------------------------------------------------------------------
official_series_j12_on_14_41_wrong = official_series_j1_14_41_wrong.add(official_series_j2_14_41_wrong,fill_value=0)
official_series_j123_on_14_41_wrong = official_series_j12_on_14_41_wrong.add(official_series_j3_14_41_wrong,fill_value=0)
official_series_j1234_on_14_41_wrong = official_series_j123_on_14_41_wrong.add(official_series_j4_14_41_wrong,fill_value=0)
official_series_j12345_on_14_41_wrong = official_series_j1234_on_14_41_wrong.add(official_series_j5_14_41_wrong,fill_value=0)
official_series_percent_on14_41_wrong = official_series_j12345_on_14_41_wrong/official_series_j12345_num_bouts * 100


#####################################################################################################################################
# ROUND SCORE CALCULATIONS: CHECK NUMBER OF OCCURRENCES AS A JUDGE WHERE THEIR ROUND SCORE DISAGREED WITH ALL OTHER JUDGES SCORES
#####################################################################################################################################

# Judge1-Round1
j1_red_rd1_win_14_wrong = big_df["judge1_name"][( big_df["J1r1"] > big_df["J1b1"] )\
                                        & ( big_df["J2r1"] < big_df["J2b1"] )\
                                        & ( big_df["J3r1"] < big_df["J3b1"] )\
                                        & ( big_df["J4r1"] < big_df["J4b1"] )\
                                        & ( big_df["J5r1"] < big_df["J5b1"] )\
                                        ].value_counts()
j1_blue_rd1_win_14_wrong = big_df["judge1_name"][( big_df["J1r1"] < big_df["J1b1"] )\
                                        & ( big_df["J2r1"] > big_df["J2b1"] )\
                                        & ( big_df["J3r1"] > big_df["J3b1"] )\
                                        & ( big_df["J4r1"] > big_df["J4b1"] )\
                                        & ( big_df["J5r1"] > big_df["J5b1"] )\
                                        ].value_counts()
j1_rd1_win_14_wrong = j1_red_rd1_win_14_wrong.add(j1_blue_rd1_win_14_wrong,fill_value=0)

#-----------------------------------------------------------------------------------------------------------------------------------

# Judge1-Round2
j1_red_rd2_win_14_wrong = big_df["judge1_name"][( big_df["J1r2"] > big_df["J1b2"] )\
                                        & ( big_df["J2r2"] < big_df["J2b2"] )\
                                        & ( big_df["J3r2"] < big_df["J3b2"] )\
                                        & ( big_df["J4r2"] < big_df["J4b2"] )\
                                        & ( big_df["J5r2"] < big_df["J5b2"] )\
                                        ].value_counts()
j1_blue_rd2_win_14_wrong = big_df["judge1_name"][( big_df["J1r2"] < big_df["J1b2"] )\
                                        & ( big_df["J2r2"] > big_df["J2b2"] )\
                                        & ( big_df["J3r2"] > big_df["J3b2"] )\
                                        & ( big_df["J4r2"] > big_df["J4b2"] )\
                                        & ( big_df["J5r2"] > big_df["J5b2"] )\
                                        ].value_counts()
j1_rd2_win_14_wrong = j1_red_rd2_win_14_wrong.add(j1_blue_rd2_win_14_wrong,fill_value=0)

#-----------------------------------------------------------------------------------------------------------------------------------

# Judge1-Round3
j1_red_rd3_win_14_wrong = big_df["judge1_name"][( big_df["J1r3"] > big_df["J1b3"] )\
                                        & ( big_df["J2r3"] < big_df["J2b3"] )\
                                        & ( big_df["J3r3"] < big_df["J3b3"] )\
                                        & ( big_df["J4r3"] < big_df["J4b3"] )\
                                        & ( big_df["J5r3"] < big_df["J5b3"] )\
                                        ].value_counts()
j1_blue_rd3_win_14_wrong = big_df["judge1_name"][( big_df["J1r3"] < big_df["J1b3"] )\
                                        & ( big_df["J2r3"] > big_df["J2b3"] )\
                                        & ( big_df["J3r3"] > big_df["J3b3"] )\
                                        & ( big_df["J4r3"] > big_df["J4b3"] )\
                                        & ( big_df["J5r3"] > big_df["J5b3"] )\
                                        ].value_counts()
j1_rd3_win_14_wrong = j1_red_rd3_win_14_wrong.add(j1_blue_rd3_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge1-Round4
j1_red_rd4_win_14_wrong = big_df["judge1_name"][( big_df["J1r4"] > big_df["J1b4"] )\
                                        & ( big_df["J2r4"] < big_df["J2b4"] )\
                                        & ( big_df["J3r4"] < big_df["J3b4"] )\
                                        & ( big_df["J4r4"] < big_df["J4b4"] )\
                                        & ( big_df["J5r4"] < big_df["J5b4"] )\
                                        ].value_counts()
j1_blue_rd4_win_14_wrong = big_df["judge1_name"][( big_df["J1r4"] < big_df["J1b4"] )\
                                        & ( big_df["J2r4"] > big_df["J2b4"] )\
                                        & ( big_df["J3r4"] > big_df["J3b4"] )\
                                        & ( big_df["J4r4"] > big_df["J4b4"] )\
                                        & ( big_df["J5r4"] > big_df["J5b4"] )\
                                        ].value_counts()
j1_rd4_win_14_wrong = j1_red_rd4_win_14_wrong.add(j1_blue_rd4_win_14_wrong,fill_value=0)


j1_rds12_win_14_wrong = j1_rd1_win_14_wrong.add(j1_rd2_win_14_wrong,fill_value=0)
j1_rds123_win_14_wrong = j1_rds12_win_14_wrong.add(j1_rd3_win_14_wrong,fill_value=0)
j1_rds1234_win_14_wrong = j1_rds123_win_14_wrong.add(j1_rd4_win_14_wrong,fill_value=0)
#print(j1_rds1234_win_14_wrong)

#***********************************************************************************************************************************
#***********************************************************************************************************************************

# Judge2-Round1
#-----------------------------------------------------------------------------------------------------------------------------------
j2_red_rd1_win_14_wrong = big_df["judge2_name"][( big_df["J2r1"] > big_df["J2b1"] )\
                                        & ( big_df["J1r1"] < big_df["J1b1"] )\
                                        & ( big_df["J3r1"] < big_df["J3b1"] )\
                                        & ( big_df["J4r1"] < big_df["J4b1"] )\
                                        & ( big_df["J5r1"] < big_df["J5b1"] )\
                                        ].value_counts()
j2_blue_rd1_win_14_wrong = big_df["judge2_name"][( big_df["J2r1"] < big_df["J2b1"] )\
                                        & ( big_df["J1r1"] > big_df["J1b1"] )\
                                        & ( big_df["J3r1"] > big_df["J3b1"] )\
                                        & ( big_df["J4r1"] > big_df["J4b1"] )\
                                        & ( big_df["J5r1"] > big_df["J5b1"] )\
                                        ].value_counts()
j2_rd1_win_14_wrong = j2_red_rd1_win_14_wrong.add(j2_blue_rd1_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge2-Round2
j2_red_rd2_win_14_wrong = big_df["judge2_name"][( big_df["J2r2"] > big_df["J2b2"] )\
                                        & ( big_df["J1r2"] < big_df["J1b2"] )\
                                        & ( big_df["J3r2"] < big_df["J3b2"] )\
                                        & ( big_df["J4r2"] < big_df["J4b2"] )\
                                        & ( big_df["J5r2"] < big_df["J5b2"] )\
                                        ].value_counts()
j2_blue_rd2_win_14_wrong = big_df["judge2_name"][( big_df["J2r2"] < big_df["J2b2"] )\
                                        & ( big_df["J1r2"] > big_df["J1b2"] )\
                                        & ( big_df["J3r2"] > big_df["J3b2"] )\
                                        & ( big_df["J4r2"] > big_df["J4b2"] )\
                                        & ( big_df["J5r2"] > big_df["J5b2"] )\
                                        ].value_counts()
j2_rd2_win_14_wrong = j2_red_rd2_win_14_wrong.add(j2_blue_rd2_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge2-Round3
j2_red_rd3_win_14_wrong = big_df["judge2_name"][( big_df["J2r3"] > big_df["J2b3"] )\
                                        & ( big_df["J1r3"] < big_df["J1b3"] )\
                                        & ( big_df["J3r3"] < big_df["J3b3"] )\
                                        & ( big_df["J4r3"] < big_df["J4b3"] )\
                                        & ( big_df["J5r3"] < big_df["J5b3"] )\
                                        ].value_counts()
j2_blue_rd3_win_14_wrong = big_df["judge2_name"][( big_df["J2r3"] < big_df["J2b3"] )\
                                        & ( big_df["J1r3"] > big_df["J1b3"] )\
                                        & ( big_df["J3r3"] > big_df["J3b3"] )\
                                        & ( big_df["J4r3"] > big_df["J4b3"] )\
                                        & ( big_df["J5r3"] > big_df["J5b3"] )\
                                        ].value_counts()
j2_rd3_win_14_wrong = j2_red_rd3_win_14_wrong.add(j2_blue_rd3_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge2-Round4
j2_red_rd4_win_14_wrong = big_df["judge2_name"][( big_df["J2r4"] > big_df["J2b4"] )\
                                        & ( big_df["J1r4"] < big_df["J1b4"] )\
                                        & ( big_df["J3r4"] < big_df["J3b4"] )\
                                        & ( big_df["J4r4"] < big_df["J4b4"] )\
                                        & ( big_df["J5r4"] < big_df["J5b4"] )\
                                        ].value_counts()
j2_blue_rd4_win_14_wrong = big_df["judge2_name"][( big_df["J2r4"] < big_df["J2b4"] )\
                                        & ( big_df["J1r4"] > big_df["J1b4"] )\
                                        & ( big_df["J3r4"] > big_df["J3b4"] )\
                                        & ( big_df["J4r4"] > big_df["J4b4"] )\
                                        & ( big_df["J5r4"] > big_df["J5b4"] )\
                                        ].value_counts()
j2_rd4_win_14_wrong = j2_red_rd4_win_14_wrong.add(j2_blue_rd4_win_14_wrong,fill_value=0)


j2_rds12_win_14_wrong = j2_rd1_win_14_wrong.add(j2_rd2_win_14_wrong,fill_value=0)
j2_rds123_win_14_wrong = j2_rds12_win_14_wrong.add(j2_rd3_win_14_wrong,fill_value=0)
j2_rds1234_win_14_wrong = j2_rds123_win_14_wrong.add(j2_rd4_win_14_wrong,fill_value=0)
#print(j2_rds1234_win_14_wrong)

#***********************************************************************************************************************************
#***********************************************************************************************************************************

# Judge3-Round1
j3_red_rd1_win_14_wrong = big_df["judge3_name"][( big_df["J3r1"] > big_df["J3b1"] )\
                                        & ( big_df["J1r1"] < big_df["J1b1"] )\
                                        & ( big_df["J2r1"] < big_df["J2b1"] )\
                                        & ( big_df["J4r1"] < big_df["J4b1"] )\
                                        & ( big_df["J5r1"] < big_df["J5b1"] )\
                                        ].value_counts()
j3_blue_rd1_win_14_wrong = big_df["judge3_name"][( big_df["J3r1"] < big_df["J3b1"] )\
                                        & ( big_df["J1r1"] > big_df["J1b1"] )\
                                        & ( big_df["J2r1"] > big_df["J2b1"] )\
                                        & ( big_df["J4r1"] > big_df["J4b1"] )\
                                        & ( big_df["J5r1"] > big_df["J5b1"] )\
                                        ].value_counts()
j3_rd1_win_14_wrong = j3_red_rd1_win_14_wrong.add(j3_blue_rd1_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge3-Round2
j3_red_rd2_win_14_wrong = big_df["judge3_name"][( big_df["J3r2"] > big_df["J3b2"] )\
                                        & ( big_df["J1r2"] < big_df["J1b2"] )\
                                        & ( big_df["J2r2"] < big_df["J2b2"] )\
                                        & ( big_df["J4r2"] < big_df["J4b2"] )\
                                        & ( big_df["J5r2"] < big_df["J5b2"] )\
                                        ].value_counts()
j3_blue_rd2_win_14_wrong = big_df["judge3_name"][( big_df["J3r2"] < big_df["J3b2"] )\
                                        & ( big_df["J1r2"] > big_df["J1b2"] )\
                                        & ( big_df["J2r2"] > big_df["J2b2"] )\
                                        & ( big_df["J4r2"] > big_df["J4b2"] )\
                                        & ( big_df["J5r2"] > big_df["J5b2"] )\
                                        ].value_counts()
j3_rd2_win_14_wrong = j3_red_rd2_win_14_wrong.add(j3_blue_rd2_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge3-Round3
j3_red_rd3_win_14_wrong = big_df["judge3_name"][( big_df["J3r3"] > big_df["J3b3"] )\
                                        & ( big_df["J1r3"] < big_df["J1b3"] )\
                                        & ( big_df["J2r3"] < big_df["J2b3"] )\
                                        & ( big_df["J4r3"] < big_df["J4b3"] )\
                                        & ( big_df["J5r3"] < big_df["J5b3"] )\
                                        ].value_counts()
j3_blue_rd3_win_14_wrong = big_df["judge3_name"][( big_df["J3r3"] < big_df["J3b3"] )\
                                        & ( big_df["J1r3"] > big_df["J1b3"] )\
                                        & ( big_df["J2r3"] > big_df["J2b3"] )\
                                        & ( big_df["J4r3"] > big_df["J4b3"] )\
                                        & ( big_df["J5r3"] > big_df["J5b3"] )\
                                        ].value_counts()
j3_rd3_win_14_wrong = j3_red_rd3_win_14_wrong.add(j3_blue_rd3_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge3-Round4
j3_red_rd4_win_14_wrong = big_df["judge3_name"][( big_df["J3r4"] > big_df["J3b4"] )\
                                        & ( big_df["J1r4"] < big_df["J1b4"] )\
                                        & ( big_df["J2r4"] < big_df["J2b4"] )\
                                        & ( big_df["J4r4"] < big_df["J4b4"] )\
                                        & ( big_df["J5r4"] < big_df["J5b4"] )\
                                        ].value_counts()
j3_blue_rd4_win_14_wrong = big_df["judge3_name"][( big_df["J3r4"] < big_df["J3b4"] )\
                                        & ( big_df["J1r4"] > big_df["J1b4"] )\
                                        & ( big_df["J2r4"] > big_df["J2b4"] )\
                                        & ( big_df["J4r4"] > big_df["J4b4"] )\
                                        & ( big_df["J5r4"] > big_df["J5b4"] )\
                                        ].value_counts()
j3_rd4_win_14_wrong = j3_red_rd4_win_14_wrong.add(j3_blue_rd4_win_14_wrong,fill_value=0)


j3_rds12_win_14_wrong = j3_rd1_win_14_wrong.add(j3_rd2_win_14_wrong,fill_value=0)
j3_rds123_win_14_wrong = j3_rds12_win_14_wrong.add(j3_rd3_win_14_wrong,fill_value=0)
j3_rds1234_win_14_wrong = j3_rds123_win_14_wrong.add(j3_rd4_win_14_wrong,fill_value=0)
#print(j3_rds1234_win_14_wrong)

#***********************************************************************************************************************************
#***********************************************************************************************************************************

# Judge4-Round1
#-----------------------------------------------------------------------------------------------------------------------------------
j4_red_rd1_win_14_wrong = big_df["judge4_name"][( big_df["J4r1"] > big_df["J4b1"] )\
                                        & ( big_df["J1r1"] < big_df["J1b1"] )\
                                        & ( big_df["J2r1"] < big_df["J2b1"] )\
                                        & ( big_df["J3r1"] < big_df["J3b1"] )\
                                        & ( big_df["J5r1"] < big_df["J5b1"] )\
                                        ].value_counts()
j4_blue_rd1_win_14_wrong = big_df["judge4_name"][( big_df["J4r1"] < big_df["J4b1"] )\
                                        & ( big_df["J1r1"] > big_df["J1b1"] )\
                                        & ( big_df["J2r1"] > big_df["J2b1"] )\
                                        & ( big_df["J3r1"] > big_df["J3b1"] )\
                                        & ( big_df["J5r1"] > big_df["J5b1"] )\
                                        ].value_counts()
j4_rd1_win_14_wrong = j4_red_rd1_win_14_wrong.add(j4_blue_rd1_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge4-Round2
j4_red_rd2_win_14_wrong = big_df["judge4_name"][( big_df["J4r2"] > big_df["J4b2"] )\
                                        & ( big_df["J1r2"] < big_df["J1b2"] )\
                                        & ( big_df["J2r2"] < big_df["J2b2"] )\
                                        & ( big_df["J3r2"] < big_df["J3b2"] )\
                                        & ( big_df["J5r2"] < big_df["J5b2"] )\
                                        ].value_counts()
j4_blue_rd2_win_14_wrong = big_df["judge4_name"][( big_df["J4r2"] < big_df["J4b2"] )\
                                        & ( big_df["J1r2"] > big_df["J1b2"] )\
                                        & ( big_df["J2r2"] > big_df["J2b2"] )\
                                        & ( big_df["J3r2"] > big_df["J3b2"] )\
                                        & ( big_df["J5r2"] > big_df["J5b2"] )\
                                        ].value_counts()
j4_rd2_win_14_wrong = j4_red_rd2_win_14_wrong.add(j4_blue_rd2_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge4-Round3
j4_red_rd3_win_14_wrong = big_df["judge4_name"][( big_df["J4r3"] > big_df["J4b3"] )\
                                        & ( big_df["J1r3"] < big_df["J1b3"] )\
                                        & ( big_df["J2r3"] < big_df["J2b3"] )\
                                        & ( big_df["J3r3"] < big_df["J3b3"] )\
                                        & ( big_df["J5r3"] < big_df["J5b3"] )\
                                        ].value_counts()
j4_blue_rd3_win_14_wrong = big_df["judge4_name"][( big_df["J4r3"] < big_df["J4b3"] )\
                                        & ( big_df["J1r3"] > big_df["J1b3"] )\
                                        & ( big_df["J2r3"] > big_df["J2b3"] )\
                                        & ( big_df["J3r3"] > big_df["J3b3"] )\
                                        & ( big_df["J5r3"] > big_df["J5b3"] )\
                                        ].value_counts()
j4_rd3_win_14_wrong = j4_red_rd3_win_14_wrong.add(j4_blue_rd3_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge4-Round4
j4_red_rd4_win_14_wrong = big_df["judge4_name"][( big_df["J4r4"] > big_df["J4b4"] )\
                                        & ( big_df["J1r4"] < big_df["J1b4"] )\
                                        & ( big_df["J2r4"] < big_df["J2b4"] )\
                                        & ( big_df["J3r4"] < big_df["J3b4"] )\
                                        & ( big_df["J5r4"] < big_df["J5b4"] )\
                                        ].value_counts()
j4_blue_rd4_win_14_wrong = big_df["judge4_name"][( big_df["J4r4"] < big_df["J4b4"] )\
                                        & ( big_df["J1r4"] > big_df["J1b4"] )\
                                        & ( big_df["J2r4"] > big_df["J2b4"] )\
                                        & ( big_df["J3r4"] > big_df["J3b4"] )\
                                        & ( big_df["J5r4"] > big_df["J5b4"] )\
                                        ].value_counts()
j4_rd4_win_14_wrong = j4_red_rd4_win_14_wrong.add(j4_blue_rd4_win_14_wrong,fill_value=0)


j4_rds12_win_14_wrong = j4_rd1_win_14_wrong.add(j4_rd2_win_14_wrong,fill_value=0)
j4_rds123_win_14_wrong = j4_rds12_win_14_wrong.add(j4_rd3_win_14_wrong,fill_value=0)
j4_rds1234_win_14_wrong = j4_rds123_win_14_wrong.add(j4_rd4_win_14_wrong,fill_value=0)
#print(j4_rds1234_win_14_wrong)

#***********************************************************************************************************************************
#***********************************************************************************************************************************

# Judge5-Round1
#-----------------------------------------------------------------------------------------------------------------------------------
j5_red_rd1_win_14_wrong = big_df["judge5_name"][( big_df["J5r1"] > big_df["J5b1"] )\
                                        & ( big_df["J1r1"] < big_df["J1b1"] )\
                                        & ( big_df["J2r1"] < big_df["J2b1"] )\
                                        & ( big_df["J3r1"] < big_df["J3b1"] )\
                                        & ( big_df["J4r1"] < big_df["J4b1"] )\
                                        ].value_counts()
j5_blue_rd1_win_14_wrong = big_df["judge5_name"][( big_df["J5r1"] < big_df["J5b1"] )\
                                        & ( big_df["J1r1"] > big_df["J1b1"] )\
                                        & ( big_df["J2r1"] > big_df["J2b1"] )\
                                        & ( big_df["J3r1"] > big_df["J3b1"] )\
                                        & ( big_df["J4r1"] > big_df["J4b1"] )\
                                        ].value_counts()
j5_rd1_win_14_wrong = j5_red_rd1_win_14_wrong.add(j5_blue_rd1_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge5-Round2
j5_red_rd2_win_14_wrong = big_df["judge5_name"][( big_df["J5r2"] > big_df["J5b2"] )\
                                        & ( big_df["J1r2"] < big_df["J1b2"] )\
                                        & ( big_df["J2r2"] < big_df["J2b2"] )\
                                        & ( big_df["J3r2"] < big_df["J3b2"] )\
                                        & ( big_df["J4r2"] < big_df["J4b2"] )\
                                        ].value_counts()
j5_blue_rd2_win_14_wrong = big_df["judge5_name"][( big_df["J5r2"] < big_df["J5b2"] )\
                                        & ( big_df["J1r2"] > big_df["J1b2"] )\
                                        & ( big_df["J2r2"] > big_df["J2b2"] )\
                                        & ( big_df["J3r2"] > big_df["J3b2"] )\
                                        & ( big_df["J4r2"] > big_df["J4b2"] )\
                                        ].value_counts()
j5_rd2_win_14_wrong = j5_red_rd2_win_14_wrong.add(j5_blue_rd2_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge5-Round3
j5_red_rd3_win_14_wrong = big_df["judge5_name"][( big_df["J5r3"] > big_df["J5b3"] )\
                                        & ( big_df["J1r3"] < big_df["J1b3"] )\
                                        & ( big_df["J2r3"] < big_df["J2b3"] )\
                                        & ( big_df["J3r3"] < big_df["J3b3"] )\
                                        & ( big_df["J4r3"] < big_df["J4b3"] )\
                                        ].value_counts()
j5_blue_rd3_win_14_wrong = big_df["judge5_name"][( big_df["J5r3"] < big_df["J5b3"] )\
                                        & ( big_df["J1r3"] > big_df["J1b3"] )\
                                        & ( big_df["J2r3"] > big_df["J2b3"] )\
                                        & ( big_df["J3r3"] > big_df["J3b3"] )\
                                        & ( big_df["J4r3"] > big_df["J4b3"] )\
                                        ].value_counts()
j5_rd3_win_14_wrong = j5_red_rd3_win_14_wrong.add(j5_blue_rd3_win_14_wrong,fill_value=0)
#-----------------------------------------------------------------------------------------------------------------------------------

# Judge5-Round4
j5_red_rd4_win_14_wrong = big_df["judge5_name"][( big_df["J5r4"] > big_df["J5b4"] )\
                                        & ( big_df["J1r4"] < big_df["J1b4"] )\
                                        & ( big_df["J2r4"] < big_df["J2b4"] )\
                                        & ( big_df["J3r4"] < big_df["J3b4"] )\
                                        & ( big_df["J4r4"] < big_df["J4b4"] )\
                                        ].value_counts()
j5_blue_rd4_win_14_wrong = big_df["judge5_name"][( big_df["J5r4"] < big_df["J5b4"] )\
                                        & ( big_df["J1r4"] > big_df["J1b4"] )\
                                        & ( big_df["J2r4"] > big_df["J2b4"] )\
                                        & ( big_df["J3r4"] > big_df["J3b4"] )\
                                        & ( big_df["J4r4"] > big_df["J4b4"] )\
                                        ].value_counts()
j5_rd4_win_14_wrong = j5_red_rd4_win_14_wrong.add(j5_blue_rd4_win_14_wrong,fill_value=0)


j5_rds12_win_14_wrong = j5_rd1_win_14_wrong.add(j5_rd2_win_14_wrong,fill_value=0)
j5_rds123_win_14_wrong = j5_rds12_win_14_wrong.add(j5_rd3_win_14_wrong,fill_value=0)
j5_rds1234_win_14_wrong = j5_rds123_win_14_wrong.add(j5_rd4_win_14_wrong,fill_value=0)
#print(j5_rds1234_win_14_wrong)

#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------

# combine all WRONG ROUNDS counts
j12_rds1234_win_14_wrong = j1_rds1234_win_14_wrong.add(j2_rds1234_win_14_wrong,fill_value=0)
j123_rds1234_win_14_wrong = j12_rds1234_win_14_wrong.add(j3_rds1234_win_14_wrong,fill_value=0)
j1234_rds1234_win_14_wrong = j123_rds1234_win_14_wrong.add(j4_rds1234_win_14_wrong,fill_value=0)
j12345_rds1234_win_14_wrong = j1234_rds1234_win_14_wrong.add(j5_rds1234_win_14_wrong,fill_value=0)
j12345_percent_rds1234_win_14_wrong = j12345_rds1234_win_14_wrong/official_series_j12345_num_rounds * 100

#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------

# START TO BUILD OFFICIALS DATAFRAME
#-----------------------------------------------------------------------------------------------------------------------
officials_stats_dataframe = pd.DataFrame()
# 0,1,2,3,4,5,6,7,8,9,10,11
officials_stats_dataframe = pd.concat([official_series_referee_num_bouts, official_series_referee_num_rounds, official_series_referee_num_finals], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j12345_num_bouts], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j12345_num_wp_bouts], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j12345_num_rounds], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j1_num_bouts], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j2_num_bouts], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j3_num_bouts], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j4_num_bouts], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j5_num_bouts], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j1_wrong], axis=1)
# 12,13,14,15,16,17,18,19,20,21
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j2_wrong], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j3_wrong], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j4_wrong], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j5_wrong], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j12345_wrong], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_percent_wrong], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_j12345_on_14_41_wrong], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,official_series_percent_on14_41_wrong], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,j12345_rds1234_win_14_wrong], axis=1)
officials_stats_dataframe = pd.concat([officials_stats_dataframe,j12345_percent_rds1234_win_14_wrong], axis=1)



# REPLACE ALL NaN VALUES WITH ZERO (0) FOR CALCULATION PURPOSES
# ...and THEN RE-LABEL ALL COLUMNS WITH MEANINGFUL NAMES
# ...and SAVE TO FILE & DISPLAY OFFICIALS STATS DATAFRAME
#-----------------------------------------------------------------------------------------------------------------------
officials_stats_dataframe = officials_stats_dataframe.fillna(0)
officials_stats_dataframe.columns = ["num_refereed","num_rds_refereed","num_finals_refereed","num_bouts_judged",\
                                     "num_bouts_judged_wp","num_rnds_judged","num_j1","num_j2","num_j3","num_j4","num_j5",\
                                     "j1_wrong", "j2_wrong", "j3_wrong", "j4_wrong", "j5_wrong","num_bouts_judged_wrong",\
                                     "percent_bouts_judged_wrong","tot_14_41_wrong", "percent_14_41_wrong",\
                                     "num_rds_judged_wrong","percent_rds_judged_wrong"]
#-----------------------------------------------------------------------------------------------------------------------
officials_stats_dataframe.to_csv(datapath+"/stats/officials_stats_dataframe.csv",sep=';') # just used to check output of DATAFRAME BUILD above
print("\nofficials_stats_dataframe:\n",officials_stats_dataframe)
print("officials_stats_dataframe:  ",type(officials_stats_dataframe), officials_stats_dataframe.shape)
#print("\n","*"*100) # JUST WHITESPACE
#-----------------------------------------------------------------------------------------------------------------------


#************************************************************************************************************************
# ANALYSIS: MOST APPEARANCES AS REFEREE
#************************************************************************************************************************
listof_final_appearances = officials_stats_dataframe[["num_refereed"]]
most_ref_appearances = listof_final_appearances.nlargest(50,"num_refereed")
print("\nTHE TOP 50 BUSIEST REFEREES ARE:\n\n",most_ref_appearances)
print("\n","*"*100) # JUST WHITESPACE

#************************************************************************************************************************
# ANALYSIS: MOST APPEARANCES AS REFEREE IN A FINAL
#************************************************************************************************************************
listof_final_appearances = officials_stats_dataframe[["num_refereed","num_finals_refereed"]]
most_final_appearances = listof_final_appearances.nlargest(30,"num_finals_refereed")
print("\nTHE TOP 30 MOST APPEARANCES AS A REFEREE IN A FINAL ARE:\n\n",most_final_appearances)
print("\n","*"*100) # JUST WHITESPACE

#************************************************************************************************************************
# ANALYSIS: MOST APPEARANCES AS A JUDGE - OVERALL AND AT EACH POSITION AROUND THE RING
#************************************************************************************************************************
listof_appearances_as_judge = officials_stats_dataframe[["num_bouts_judged","num_j1","num_j2","num_j3","num_j4","num_j5"]]
most_appearances_as_judge = listof_appearances_as_judge.nlargest(100,"num_bouts_judged")
print("\nTHE TOP 100 BUSIEST JUDGES:\n\n",most_appearances_as_judge)
print("\n","*"*100) # JUST WHITESPACE

#************************************************************************************************************************
# ANALYSIS: MOST WRONG DECISIONS AS A JUDGE ACTUAL & PERCENTAGE - ONLY JUDGED MORE THAN 'n' TIMES
#************************************************************************************************************************
n = 100;
listof_all_wrong_decisions = officials_stats_dataframe[["num_bouts_judged","num_bouts_judged_wp","num_bouts_judged_wrong",\
                                                        "percent_bouts_judged_wrong","num_rnds_judged","num_rds_judged_wrong",\
                                                        "percent_rds_judged_wrong","tot_14_41_wrong","percent_14_41_wrong",\
                                                        "j1_wrong","j2_wrong","j3_wrong","j4_wrong","j5_wrong"]]

listof_all_wrong_decisions_with_morethan50judged = listof_all_wrong_decisions[listof_all_wrong_decisions["num_bouts_judged_wp"]>=n]
most_wrong_decisions = listof_all_wrong_decisions_with_morethan50judged.nlargest(50,"percent_bouts_judged_wrong")
print("\nJUDGES WITH THE HIGHEST NUMBER OF WRONG DECISIONS (judged more than %d times):\n\n%s" % (n,most_wrong_decisions))
print("\n","*"*100) # JUST WHITESPACE

