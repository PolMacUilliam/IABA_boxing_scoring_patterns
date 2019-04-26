###############################################################################################################
# Filename: boxer_analysis.py
# Author: Paul Williamson
# Date: 13/10/2017
################################################################################################################
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

bouts_dataframe = pd.read_csv(datapath+"/bouts_dbase_table.csv", sep=';')
bouts_dataframe.set_index('pk_bout_index', inplace=True)
#print(bouts_dataframe)

boutscores_dataframe = pd.read_csv(datapath+"/boutscores_dbase_table.csv", sep=';')
boutscores_dataframe.set_index('pk_boutscores_index', inplace=True)
#print(boutscores_dataframe)

######################################################################################################################
# BOXERS DATAFRAME
######################################################################################################################

# COUNT EACH BOXERS APPEARANCE
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_red = bouts_dataframe["red_boxer_name"].value_counts()
boxers_series_blue = bouts_dataframe["blue_boxer_name"].value_counts()
boxers_series_num_bouts = boxers_series_red.add(boxers_series_blue,fill_value=0)
#print("\n boxers_series_num_bouts is:\n",boxers_series_num_bouts)
#boxers_series_num_bouts.to_csv(datapath+"/stats/boxers_series_num_bouts.csv",sep=';') # just used to check output of series

# GET NUMBER OF ROUNDS RECORDED FOR EACH BOXER
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_count_red_rounds = bouts_dataframe.groupby("red_boxer_name")["number_of_rounds"].sum()
#print("\n boxers_series_count_red_rounds: ",boxers_series_count_red_rounds)

boxers_series_count_blue_rounds = bouts_dataframe.groupby("blue_boxer_name")["number_of_rounds"].sum()
#print("\n boxers_series_count_blue_rounds: ",boxers_series_count_blue_rounds)

boxers_series_count_rounds = boxers_series_count_red_rounds.add(boxers_series_count_blue_rounds,fill_value=0)
#print("\n boxers_series_count_rounds: ",boxers_series_count_rounds)

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

# COUNT EACH BOXERS WINS
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_count_wins = bouts_dataframe["winner"].value_counts()
#print("\nboxers_series_count_wins is:\n",boxers_series_count_wins)

# GET NUMBER OF WINS AS PERCENTAGE OF APPEARANCES
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_calculate_win_percent = (boxers_series_count_wins/boxers_series_num_bouts)*100

