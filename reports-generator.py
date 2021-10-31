#This is just to provide a sample of what this system does and looks like.

#Here is just the list of imports
# Get useful libraries
from glob import glob
from re import search
from re import sub
from re import match
import pandas as pd
from webbrowser import open
import numpy as np
from math import floor
from math import ceil
import openpyxl
from openpyxl import load_workbook
from requests import get
from re import sub
from re import search
from pandas import DataFrame
from pandas import read_table
from pandas import set_option
import os
import csv
from shutil import copyfile





#This is the code I use to pull information into my program from my downloads
# Have the computer find the downloaded csv files in your downloads folder.
list_of_files_in_downloads = glob("".join([downloads_folder,"*"]))

"""Find the location for each of the files in downloads based on how they are named (for attendance reports 
also use whether you have already found the first or not)"""
attendance_file_location_1 = ""
for x in filter(lambda x: search(r"\.csv$",x), list_of_files_in_downloads):
    if search(r"grade_export_csv",x):
        grade_file_location = x
    elif search(r"attendance_reports_attendance",x):
        if attendance_file_location_1 == "":
            attendance_file_location_1 = x
        else:
            attendance_file_location_2 = x
    elif search(r"Grades-OR",x):
        student_orientation_course_input_location = x
    elif search(r"\\[0-9]+.csv$",x):
        zoho_file_location = x
    elif search(r"Download Me for Student Services - Conglomeration",x):
        google_download_file_location = x


        

        
        
        
#This is some code for finding grade ranges
#Find all students last block of grades in each range
dictionary_of_last_block_initial = {
        "Last time student got a score between -10 and 0": None,
        "Last time student got a score between 0 and 10": None,
        "Last time student got a score between 10 and 20": None,
        "Last time student got a score between 20 and 30": None,
        "Last time student got a score between 30 and 40": None,
        "Last time student got a score between 40 and 50": None,
        "Last time student got a score between 50 and 60": None,
        "Last time student got a score between 60 and 70": None,
        "Last time student got a score between 70 and 80": None,
        "Last time student got a score between 80 and 90": None,
        "Last time student got a score between 90 and 100": None}

last_block_of_a_grade_range = pd.DataFrame(pd.Series(dictionary_of_last_block_initial))
last_block_of_a_grade_range = last_block_of_a_grade_range.T

list_of_all_students = pd.DataFrame(zoho_information["student sis"].astype("int"))["student sis"].tolist()

for x in list_of_all_students:
    dictionary_of_last_block = dictionary_of_last_block_initial
    x = str(x)
    data_for_one_student = grade_count_summaries.loc[grade_count_summaries["student sis"] == x].groupby(["student sis","Block","buckets of 10"]).sum()
    data_for_one_student = data_for_one_student.reset_index()
    blocks = list(pd.unique(data_for_one_student["Block"]))
    blocks.reverse()
    for block in blocks:
        buckets = list(pd.unique(data_for_one_student.loc[data_for_one_student["Block"] == block]["buckets of 10"]))
        for bucket in buckets:
            if dictionary_of_last_block[f"Last time student got a score between {round(bucket - 10)} and {round(bucket)}"] == None:
                dictionary_of_last_block[f"Last time student got a score between {round(bucket - 10)} and {round(bucket)}"] = current_block_date - block - 1
        
    dataframe_of_last_time_values = pd.DataFrame(pd.Series(dictionary_of_last_block))
    dataframe_of_last_time_values.columns = [x]
    last_block_of_a_grade_range = last_block_of_a_grade_range.append(dataframe_of_last_time_values.T)
    
   
  
  
  
  
 #This is some code for creating a report.
  semester_summary_report = semester_summary[["Semester GPA","Semester Attendance","Total Hours Missed"]].join(last_block_summary_statistics.set_index("student sis")[["GPA","Attendance Average","Hours Missed"]]).join(number_of_Fs).fillna(value="999")
semester_summary_report.columns = ["Current/Very, Very Recent Semester GPA","Current/Very, Very Recent Semester Attendance","Total Hours Missed in Current/V.V. Recent Semester","Last Completed Block GPA","Last Completed Block Attendance","Total Hours Missed Last Block","Number of F's in Last Completed Block"]
for x in ["Current/Very, Very Recent Semester GPA","Current/Very, Very Recent Semester Attendance","Total Hours Missed in Current/V.V. Recent Semester","Last Completed Block GPA","Last Completed Block Attendance","Total Hours Missed Last Block","Number of F's in Last Completed Block"]:
    semester_summary_report[x] = round(semester_summary_report[x].astype("float"),2)
semester_summary_report.to_csv("".join([program_folder,f"Records\\Semester Data\\{term_for_records}_Semester_Summary_Data.csv"]),
    sep="\t")

        
