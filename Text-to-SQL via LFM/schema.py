#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@ file        : 0.py
@ description : gets chema.txt
@ time        : 2024/03/08 16:54:03
@ author      : Wenshuo Zhai
@ version     : 1.0
'''

import json
import os
import sqlite3
import re

def processing(s):
    while "insert" in s:
        start_index = s.find("insert")
        end_index = s.find(";", start_index + len("insert"))
        if start_index != -1 and end_index != -1:
            s = s[:start_index] + s[end_index+1:]
        else:
            break
    while "INSERT" in s:
        start_index = s.find("INSERT")
        end_index = s.find(";", start_index + len("INSERT"))
        if start_index != -1 and end_index != -1:
            s = s[:start_index] + s[end_index+1:]
        else:
            break
    s = s.replace("\n", "")
    s = re.sub(r'\s+', ' ', s)
    s = s.replace(";", ";\n")
    s = s.replace("create", "# create")
    s = s.replace("CREATE", "# CREATE") 
    return s
i = 0
folder_path = 'C:/programming/cosql_dataset/database/'
for folder_name in os.listdir(folder_path)[:]:
    sub_folder_path = os.path.join(folder_path, folder_name)
    for filename in os.listdir(sub_folder_path):
        if filename.endswith(".sql"):
            file_path = os.path.join(sub_folder_path, filename)
            with open(file_path, "r", errors = 'ignore') as input_file:
                original_sql_content = input_file.read()
                remove_sql_content = processing(original_sql_content)
                with open(sub_folder_path + '/' + filename.split('.')[0] + '.txt', 'w') as f:
                    f.write(remove_sql_content)
    print(folder_name)