# COUNT NUMBER OF TIMES EACH BOXER WON BY WP IN RED CORNER
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_red_wp_winner = bouts_dataframe[ bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"] ] # get red winners only
boxers_series_red_wp_winner = boxers_series_red_wp_winner[ boxers_series_red_wp_winner["result_text"] == "WP" ] # get 'wp' points wins only
#red_wp_winner_series = bouts_dataframe[(bouts_dataframe['winner'] == bouts_dataframe["red_boxer_name"]) & (bouts_dataframe['result_text'] == "WP")]
boxers_series_red_wp_winner = boxers_series_red_wp_winner["winner"].value_counts() # get just the value counts of each 'winner'
#print(red_wp_winner_series)
#boxers_series_red_wp_winner.to_csv(datapath+"/boxers_series_red_wp_winner.csv",sep=';') # just used to check output above

# COUNT NUMBER OF TIMES EACH BOXER WON BY WP IN BLUE CORNER
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_blue_wp_winner = bouts_dataframe[ bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"] ] # get blue winners only
boxers_series_blue_wp_winner = boxers_series_blue_wp_winner[ boxers_series_blue_wp_winner["result_text"] == "WP" ] # get 'wp' points wins only
#blue_wp_winner_series = bouts_dataframe[(bouts_dataframe['winner'] == bouts_dataframe["blue_boxer_name"]) & (bouts_dataframe['result_text'] == "WP")]
boxers_series_blue_wp_winner = boxers_series_blue_wp_winner["winner"].value_counts() # get just the value counts of each 'winner'
#print(blue_wp_winner_series)
#boxers_series_blue_wp_winner.to_csv(datapath+"/boxers_series_blue_wp_winner.csv",sep=';') # just used to check output above

# COUNT NUMBER OF TIMES EACH BOXER WON BY WP "red PLUS blue"
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_calculate_wp_wins = boxers_series_red_wp_winner.add(boxers_series_blue_wp_winner,fill_value=0)

# COUNT NUMBER OF TIMES EACH BOXER WON BY TKO or RSC "tko PLUS rsc"
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_wins_by_tko = bouts_dataframe["winner"][bouts_dataframe["result_text"] == "TKO" ].value_counts()
boxers_series_wins_by_rsc = bouts_dataframe["winner"][bouts_dataframe["result_text"] == "RSC" ].value_counts()
boxers_series_wins_by_tko_plus_rsc = boxers_series_wins_by_tko.add(boxers_series_wins_by_rsc,fill_value=0)
#print(boxers_series_wins_by_tko_plus_rsc)
#boxers_series_wins_by_tko_plus_rsc.to_csv(datapath+"/stats/boxers_series_wins_by_tko_plus_rsc.csv",sep=';') # just used to check output

# COUNT NUMBER OF TIMES EACH BOXER WON BY TKO-I or RSC-I "tko PLUS rsc"
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_wins_by_tkoi = bouts_dataframe["winner"][bouts_dataframe["result_text"] == "TKO-I" ].value_counts()
boxers_series_wins_by_rsci = bouts_dataframe["winner"][bouts_dataframe["result_text"] == "RSC-I" ].value_counts()
boxers_series_wins_by_tkoi_plus_rsci = boxers_series_wins_by_tkoi.add(boxers_series_wins_by_rsci,fill_value=0)
#print(boxers_series_wins_by_tkoi_plus_rsci)
#boxers_series_wins_by_tkoi_plus_rsci.to_csv(datapath+"/stats/boxers_series_wins_by_tkoi_plus_rsci.csv",sep=';') # just used to check output

# COUNT NUMBER OF TIMES EACH BOXER WON BY 'KO'
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_wins_by_ko = bouts_dataframe["winner"][bouts_dataframe["result_text"] == "KO" ].value_counts()
#print(boxers_series_wins_by_ko)
#boxers_series_wins_by_ko.to_csv(datapath+"/stats/boxers_series_wins_by_ko.csv",sep=';') # just used to check output

#  COUNT NUMBER OF TIMES EACH BOXER WON BY 'AB' or 'RET'
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_wins_by_abd = bouts_dataframe["winner"][bouts_dataframe["result_text"] == "ABD" ].value_counts()
boxers_series_wins_by_ret = bouts_dataframe["winner"][bouts_dataframe["result_text"] == "RET" ].value_counts()
boxers_series_wins_by_abd_plus_ret = boxers_series_wins_by_abd.add(boxers_series_wins_by_ret,fill_value=0)
#print(boxers_series_wins_by_abd_plus_ret)
#boxers_series_wins_by_abd_plus_ret.to_csv(datapath+"/stats/boxers_series_wins_by_abd_plus_ret.csv",sep=';') # just used to check output

# COUNT NUMBER OF TIMES EACH BOXER WON BY 'WO'
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_wins_by_wo = bouts_dataframe["winner"][bouts_dataframe["result_text"] == "WO" ].value_counts()
#print(boxers_series_wins_by_wo)
#boxers_series_wins_by_wo.to_csv(datapath+"/stats/boxers_series_wins_by_wo.csv",sep=';') # just used to check output

# COUNT NUMBER OF TIMES EACH BOXER WON BY 'DSQ'
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_wins_by_dsq = bouts_dataframe["winner"][bouts_dataframe["result_text"] == "DSQ" ].value_counts()
#print(boxers_series_wins_by_dsq)
#boxers_series_wins_by_dsq.to_csv(datapath+"/stats/boxers_series_wins_by_dsq.csv",sep=';') # just used to check output

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

# CALCULATE TOTAL LOSS COUNT FOR EACH BOXER
#-----------------------------------------------------------------------------------------------------------------------
boxers_series_red_losses = bouts_dataframe["red_boxer_name"][ bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"] ].value_counts()
boxers_series_blue_losses = bouts_dataframe["blue_boxer_name"][ bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"] ].value_counts()
boxers_series_total_losses = boxers_series_red_losses.add(boxers_series_blue_losses,fill_value=0)
#print(boxers_series_total_losses)

# COUNT NUMBER OF TIMES EACH BOXER LOST BY 'WP'
#--------------------------------------------------------------------------------------------------------------------------------
boxers_series_red_wp_loss = bouts_dataframe["red_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "WP") ].value_counts()
boxers_series_blue_wp_loss = bouts_dataframe["blue_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "WP") ].value_counts()

boxers_series_total_wp_losses = boxers_series_red_wp_loss.add(boxers_series_blue_wp_loss,fill_value = 0)

# COUNT NUMBER OF TIMES EACH BOXER LOST BY 'RSC' or 'TKO'
#--------------------------------------------------------------------------------------------------------------------------------
boxers_series_red_rsc_loss = bouts_dataframe["red_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "RSC") ].value_counts()
boxers_series_red_tko_loss = bouts_dataframe["red_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "TKO") ].value_counts()
boxers_series_red_rsc_plus_tko_loss = boxers_series_red_rsc_loss.add(boxers_series_red_tko_loss,fill_value = 0)

boxers_series_blue_rsc_loss = bouts_dataframe["blue_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "RSC") ].value_counts()
boxers_series_blue_tko_loss = bouts_dataframe["blue_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "TKO") ].value_counts()
boxers_series_blue_rsc_plus_tko_loss = boxers_series_blue_rsc_loss.add(boxers_series_blue_tko_loss,fill_value = 0)

boxers_series_total_rsc_tko_losses = boxers_series_red_rsc_plus_tko_loss.add(boxers_series_blue_rsc_plus_tko_loss,fill_value=0)

# COUNT NUMBER OF TIMES EACH BOXER LOST BY 'RSC-I' or 'TKO-I'
#--------------------------------------------------------------------------------------------------------------------------------
boxers_series_red_rsci_loss = bouts_dataframe["red_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "RSC-I") ].value_counts()
boxers_series_red_tkoi_loss = bouts_dataframe["red_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "TKO-I") ].value_counts()
boxers_series_red_rsci_plus_tkoi_loss = boxers_series_red_rsci_loss.add(boxers_series_red_tkoi_loss,fill_value = 0)

boxers_series_blue_rsci_loss = bouts_dataframe["blue_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "RSC-I") ].value_counts()
boxers_series_blue_tkoi_loss = bouts_dataframe["blue_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "TKO-I") ].value_counts()
boxers_series_blue_rsci_plus_tkoi_loss = boxers_series_blue_rsci_loss.add(boxers_series_blue_tkoi_loss,fill_value = 0)

boxers_series_total_rsci_tkoi_losses = boxers_series_red_rsci_plus_tkoi_loss.add(boxers_series_blue_rsci_plus_tkoi_loss,fill_value=0)

# COUNT NUMBER OF TIMES EACH BOXER LOST BY 'KO'
#--------------------------------------------------------------------------------------------------------------------------------
boxers_series_red_ko_loss = bouts_dataframe["red_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "KO") ].value_counts()

boxers_series_blue_ko_loss = bouts_dataframe["blue_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "KO") ].value_counts()

boxers_series_total_ko_loss = boxers_series_red_ko_loss.add(boxers_series_blue_ko_loss,fill_value=0)

# COUNT NUMBER OF TIMES EACH BOXER LOST BY 'ABD' or 'RET'
#--------------------------------------------------------------------------------------------------------------------------------
boxers_series_red_abd_loss = bouts_dataframe["red_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "ABD") ].value_counts()
boxers_series_red_ret_loss = bouts_dataframe["red_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "RET") ].value_counts()
boxers_series_red_abd_plus_ret_loss = boxers_series_red_abd_loss.add(boxers_series_red_ret_loss,fill_value=0)

boxers_series_blue_abd_loss = bouts_dataframe["blue_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "ABD") ].value_counts()
boxers_series_blue_ret_loss = bouts_dataframe["blue_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "RET") ].value_counts()
boxers_series_blue_abd_plus_ret_loss = boxers_series_blue_abd_loss.add(boxers_series_blue_ret_loss,fill_value=0)

boxers_series_total_abd_ret_loss = boxers_series_red_abd_plus_ret_loss.add(boxers_series_blue_abd_plus_ret_loss,fill_value=0)

# COUNT NUMBER OF TIMES EACH BOXER LOST BY 'WO'
#--------------------------------------------------------------------------------------------------------------------------------
boxers_series_red_wo_loss = bouts_dataframe["red_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "WO") ].value_counts()
boxers_series_blue_wo_loss = bouts_dataframe["blue_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "WO") ].value_counts()

boxers_series_total_wo_loss = boxers_series_red_wo_loss.add(boxers_series_blue_wo_loss,fill_value=0)

# COUNT NUMBER OF TIMES EACH BOXER LOST BY 'DSQ'
#--------------------------------------------------------------------------------------------------------------------------------
boxers_series_red_dsq_loss = bouts_dataframe["red_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "DSQ") ].value_counts()

boxers_series_blue_dsq_loss = bouts_dataframe["blue_boxer_name"][(bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])\
                                  & (bouts_dataframe["result_text"] == "DSQ") ].value_counts()

boxers_series_total_dsq_loss = boxers_series_red_dsq_loss.add(boxers_series_blue_dsq_loss,fill_value=0)

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

# COUNT NUMBER OF TIMES EACH BOXER APPEARED IN A 'FINAL'
#--------------------------------------------------------------------------------------------------------------------------------
boxers_series_red_finals =  bouts_dataframe["red_boxer_name"][bouts_dataframe["competition_session_name"] == "Finals"].value_counts()
boxers_series_blue_finals =  bouts_dataframe["blue_boxer_name"][bouts_dataframe["competition_session_name"] == "Finals"].value_counts()

boxers_series_total_finals = boxers_series_red_finals.add(boxers_series_blue_finals,fill_value=0)

# COUNT NUMBER OF TIMES EACH BOXER WON IN 'FINAL'
#--------------------------------------------------------------------------------------------------------------------------------
boxers_series_red_finals_won =  bouts_dataframe["red_boxer_name"][(bouts_dataframe["competition_session_name"] == "Finals") & (bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])].value_counts()
boxers_series_blue_finals_won =  bouts_dataframe["blue_boxer_name"][(bouts_dataframe["competition_session_name"] == "Finals") & (bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])].value_counts()

boxers_series_total_finals_won = boxers_series_red_finals_won.add(boxers_series_blue_finals_won,fill_value=0)

# COUNT NUMBER OF TIMES EACH BOXER LOST IN 'FINAL'
#--------------------------------------------------------------------------------------------------------------------------------
boxers_series_red_finals_lost =  bouts_dataframe["red_boxer_name"][(bouts_dataframe["competition_session_name"] == "Finals") & (bouts_dataframe["winner"] == bouts_dataframe["blue_boxer_name"])].value_counts()
boxers_series_blue_finals_lost =  bouts_dataframe["blue_boxer_name"][(bouts_dataframe["competition_session_name"] == "Finals") & (bouts_dataframe["winner"] == bouts_dataframe["red_boxer_name"])].value_counts()

boxers_series_total_finals_lost = boxers_series_red_finals_lost.add(boxers_series_blue_finals_lost,fill_value=0)

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

#-----------------------------------------------------------------------------------------------------------------------
# BUILD BOXERS DATAFRAME
#-----------------------------------------------------------------------------------------------------------------------
boxers_stats_dataframe = pd.DataFrame()
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_num_bouts], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_count_rounds], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_count_wins], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_calculate_win_percent], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_calculate_wp_wins], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_red_wp_winner], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_blue_wp_winner], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_wins_by_tko_plus_rsc], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_wins_by_tkoi_plus_rsci], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_wins_by_ko], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_wins_by_abd_plus_ret], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_wins_by_wo], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_wins_by_dsq], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_losses], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_wp_losses], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_rsc_tko_losses], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_rsci_tkoi_losses], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_ko_loss], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_abd_ret_loss], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_wo_loss], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_dsq_loss], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_finals], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_finals_won], axis=1)
boxers_stats_dataframe = pd.concat([boxers_stats_dataframe, boxers_series_total_finals_lost], axis=1)


