###############################################################################################################
# Filename: boxer_analysis.py
# Author: Paul Williamson
# Date: 11/10/2017
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
from statistics import mode
from collections import Counter

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
#print(bouts_dataframe)

number_of_sessions_per_competition = bouts_dataframe.groupby("competition_name")["competition_session_num"].nunique()
#print("\nnumber_of_sessions_per_competition is:\n",number_of_sessions_per_competition)
#print("\n",type(number_of_sessions_per_competition))

number_of_weight_cats_per_competition = bouts_dataframe.groupby("competition_name")["competition_bout_weight_(KG)"].nunique()
#print("\nnumber_of_sessions_per_competition is:\n",number_of_sessions_per_competition)

number_of_bouts_per_competition = bouts_dataframe.groupby("competition_name")["pk_bout_index"].count()
#print("\nnumber_of_bouts_per_competition is:\n",number_of_bouts_per_competition)

avg_number_of_bouts_per_session = (number_of_bouts_per_competition) /(number_of_sessions_per_competition)
#print("\navg_number_of_bouts_per_session is:\n",avg_number_of_bouts_per_session)

number_of_rounds_per_competition = bouts_dataframe.groupby("competition_name")["number_of_rounds"].sum()
#print("\nnumber_of_rounds_per_competition is:\n",number_of_rounds_per_competition)

avg_number_of_rounds_per_competition = (number_of_rounds_per_competition)/(number_of_bouts_per_competition)
#print("\navg_number_of_rounds_per_competition:\n",avg_number_of_rounds_per_competition)

bouts_dataframe_count_results_wp = bouts_dataframe["competition_name"][bouts_dataframe["result_text"]=="WP"].value_counts()
#print("\nbouts_dataframe_count_results_wp:\n",bouts_dataframe_count_results_wp) # display pandas series

bouts_dataframe_count_results_not_wp = bouts_dataframe["competition_name"][bouts_dataframe["result_text"]!="WP"].value_counts()
#print("\nbouts_dataframe_count_results_not_wp:\n",bouts_dataframe_count_results_not_wp) # display pandas series

bouts_dataframe_count_results_rsc = bouts_dataframe["competition_name"][bouts_dataframe["result_text"]=="RSC"].value_counts()
#print("\nbouts_dataframe_count_results_rsc:\n",bouts_dataframe_count_results_rsc) # display pandas series

bouts_dataframe_count_results_tko = bouts_dataframe["competition_name"][bouts_dataframe["result_text"]=="TKO"].value_counts()
#print("\nbouts_dataframe_count_results_tko:\n",bouts_dataframe_count_results_tko) # display pandas series

bouts_dataframe_count_results_rsci = bouts_dataframe["competition_name"][bouts_dataframe["result_text"]=="RSC-I"].value_counts()
#print("\nbouts_dataframe_count_results_rsci:\n",bouts_dataframe_count_results_rsci) # display pandas series

bouts_dataframe_count_results_tkoi = bouts_dataframe["competition_name"][bouts_dataframe["result_text"]=="TKO-I"].value_counts()
#print("\nbouts_dataframe_count_results_tkoi:\n",bouts_dataframe_count_results_tkoi) # display pandas series

bouts_dataframe_count_results_ko = bouts_dataframe["competition_name"][bouts_dataframe["result_text"]=="KO"].value_counts()
#print("\nbouts_dataframe_count_results_ko:\n",bouts_dataframe_count_results_ko) # display pandas series

bouts_dataframe_count_results_wo = bouts_dataframe["competition_name"][bouts_dataframe["result_text"]=="WO"].value_counts()
#print("\nbouts_dataframe_count_results_wo:\n",bouts_dataframe_count_results_wo) # display pandas series

bouts_dataframe_count_results_abd = bouts_dataframe["competition_name"][bouts_dataframe["result_text"]=="ABD"].value_counts()
#print("\nbouts_dataframe_count_results_wo:\n",bouts_dataframe_count_results_wo) # display pandas series

number_of_referees_per_competition = bouts_dataframe.groupby("competition_name")["referee_name"].nunique()
#print("\nNumber_of_referees_per_competition is:\n",number_of_referees_per_competition)

#--------------------------------------------------------------------------------------------------------------------------------------
number_of_entries_dict = {}
most_comtested_weights_dict = {}
number_of_judges_dict = {}
# Group the dataframe by competition name, and iterate over data from each competition
for comp_name, comp_data in bouts_dataframe.groupby("competition_name"):
    #print("\nCOMP_NAME:\n",comp_name)  # print the name of the competition
    #print("\nCOMP_DATA:\n",comp_data) # print the data for that competition
    rednames = list(comp_data["red_boxer_name"])
    bluenames = list(comp_data["blue_boxer_name"])
    allredbluenames = list(set(rednames).union(bluenames))
    this_event_num_entries = len(allredbluenames)

