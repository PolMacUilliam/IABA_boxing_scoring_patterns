import sys
import datetime
from datetime import datetime
import pyodbc
import socket
import tkinter
from tkinter import filedialog

hostname=(socket.gethostname())
print(hostname)

###############################################################################################################
# FUNCTION DEFINITIONS
###############################################################################################################
def check_date(input_date):
    for fmt in ('%Y-%m-%d','%d/%m/%Y','%d/%m/%y'): # ALLOWED DATE FORMATS
        try:
            return datetime.strptime(input_date, fmt)
        except ValueError:
            pass # IGNORE & DO NOTHING YET...
    raise ValueError('Invalid date format found: '+str(input_date))

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

###############################################################################################################
###############################################################################################################
# CREATE CONNECTION TO SQL SERVER AND DATABASE
###############################################################################################################
###############################################################################################################

if hostname == 'PAUL-PC':
    connection_str = """Driver={SQL Server}; Server=PAUL-PC\SQL12EXPRESS; Database=master; Trusted_Connection=yes; """
elif hostname == 'Cenit-PC':
    connection_str = """Driver={SQL Server}; Server=CENIT-PC; Database=master; Trusted_Connection=yes; """
else: 
    sys.exit("ERROR: Cannot connect to server!!!")

print(connection_str)

db_connection = pyodbc.connect(connection_str)
db_connection.autocommit = True
db_cursor = db_connection.cursor()

# CHECK IF DATABASE ALREADY EXISTS, IF NOT CREATE IT
# CHECK IF TABLES ALREADY EXIST, IF NOT CREATE THEM
# ATTEMPT TO WRITE ALL RECORDS INTO THE DATABASE, IF RECORD ALREADY EXISTS SKIP, OTHERWISE WRITE

'''
sql_command =   """ CREATE DATABASE ASwissTiming_WinBPM3163_IABA_Analytics """
try: db_cursor.execute(sql_command)
except pyodbc.ProgrammingError:
    print("ERROR: CREATE Database 'ASwissTiming_WinBPM314_IABA_Analytics' failed")
    sys.exit()
'''

sql_command =   """ USE ASwissTiming_WinBPM3163_IABA_Analytics """
try: db_cursor.execute(sql_command)
except pyodbc.ProgrammingError:
    print("ERROR: USE DATABASE 'ASwissTiming_WinBPM3163_IABA_Analytics' failed")
    sys.exit()




print("*"*100+"\n") # WHITESPACE

###############################################################################################################
###############################################################################################################
# CREATE SQL SERVER DATABASE TABLE "BOUTS_DBASE_TABLE"
###############################################################################################################
###############################################################################################################

if db_cursor.tables(table='bouts_dbase_table', tableType='TABLE').fetchone():
    print("\nBouts table exists already, reading dbase files...")
else:
    print("Bouts table doesn't exist yet, creating now...", end="")
    sql_command = """ CREATE TABLE bouts_dbase_table ( 
    pk_bout_index VARCHAR(255) PRIMARY KEY, 
    competition_name VARCHAR(255),
    competition_session_num INTEGER, competition_session_name VARCHAR(255),
    competition_bout_date DATE, competition_bout_time TIME(0), competition_bout_number INTEGER,
    competition_bout_weight_class VARCHAR(255), competition_bout_weight_KG VARCHAR(255),
    competition_bout_gender VARCHAR(255), competition_bout_groupname VARCHAR(255),
    red_boxer_name VARCHAR(255), red_club VARCHAR(255),
    blue_boxer_name VARCHAR(255), blue_club VARCHAR(255),
    referee_name VARCHAR(255), referee_nat VARCHAR(255),
    judge1_name VARCHAR(255), judge1_nat VARCHAR(255),
    judge2_name VARCHAR(255), judge2_nat VARCHAR(255),
    judge3_name VARCHAR(255), judge3_nat VARCHAR(255),
    judge4_name VARCHAR(255), judge4_nat VARCHAR(255),
    judge5_name VARCHAR(255), judge5_nat VARCHAR(255),
    data_format VARCHAR(255), number_of_rounds INTEGER,
    result_text VARCHAR(255), winner VARCHAR(255)  ) """

    try:
        db_cursor.execute(sql_command)
        print("Done")
    except pyodbc.ProgrammingError:
        print("\nERROR: CREATE TABLE failed")
        sys.exit()