# REPLACE ALL NaN VALUES WITH ZERO (0) FOR CALCULATION PURPOSES
# ...and THEN RE-LABEL ALL COLUMNS WITH MEANINGFUL NAMES
# ...and SAVE TO FILE & DISPLAY BOXERS STATS DATAFRAME
##-----------------------------------------------------------------------------------------------------------------------
boxers_stats_dataframe = boxers_stats_dataframe.fillna(0)
boxers_stats_dataframe.columns = ["num_bouts","num_rds","num_wins","%win",\
                                  "wp_wins","red_wp_wins", "blue_wp_wins", "tko-rsc_wins",\
                                  "tkoi-rsci_wins","ko_wins","abd-ret_wins", "wo_wins","dsq_wins",\
                                  "num_losses", "wp_losses", "tko-rsc_losses", "tkoi-rsci_losses",\
                                  "ko_losses", "abd-ret_losses", "wo_losses","dsq_losses", "num_finals",\
                                  "finals_won","finals_lost"]
#-----------------------------------------------------------------------------------------------------------------------
boxers_stats_dataframe.to_csv(datapath+"/stats/boxers_stats_dataframe.csv",sep=';') # just used to check output of DATAFRAME BUILD above
print("boxers_stats_dataframe:\n",boxers_stats_dataframe)
print("boxers_stats_dataframe:  ",type(boxers_stats_dataframe), boxers_stats_dataframe.shape)
print("\n","*"*100) # JUST WHITESPACE
#-----------------------------------------------------------------------------------------------------------------------