#--------------------------------------------------------------------------------------------------------------------------------------
    bouts_per_weight = Counter(list(comp_data["competition_bout_weight_(KG)"]))
    try:
        #most_contested_weight = mode(weights)
        most_contested_weight = bouts_per_weight.most_common(2)
    except:
        #most_contested_weight = str(bouts_per_weight.most_common(2))
        most_contested_weight = "Multiple"
    #print(most_contested_weight)

#--------------------------------------------------------------------------------------------------------------------------------------
    j1names = list(comp_data["judge1_name"])
    j2names = list(comp_data["judge2_name"])
    j3names = list(comp_data["judge3_name"])
    j4names = list(comp_data["judge4_name"])
    j5names = list(comp_data["judge5_name"])
    alljudgenames = list(set(j1names).union(j2names).union(j3names).union(j4names).union(j5names))
    this_event_num_judges = len(alljudgenames)

#--------------------------------------------------------------------------------------------------------------------------------------
    number_of_entries_dict[comp_name] = this_event_num_entries if comp_name not in number_of_entries_dict else number_of_entries_dict[comp_name]
    most_comtested_weights_dict[comp_name] = most_contested_weight if comp_name not in most_comtested_weights_dict else most_comtested_weights_dict[comp_name]
    number_of_judges_dict[comp_name] = this_event_num_judges if comp_name not in number_of_judges_dict else number_of_judges_dict[comp_name]

#--------------------------------------------------------------------------------------------------------------------------------------
number_of_entries_per_competition = pd.Series(number_of_entries_dict)
#print(number_of_entries_per_competition)
most_contested_weights_per_competition = pd.Series(most_comtested_weights_dict)
#print(most_common_weights_per_competition)
number_of_officials_per_competition = pd.Series(number_of_judges_dict)
#print(number_of_judges_per_competition)

bouts_to_officials_ratio = number_of_bouts_per_competition/number_of_officials_per_competition
#print("\nNumber_of_referees_per_competition is:\n",number_of_referees_per_competition)


# BUILD COMPETITION DATAFRAME
competition_stats_dataframe = pd.DataFrame()
competition_stats_dataframe = pd.concat([competition_stats_dataframe, number_of_entries_per_competition], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, number_of_weight_cats_per_competition], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, most_contested_weights_per_competition], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, number_of_bouts_per_competition], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, number_of_sessions_per_competition], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, avg_number_of_bouts_per_session], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, number_of_rounds_per_competition], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, avg_number_of_rounds_per_competition], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, bouts_dataframe_count_results_wp], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, bouts_dataframe_count_results_not_wp], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, bouts_dataframe_count_results_rsc], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, bouts_dataframe_count_results_rsci], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, bouts_dataframe_count_results_tko], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, bouts_dataframe_count_results_tkoi], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, bouts_dataframe_count_results_ko], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, bouts_dataframe_count_results_abd], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, bouts_dataframe_count_results_wo], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, number_of_referees_per_competition], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, number_of_officials_per_competition], axis=1)
competition_stats_dataframe = pd.concat([competition_stats_dataframe, bouts_to_officials_ratio], axis=1)

# REPLACE ALL NaN & Inf VALUES WITH ZERO (0) FOR CALCULATION PURPOSES
# RENAME ALL COLUMNS WITH MEANINGFUL LABELS
# ...and SAVE TO FILE & DISPLAY OFFICIALS STATS DATAFRAME
#-----------------------------------------------------------------------------------------------------------------------
competition_stats_dataframe = competition_stats_dataframe.replace([np.inf, -np.inf], np.nan)
competition_stats_dataframe = competition_stats_dataframe.fillna(0)
competition_stats_dataframe.columns = ["num_entries","num_wt_cats","most_bouts_per_wt","num_bouts","num_sess","avg_bouts",\
                                       "num_rds","avg_rds","num_wp","num_!= wp",\
                                       "num_rsc","num_rsc-i","num_tko","num_tko-i",\
                                       "num_ko", "num_abd","num_wo","num_refs","num_officials","bouts_offs_ratio"]

print("competition_stats_dataframe:\n",competition_stats_dataframe)
print("competition_stats_dataframe:  ",type(competition_stats_dataframe), competition_stats_dataframe.shape)
print("\n","*"*100) # JUST WHITESPACE
competition_stats_dataframe.to_csv(datapath+"/stats/competition_stats_dataframe.csv",sep=';') # just used to check output of DATAFRAME BUILD above
