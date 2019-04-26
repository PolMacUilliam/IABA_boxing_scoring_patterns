# open file lorem.txt for reading text data
with open("data/c73b013.cp", "rt") as file_input:
    for line in file_input:
        print(line, end="")
file_input.close()                   # close the file

print file_input

'''
# open file
lines = [] # define empty list to hold file contents as strings
with open("data/c73b012.cp", "rt") as cp_file_input:
    for line in cp_file_input:
       lines.append(line)  #add that line to our list of lines.
cp_file_input.close()                   # close the file
#print("lines:\n",lines); print("\n\n\n")

competition = lines[32]; print(competition)
red_team = lines[38]; print(red_team)
blue_team = lines[39]; print(blue_team)
session = lines[42]; print(session)
judges = lines[50]; print(judges)

rd1_det_scores = lines[56]; print(rd1_det_scores)
rd2_det_scores = lines[57]; print(rd2_det_scores)
rd3_det_scores = lines[57]; print(rd3_det_scores)

result = lines[70:72]; print(result)


















'''
cp_file_in = open("data/c73b012.cp")
lines = cp_file_in.read()
print(lines)
answer = lines.find('[CombPoints]')
print("answer: ",answer)
cp_file_in.close()

'''
'''
import csv as csv

myResultString = "WP"
yes = 0
inFpath = csv.askopenfilename(defaultextension =".cp", filetypes = [("csv files",".csv"), ("all files", ".*")])
with open(inFpath, 'r') as inF:
    for index, line in enumerate(inF):
        if 'myString' in line:
            yes = yes =+ 1
            print("yes")
            with open("C:/Users/Cenit/PycharmProjects/Major_Project/data/thenewfile", 'w') as f:
                f.write("Line #%d has string: %s"  (index, line))
print(yes)



import re


# open file text.cp for reading text data
with open("data/text.cp", "rt") as in_file:
    contents = in_file.read()  # read the entire file into a string variable
in_file.close()                   # close the file
print("\n",contents,"\n")  		          # print contents
'''
'''