# UNUSED - GET INDEX VALUES i.e. ALL BOXERS' NAMES ARE USED AS INDICES IN DATAFRAME
#-----------------------------------------------------------------------------------------------------------------------
#indices = boxers_stats_dataframe.index.get_values()
#print(indices)

# SINGLE MOST WINS - AS COMPARED TO A SINGLE VALUE OF MAX NUM OF WINS
#-----------------------------------------------------------------------------------------------------------------------
#max_wins = boxers_stats_dataframe["num wins"].max()
#max_winner = boxers_stats_dataframe[boxers_stats_dataframe["num_bouts","num_wins","num_losses","%win"]][boxers_stats_dataframe["num wins"]==max_wins]
#print("\nTHE MOST PROLIFIC WINNER IS:\n",max_winner)
#print("\n","*"*100) # JUST WHITESPACE

# MOST WINS
#-----------------------------------------------------------------------------------------------------------------------
listof_max_winners = boxers_stats_dataframe[["num_bouts","num_wins","%win"]]
max_num_wins = listof_max_winners.nlargest(10,"num_wins")
print("\nTHE TOP 10 MOST PROLIFIC WINNERS ARE:\n\n",max_num_wins)
print("\n","*"*100) # JUST WHITESPACE

# MOST COMPETITIVE
#-----------------------------------------------------------------------------------------------------------------------
listof_most_competitive = boxers_stats_dataframe[["num_bouts","num_rds","num_wins","num_losses"]]
most_competitive_boxers = listof_most_competitive.nlargest(10,"num_rds")
print("\nTHE TOP 10 MOST COMPETITIVE BOXERS BASED ON APPEARANCES & NUMBER OF ROUNDS BOXED ARE:\n\n",most_competitive_boxers)
print("\n","*"*100) # JUST WHITESPACE

