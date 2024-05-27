#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@ file        : GPTQuery_improved.py
@ description : 
@ time        : 2024/03/29 10:02:45
@ author      : Wenshuo Zhai
@ version     : 1.0
'''

from gptdemo import OpenAI
import pandas as pd
import json
import re
import sqlite3
import copy

def process(raw_sql):
    utterance_sql_gpt = raw_sql
    utterance_sql_gpt = utterance_sql_gpt.replace("\n", " ")
    utterance_sql_gpt = utterance_sql_gpt.replace("sql", " ")
    utterance_sql_gpt = utterance_sql_gpt.replace("##", " ")
    utterance_sql_gpt = utterance_sql_gpt.replace("```", " ")
    utterance_sql_gpt = re.sub(r'\s+', ' ', utterance_sql_gpt)
    return utterance_sql_gpt

# model
model_name = "gpt-3.5-turbo-0125"

# API KEY
client = OpenAI(api_key = '')

# open train json
f = open('C:/programming/cosql_dataset/sql_state_tracking/cosql_dev.json', 'r')
# read json 
data = json.load(f)
table_list = open('C:/programming/cosql_dataset/tables.json', 'r')
table_list = json.load(table_list)

for i in range(len(data)):
    # i = random[i]
    task = data[i]
    database_id = task['database_id']
    database_schema_path = 'C:/programming/cosql_dataset/database/' + database_id + '/' + 'schema.txt'
    file_database_schema = open(database_schema_path, 'r')
    database_schema = file_database_schema.read()
    file_database_schema.close()
    database_path = 'C:/programming/cosql_dataset/database/' + database_id + '/' + database_id + '.sqlite'
    conn = sqlite3.connect(database_path)
    filtered_elements = [element for element in table_list if element.get("db_id") == database_id]
    table_names_original = filtered_elements[0]['table_names_original']
    # # 
    database_data = '## We selected the first three rows of data from each table as reference, as follows: \n'
    for k in range(len(table_names_original)):
        table_name = table_names_original[k] 
        table = pd.read_sql_query("SELECT * FROM " + table_name + " limit 3", conn)
        table_json = table.to_json()
        database_data += "# TABLE " + '"' + table_name + '"' + ": " + str(table_json) + '\n'

    head_semantic = "### Given the following database schema, your job is to infer the semantics of table and column to ensure correct table joins based on relationships defined in the database schema.\n" + database_schema + database_data 
    conversation_semantic = [{"role": "user","content": head_semantic}]
    completion = client.chat.completions.create(
                            model = model_name,
                            messages = conversation_semantic,
                            temperature=0.0, seed=319)
    semantic = process(completion.choices[0].message.content)

    head = "### Given the following database schema, your job is to write queries given a user’s request and with no explanation. \n" + database_schema + database_data + "\n## " + semantic + "\n### You must follow these rules: \n1. Clearly define the query conditions and constraints to match the expected results accurately. Ensure a clear understanding of the relationships between tables before formulating queries.\n2. Familiarize yourself with the database schema, including table relationships and foreign keys. Ensure JOIN conditions accurately reflect the connections between tables to avoid data discrepancies.\n3.Select only the necessary columns in the SELECT statement to retrieve relevant data. Apply aggregate functions appropriately, ensuring they align with the desired aggregation logic.\n4. Verify that JOIN conditions are based on correct columns to establish accurate relationships. Include all non-aggregated columns in the GROUP BY clause for proper grouping. Apply filtering conditions accurately in the WHERE clause to refine data before aggregation. Use ORDER BY clauses effectively, specifying ASC or DESC for correct result ordering.\n5. Maintain consistent aliases for tables and columns throughout the query for clarity and accuracy. Validate data existence before querying to prevent referencing non-existent values.\n"
    interaction = task['interaction']
    conversation = [{"role": "system","content": head}]
    cur = conn.cursor() 
    for j in range(len(interaction)):
        utterance = interaction[j]
        utterance_text = "## " + utterance['utterance']
        conversation.append({"role": "user", "content": utterance_text})
        completion = client.chat.completions.create(
                            model = model_name,
                            messages = conversation,
                            temperature=0.0, seed=319)
        answer =  "## " + completion.choices[0].message.content
        conversation.append({"role":"assistant","content":answer})
        interaction[j]['query_GPT3.5-turbo_improved3.0+'] = answer

    if(i % 5 == 0):
        new_file_path = 'C:/programming/cosql_dataset/sql_state_tracking/sparc_dev_gpt3.5-0408' + str(i) + '.json' 
        with open(new_file_path, 'w', errors = 'ignore') as f:
            json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)

new_file_path = 'C:/programming/cosql_dataset/sql_state_tracking/cosql_12345guidance.json' 
with open(new_file_path, 'w') as f:
    json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