# READ BOUTS_DBASE_TABLE FILE
with open(datapath+"/bouts_dbase_table.csv","r") as bouts_dbase_table:
    bouts_dbase_table_lines_read = bouts_dbase_table.readlines()

    # exclude column headings line [0] and dummy line [1], start reading at line [2]
    bouts_dbase_table_lines_read = bouts_dbase_table_lines_read[2:]
    print("Number of db lines read: ",len(bouts_dbase_table_lines_read))
    print("Now attempting to insert values into bouts table...", end="")

# FORMAT DATES, INSERTS NULLS AND THEN INSERT ALL VALUES INTO TABLE
for line in bouts_dbase_table_lines_read:

    # HANDLE SINGLE-QUOTES/APOSTROPHES IN TEXT VALUES BY REPLACING WITH DOUBLE SINGLE-QUOTES
    line = line.replace("'","''")

    # SPLIT EACH BOUTS LINE INTO A LIST TO AID DATA EXTRACTION
    line=line.rstrip("\n").split(";")

    # INSERT NULL VALUES INTO ANY EMPTY FIELDS
    for index in range (0,len(line)):
        if line[index] =="": line[index] = None

    pk_bout_index=line[0]; competition_name=line[1]
    competition_session_num=line[2]; competition_session_name=line[3]
    competition_bout_date=line[4]; competition_bout_time=line[5]; competition_bout_number=line[6]
    competition_bout_weight_class=line[7]; competition_bout_weight_KG=line[8]
    competition_bout_gender=line[9]; competition_bout_groupname=line[10]
    red_boxer_name=line[11]; red_club=line[12]
    blue_boxer_name=line[13]; blue_club=line[14]
    referee_name=line[15]; referee_nat=line[16]
    judge1_name=line[17]; judge1_nat=line[18]
    judge2_name=line[19]; judge2_nat=line[20]
    judge3_name=line[21]; judge3_nat=line[22]
    judge4_name=line[23]; judge4_nat=line[24]
    judge5_name=line[25]; judge5_nat=line[26]
    data_format=line[27]; number_of_rounds=line[28]
    result_text=line[29]; winner=line[30]

    # REFORMAT DATE VALUE INTO YY/MM/DD SO THAT IT FITS INTO MSSQL DATE TYPE FIELDS
    if competition_bout_date == None: pass
    else:
        competition_bout_date = check_date(competition_bout_date)
        competition_bout_date = datetime.strftime(competition_bout_date,'%Y/%m/%d')

    # INSERT VALUES INTO TABLE
    try:
        db_cursor.execute(""" INSERT into bouts_dbase_table (pk_bout_index, competition_name,competition_session_num,\
        competition_session_name,competition_bout_date, competition_bout_time, competition_bout_number,\
        competition_bout_weight_class, competition_bout_weight_KG,competition_bout_gender, competition_bout_groupname,\
        red_boxer_name, red_club,blue_boxer_name, blue_club, referee_name, referee_nat,judge1_name, judge1_nat,\
        judge2_name, judge2_nat,judge3_name, judge3_nat,judge4_name, judge4_nat,judge5_name, judge5_nat,data_format,\
        number_of_rounds, result_text, winner) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",\
                          (pk_bout_index,competition_name,competition_session_num,competition_session_name,competition_bout_date,\
                           competition_bout_time,competition_bout_number,competition_bout_weight_class,competition_bout_weight_KG,\
                           competition_bout_gender,competition_bout_groupname,red_boxer_name,red_club,blue_boxer_name,blue_club,\
                           referee_name,referee_nat,judge1_name,judge1_nat,judge2_name,judge2_nat,judge3_name,judge3_nat,\
                           judge4_name,judge4_nat,judge5_name,judge5_nat,data_format,number_of_rounds,result_text,winner)\
                          )
    # HANDLE INSERTION FAILURE
    except pyodbc.ProgrammingError:
        print("ERROR: INSERT failed")
        sys.exit()
print("Done")


###############################################################################################################
###############################################################################################################
# CREATE SQL SERVER DATABASE TABLE "COMPETITION_DBASE_TABLE"
###############################################################################################################
###############################################################################################################

if db_cursor.tables(table='competition_dbase_table', tableType='TABLE').fetchone():
    print("\nCompetition table exists already, reading dbase files...")
else:
    print("\nCompetition table doesn't exist yet, creating now...", end="")
    sql_command = """ CREATE TABLE competition_dbase_table ( 
    pk_competition_index VARCHAR(255) PRIMARY KEY, 
    competition_name VARCHAR(255), competition_venue VARCHAR(255),
    competition_firstday DATE, competition_lastday DATE,
    competition_type VARCHAR(255) ) """

    try:
        db_cursor.execute(sql_command)
        print("Done")
        print("Now reading dbase files...")
    except pyodbc.ProgrammingError:
        print("\nERROR: CREATE TABLE failed")
        sys.exit()

# READ COMPETITION_DBASE_TABLE FILE
with open(datapath+"/competition_dbase_table.csv","r") as competition_dbase_table:
    competition_dbase_table_lines_read = competition_dbase_table.readlines()

    # EXCLUDE COLUMN HEADINGS LINE [0] AND DUMMY LINE [1], START READING AT LINE [2]
    competition_dbase_table_lines_read = competition_dbase_table_lines_read[2:]
    print("Number of db lines read: ",len(competition_dbase_table_lines_read))
    print("Now attempting to insert values into competitions table...", end="")

# FORMAT DATES, INSERTS NULLS AND THEN INSERT ALL VALUES INTO TABLE
for line in competition_dbase_table_lines_read:

    # HANDLE SINGLE-QUOTES/APOSTROPHES IN TEXT VALUES BY REPLACING WITH DOUBLE SINGLE-QUOTES
    line = line.replace("'","''")

    # SPLIT EACH COMPETITION LINE INTO A LIST TO AID DATA EXTRACTION
    line=line.rstrip("\n").split(";")

    # INSERT NULL VALUES INTO ANY EMPTY FIELDS
    for index in range (0,len(line)):
        if line[index] =="": line[index] = None

    #print("\n",line)

    # EXTRACT DATA VALUES FROM THE CURRENT LINE
    pk_competition_index=line[0]; competition_name=line[1]
    competition_venue=line[2];
    competition_type = None #line[5]

    # REFORMAT DATE VALUE INTO YY/MM/DD SO THAT IT FITS INTO MSSQL DATE TYPE FIELDS
    competition_firstday=line[3];
    if competition_firstday == None: pass
    else:
        competition_firstday = check_date(competition_firstday)
        competition_firstday = datetime.strftime(competition_firstday,'%Y/%m/%d')

    competition_lastday=line[4]
    if competition_lastday == None: pass
    else:
        competition_lastday = check_date(competition_lastday)
        competition_lastday = datetime.strftime(competition_lastday,'%Y/%m/%d')

    #print("\nValues to be inserted: %s,%s,%s,%s,%s,%s" %(pk_competition_index,\
    #      competition_name,competition_venue,competition_firstday,competition_lastday,competition_type))

    # INSERT VALUES INTO TABLE
    try:
        db_cursor.execute(""" INSERT into competition_dbase_table (pk_competition_index, competition_name,\
        competition_venue, competition_firstday,competition_lastday,competition_type)\
        values (?,?,?,?,?,?)""", (pk_competition_index, competition_name,competition_venue,competition_firstday,\
                                competition_lastday,competition_type))
    # HANDLE INSERTION FAILURE
    except pyodbc.ProgrammingError:
        print("\nERROR: INSERT failed")
        sys.exit()
print("Done")


###############################################################################################################
###############################################################################################################
# CREATE SQL SERVER DATABASE TABLE "BOXERS_DBASE_TABLE"
###############################################################################################################
###############################################################################################################

if db_cursor.tables(table='boxers_dbase_table', tableType='TABLE').fetchone():
    print("\nBoxers table exists already, reading dbase files...")
else:
    print("\nBoxers table doesn't exist yet, creating now...", end="")
    sql_command = """ CREATE TABLE boxers_dbase_table ( 
    pk_boxers_index VARCHAR(255) PRIMARY KEY, 
    boxers_name VARCHAR(255), boxers_club VARCHAR(255),
    boxers_dob DATE ) """

    try:
        db_cursor.execute(sql_command)
        print("Done")
        print("Now reading dbase files...")
    except pyodbc.ProgrammingError:
        print("\nERROR: CREATE TABLE failed")
        sys.exit()

# READ BOXERS_DBASE_TABLE FILE
with open(datapath+"/boxers_dbase_table.csv","r") as boxers_dbase_table:
    boxers_dbase_table_lines_read = boxers_dbase_table.readlines()

    # EXCLUDE COLUMN HEADINGS LINE [0] AND DUMMY LINE [1], START READING AT LINE [2]
    boxers_dbase_table_lines_read = boxers_dbase_table_lines_read[2:]
    print("Number of db lines read: ",len(boxers_dbase_table_lines_read))
    print("Now attempting to insert values into boxers table...", end="")

# FORMAT DATES, INSERTS NULLS AND THEN INSERT ALL VALUES INTO TABLE
for line in boxers_dbase_table_lines_read:

    # HANDLE SINGLE-QUOTES/APOSTROPHES IN TEXT VALUES BY REPLACING WITH DOUBLE SINGLE-QUOTES
    line = line.replace("'","''")

    # SPLIT EACH BOXERS LINE INTO A LIST TO AID DATA EXTRACTION
    line=line.rstrip("\n").split(";")

    # INSERT NULL VALUES INTO ANY EMPTY FIELDS
    for index in range (0,len(line)):
        if line[index] =="": line[index] = None

    #print("\n",line)

    # EXTRACT DATA VALUES FROM THE CURRENT LINE
    pk_boxers_index=line[0]; boxers_name=line[1]
    boxers_club=line[2];
    boxers_dob = None #line[3]

    # REFORMAT DATE VALUE INTO YY/MM/DD SO THAT IT FITS INTO MSSQL DATE TYPE FIELDS
    if boxers_dob == None: pass
    else:
        boxers_dob = check_date(boxers_dob)
        boxers_dob = datetime.strftime(boxers_dob,'%Y/%m/%d')

    #print("\nValues to be inserted: %s,%s,%s,%s" %(pk_boxers_index,boxers_name,boxers_club,boxers_dob))

    # INSERT VALUES INTO TABLE
    try:
        db_cursor.execute(""" INSERT into boxers_dbase_table (pk_boxers_index, boxers_name,\
        boxers_club, boxers_dob)\
        values (?,?,?,?)""", (pk_boxers_index,boxers_name,boxers_club,boxers_dob))
    # HANDLE INSERTION FAILURE
    except pyodbc.ProgrammingError:
        print("\nERROR: INSERT failed")
        sys.exit()
print("Done")


###############################################################################################################
###############################################################################################################
# CREATE SQL SERVER DATABASE TABLE "OFFICIALS_DBASE_TABLE"
###############################################################################################################
###############################################################################################################

if db_cursor.tables(table='officials_dbase_table', tableType='TABLE').fetchone():
    print("\nOfficials table exists already, reading dbase files...")
else:
    print("\nOfficials table doesn't exist yet, creating now...", end="")
    sql_command = """ CREATE TABLE officials_dbase_table ( 
    pk_officials_index VARCHAR(255) PRIMARY KEY, 
    officials_name VARCHAR(255), officials_club VARCHAR(255),
    officials_dob DATE ) """

    try:
        db_cursor.execute(sql_command)
        print("Done")
        print("Now reading dbase files...")
    except pyodbc.ProgrammingError:
        print("\nERROR: CREATE TABLE failed")
        sys.exit()

# READ OFFICIALS_DBASE_TABLE FILE
with open(datapath+"/officials_dbase_table.csv","r") as officials_dbase_table:
    officials_dbase_table_lines_read = officials_dbase_table.readlines()

    # EXCLUDE COLUMN HEADINGS LINE [0] AND DUMMY LINE [1], START READING AT LINE [2]
    officials_dbase_table_lines_read = officials_dbase_table_lines_read[2:]
    print("Number of db lines read: ",len(officials_dbase_table_lines_read))
    print("Now attempting to insert values into officials table...", end="")

# FORMAT DATES, INSERTS NULLS AND THEN INSERT ALL VALUES INTO TABLE
for line in officials_dbase_table_lines_read:

    # HANDLE SINGLE-QUOTES/APOSTROPHES IN TEXT VALUES BY REPLACING WITH DOUBLE SINGLE-QUOTES
    line = line.replace("'","''")

    # SPLIT EACH OFFICIALS LINE INTO A LIST TO AID DATA EXTRACTION
    line=line.rstrip("\n").split(";")

    # INSERT NULL VALUES INTO ANY EMPTY FIELDS
    for index in range (0,len(line)):
        if line[index] =="": line[index] = None

    #print("\n",line)

    # EXTRACT DATA VALUES FROM THE CURRENT LINE
    pk_officials_index=line[0]; officials_name=line[1]
    officials_club=line[2];
    officials_dob = None #line[3]

    # REFORMAT DATE VALUE INTO YY/MM/DD SO THAT IT FITS INTO MSSQL DATE TYPE FIELDS
    if officials_dob == None: pass
    else:
        officials_dob = check_date(officials_dob)
        officials_dob = datetime.strftime(officials_dob,'%Y/%m/%d')

    #print("\nValues to be inserted: %s,%s,%s,%s" %(pk_officials_index,officials_name,officials_club,officials_dob))

    # INSERT VALUES INTO TABLE
    try:
        db_cursor.execute(""" INSERT into officials_dbase_table (pk_officials_index, officials_name,\
        officials_club, officials_dob)\
        values (?,?,?,?)""", (pk_officials_index,officials_name,officials_club,officials_dob))
    # HANDLE INSERTION FAILURE
    except pyodbc.ProgrammingError:
        print("\nERROR: INSERT failed")
        sys.exit()
print("Done")


###############################################################################################################
###############################################################################################################
# CREATE SQL SERVER DATABASE TABLE "BOUTSCORES_DBASE_TABLE"
###############################################################################################################
###############################################################################################################

if db_cursor.tables(table='boutscores_dbase_table', tableType='TABLE').fetchone():
    print("\nBoutscores table exists already, reading dbase files...")
else:
    print("\nBoutscores table doesn't exist yet, creating now...", end="")
    sql_command = """ CREATE TABLE boutscores_dbase_table ( 
    pk_boutscores_index VARCHAR(255) PRIMARY KEY, J1r1 INTEGER, J1b1 INTEGER, J2r1 INTEGER, J2b1 INTEGER, J3r1\
    INTEGER, J3b1 INTEGER, J4r1 INTEGER, J4b1 INTEGER, J5r1 INTEGER, J5b1 INTEGER, kdr1 INTEGER, kdb1 INTEGER, wr1\
    INTEGER, wb1 INTEGER, ix1r1 INTEGER, ix1b1 INTEGER, ix2r1 INTEGER, ix2b1 INTEGER, ix3r1 INTEGER, ix3b1\
    INTEGER, ix4r1 INTEGER, ix4b1 INTEGER, ix5r1 INTEGER, ix5b1 INTEGER, J1r2 INTEGER, J1b2 INTEGER, J2r2 INTEGER,\
    J2b2 INTEGER, J3r2 INTEGER, J3b2 INTEGER, J4r2 INTEGER, J4b2 INTEGER, J5r2 INTEGER, J5b2 INTEGER, kdr2\
    INTEGER, kdb2 INTEGER, wr2 INTEGER, wb2 INTEGER, ix1r2 INTEGER, ix1b2 INTEGER, ix2r2 INTEGER, ix2b2 INTEGER,\
    ix3r2 INTEGER, ix3b2 INTEGER, ix4r2 INTEGER, ix4b2 INTEGER, ix5r2 INTEGER, ix5b2 INTEGER, J1r3 INTEGER, J1b3\
    INTEGER, J2r3 INTEGER, J2b3 INTEGER, J3r3 INTEGER, J3b3 INTEGER, J4r3 INTEGER, J4b3 INTEGER, J5r3 INTEGER,\
    J5b3 INTEGER, kdr3 INTEGER, kdb3 INTEGER, wr3 INTEGER, wb3 INTEGER, ix1r3 INTEGER, ix1b3 INTEGER, ix2r3\
    INTEGER, ix2b3 INTEGER, ix3r3 INTEGER, ix3b3 INTEGER, ix4r3 INTEGER, ix4b3 INTEGER, ix5r3 INTEGER, ix5b3\
    INTEGER, J1r4 INTEGER, J1b4 INTEGER, J2r4 INTEGER, J2b4 INTEGER, J3r4 INTEGER, J3b4 INTEGER, J4r4 INTEGER,\
    J4b4 INTEGER, J5r4 INTEGER, J5b4 INTEGER, kdr4 INTEGER, kdb4 INTEGER, wr4 INTEGER, wb4 INTEGER, ix1r4 INTEGER,\
    ix1b4 INTEGER, ix2r4 INTEGER, ix2b4 INTEGER, ix3r4 INTEGER, ix3b4 INTEGER, ix4r4 INTEGER, ix4b4 INTEGER, ix5r4\
    INTEGER, ix5b4 INTEGER) """

    try:
        db_cursor.execute(sql_command)
        print("Done")
        print("Now reading dbase files...")
    except pyodbc.ProgrammingError:
        print("\nERROR: CREATE TABLE failed")
        sys.exit()

# READ BOUTSCORES_DBASE_TABLE FILE
with open(datapath+"/boutscores_dbase_table.csv","r") as boutscores_dbase_table:
    boutscores_dbase_table_lines_read = boutscores_dbase_table.readlines()

    # EXCLUDE COLUMN HEADINGS LINE [0] AND DUMMY LINE [1], START READING AT LINE [2]
    boutscores_dbase_table_lines_read = boutscores_dbase_table_lines_read[2:]
    print("Number of db lines read: ",len(boutscores_dbase_table_lines_read))
    print("Now attempting to insert values into boutscores table...", end="")

# FORMAT DATES, INSERTS NULLS AND THEN INSERT ALL VALUES INTO TABLE
for line in boutscores_dbase_table_lines_read:

    # SPLIT EACH BOUTSCORES LINE INTO A LIST TO AID DATA EXTRACTION
    line=line.rstrip("\n").split(";")

    # INSERT NULL VALUES INTO ANY EMPTY FIELDS
    for index in range (0,len(line)):
        if line[index] =="": line[index] = None

    #print("\n",line)

    # EXTRACT DATA VALUES FROM THE CURRENT LINE
    pk_boutscores_index = line[0];
    #print(pk_boutscores_index)
    J1r1 = line[1]; J1b1 = line[2]; J2r1 = line[3]; J2b1 = line[4];
    J3r1 = line[5]; J3b1 = line[6]; J4r1 = line[7]; J4b1 = line[8];
    J5r1 = line[9]; J5b1 = line[10]; kdr1 = line[11]; kdb1 = line[12];
    wr1 = line[13]; wb1 = line[14]; ix1r1 = line[15]; ix1b1 = line[16];
    ix2r1 = line[17]; ix2b1 = line[18]; ix3r1 = line[19]; ix3b1 = line[20];
    ix4r1 = line[21]; ix4b1 = line[22]; ix5r1 = line[23]; ix5b1 = line[24];

    J1r2 = line[25]; J1b2 = line[26]; J2r2 = line[27]; J2b2 = line[28];
    J3r2 = line[29]; J3b2 = line[30]; J4r2 = line[31]; J4b2 = line[32];
    J5r2 = line[33]; J5b2 = line[34]; kdr2 = line[35]; kdb2 = line[36];
    wr2 = line[37]; wb2 = line[38]; ix1r2 = line[39]; ix1b2 = line[40];
    ix2r2 = line[41]; ix2b2 = line[42]; ix3r2 = line[43]; ix3b2 = line[44];
    ix4r2 = line[45]; ix4b2 = line[46]; ix5r2 = line[47]; ix5b2 = line[48];

    J1r3 = line[49]; J1b3 = line[50]; J2r3 = line[51]; J2b3 = line[52];
    J3r3 = line[53]; J3b3 = line[54]; J4r3 = line[55]; J4b3 = line[56];
    J5r3 = line[57]; J5b3 = line[58]; kdr3 = line[59]; kdb3 = line[60];
    wr3 = line[61]; wb3 = line[62]; ix1r3 = line[63]; ix1b3 = line[64];
    ix2r3 = line[65]; ix2b3 = line[66]; ix3r3 = line[67]; ix3b3 = line[68];
    ix4r3 = line[69]; ix4b3 = line[70]; ix5r3 = line[71]; ix5b3 = line[72];

    J1r4 = line[73]; J1b4 = line[74]; J2r4 = line[75]; J2b4 = line[76];
    J3r4 = line[77]; J3b4 = line[78]; J4r4 = line[79]; J4b4 = line[80];
    J5r4 = line[81]; J5b4 = line[82]; kdr4 = line[83]; kdb4 = line[84];
    wr4 = line[85]; wb4 = line[86]; ix1r4 = line[87]; ix1b4 = line[88];
    ix2r4 = line[89]; ix2b4 = line[90]; ix3r4 = line[91]; ix3b4 = line[92];
    ix4r4 = line[93]; ix4b4 = line[94]; ix5r4 = line[95]; ix5b4 = line[96];

    # INSERT VALUES INTO TABLE
    try:

        db_cursor.execute(""" INSERT into boutscores_dbase_table (pk_boutscores_index,\
        J1r1, J1b1, J2r1, J2b1, J3r1, J3b1, J4r1, J4b1, J5r1, J5b1, kdr1, kdb1, wr1, wb1, ix1r1, ix1b1, ix2r1,\
        ix2b1, ix3r1, ix3b1, ix4r1, ix4b1, ix5r1, ix5b1, J1r2, J1b2, J2r2, J2b2, J3r2, J3b2, J4r2, J4b2, J5r2,\
        J5b2, kdr2, kdb2, wr2, wb2, ix1r2, ix1b2, ix2r2, ix2b2, ix3r2, ix3b2, ix4r2, ix4b2, ix5r2, ix5b2, J1r3,\
        J1b3, J2r3, J2b3, J3r3, J3b3, J4r3, J4b3, J5r3, J5b3, kdr3, kdb3, wr3, wb3, ix1r3, ix1b3, ix2r3, ix2b3,\
        ix3r3, ix3b3, ix4r3, ix4b3, ix5r3, ix5b3, J1r4, J1b4, J2r4, J2b4, J3r4, J3b4, J4r4, J4b4, J5r4, J5b4,\
        kdr4, kdb4, wr4, wb4, ix1r4, ix1b4, ix2r4, ix2b4, ix3r4, ix3b4, ix4r4, ix4b4, ix5r4, ix5b4)
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",\
                (pk_boutscores_index,\
                J1r1, J1b1, J2r1, J2b1, J3r1, J3b1, J4r1, J4b1, J5r1, J5b1, kdr1, kdb1, wr1, wb1, ix1r1, ix1b1,\
                ix2r1, ix2b1, ix3r1, ix3b1, ix4r1, ix4b1, ix5r1, ix5b1, J1r2, J1b2, J2r2, J2b2, J3r2, J3b2,\
                J4r2, J4b2, J5r2, J5b2, kdr2, kdb2, wr2, wb2, ix1r2, ix1b2, ix2r2, ix2b2, ix3r2, ix3b2, ix4r2,\
                ix4b2, ix5r2, ix5b2, J1r3, J1b3, J2r3, J2b3, J3r3, J3b3, J4r3, J4b3, J5r3, J5b3, kdr3, kdb3, wr3,\
                wb3, ix1r3, ix1b3, ix2r3, ix2b3, ix3r3, ix3b3, ix4r3, ix4b3, ix5r3, ix5b3, J1r4, J1b4, J2r4, J2b4,\
                J3r4, J3b4, J4r4, J4b4, J5r4, J5b4, kdr4, kdb4, wr4, wb4, ix1r4, ix1b4, ix2r4, ix2b4, ix3r4,\
                ix3b4, ix4r4, ix4b4, ix5r4, ix5b4)
                          )

    # HANDLE INSERTION FAILURE
    except pyodbc.ProgrammingError:
        print("\nERROR: INSERT failed")

        sys.exit()
print("Done")


###############################################################################################################
# CLOSE DATABASE CONNECTION
###############################################################################################################
db_connection.autocommit = False
db_cursor.close()
del db_cursor
db_connection.close()