# MOST WINS BY KOs...necessary to use criteria here i.e. "ko wins >=1"
#-----------------------------------------------------------------------------------------------------------------------
ALL_ko_winners = boxers_stats_dataframe[["num_bouts","num_wins","ko_wins"]][boxers_stats_dataframe["ko_wins"]>=1]
ALL_ko_winners["%KO"] = ALL_ko_winners["ko_wins"]/ALL_ko_winners["num_wins"] * 100
biggest_ko_winners = ALL_ko_winners.nlargest(10,"ko_wins")
print("\nTHE TOP KO EXPERTS ARE:\n\n",biggest_ko_winners)
print("\n","*"*100) # JUST WHITESPACE

# MOST WINS INSIDE THE DISTANCE including KOs...necessary to use criteria here i.e. "num wins >=1"
#-----------------------------------------------------------------------------------------------------------------------
ALL_stoppage_winners = boxers_stats_dataframe[["num_bouts","num_wins","%win",\
                                               "tko-rsc_wins","ko_wins","abd-ret_wins",\
                                               "tkoi-rsci_wins","dsq_wins"]][boxers_stats_dataframe["num_wins"]>=1]

ALL_stoppage_winners["ALL_stoppage_wins"] = ALL_stoppage_winners["tko-rsc_wins"]\
                                           + ALL_stoppage_winners["ko_wins"]\
                                           + ALL_stoppage_winners["abd-ret_wins"]\
                                           + ALL_stoppage_winners["tkoi-rsci_wins"]\
                                            + ALL_stoppage_winners["dsq_wins"]

ALL_stoppage_winners = ALL_stoppage_winners[["num_bouts","num_wins","ALL_stoppage_wins"]]
ALL_stoppage_winners["%Stoppages"] = ALL_stoppage_winners["ALL_stoppage_wins"]/ALL_stoppage_winners["num_wins"] * 100
biggest_stoppage_winners = ALL_stoppage_winners.nlargest(10,"ALL_stoppage_wins")
print("\nTHE TOP 10 MOST DANGEROUS BOXERS BASED ON WINS INSIDE THE DISTANCE ARE:\n\n",biggest_stoppage_winners)
print("\n","*"*100) # JUST WHITESPACE

# MOST APPEARANCES IN A FINAL
#-----------------------------------------------------------------------------------------------------------------------
listof_final_appearances = boxers_stats_dataframe[["num_bouts","num_finals","finals_won", "finals_lost"]]
most_final_appearances = listof_final_appearances.nlargest(50,"num_finals")
print("\nTHE TOP 50 MOST APPEARANCES IN A FINAL ARE:\n\n",most_final_appearances)
print("\n","*"*100) # JUST WHITESPACE

# MOST LOSSES
#-----------------------------------------------------------------------------------------------------------------------
listof_likely_journeyers = boxers_stats_dataframe[["num_bouts","num_losses","wp_losses","tko-rsc_losses","tkoi-rsci_losses",\
                                                   "ko_losses", "abd-ret_losses", "wo_losses","dsq_losses"]]
most_likely_journeyers = listof_likely_journeyers.nlargest(25,"num_losses")
print("\nTHE 25 BOXERS WITH MOST LOSSES BASED ON ALL DECISIONS:\n\n",most_likely_journeyers)
print("\n","*"*100) # JUST WHITESPACE
