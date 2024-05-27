#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@ file        : 
@ description : 
@ time        : 2024/03/06 16:08:13
@ author      : Wenshuo Zhai
@ version     : 1.0
'''


import json
import sqlite3
from collections import Counter
import re

def ExactMatch(sql, sql_gpt):
    sql = sql.replace(" ", "")
    sql = sql.replace(";", "")
    sql = sql.upper()
    sql_gpt = sql_gpt.replace(" ", "")
    sql_gpt = sql_gpt.replace(";", "")
    sql_gpt = sql_gpt.upper()
    return sql, sql_gpt

def ExecutionAccuracy(answer, answer_gpt):
    if ((answer == None) & (answer_gpt != None)) or ((answer != None) & (answer_gpt == None)):
        return 0
    elif (answer == None) & (answer_gpt == None):
        return 1
    elif (answer != None) & (answer_gpt != None):
        d = [False for c in answer if c not in answer_gpt]
        if d :
            return 0
        else:
            return 1
          
f = open('C:/programming/cosql_dataset/sql_state_tracking/cosql_1234guidance.json', 'r')

data = json.load(f)
sum_q = 0
qex = 0
sum_i = 0
qem = 0
iex = 0
iem = 0
fva = 0
for i in range(len(data)):
    sum_i += 1
    set = data[i]
    database_id = set['database_id']
    database_path = 'C:/programming/cosql_dataset/database/' + database_id + '/' + database_id + '.sqlite'
    interaction = set['interaction']
    conn = sqlite3.connect(database_path) 
    cur = conn.cursor()
    cha_x = 1
    cha_m = 1
    for j in range(len(interaction)):
        sum_q += 1
        utterance = interaction[j]
        utterance_text = utterance["utterance"]
        # gold sql query
        utterance_sql = utterance['query']
        utterance_sql = utterance_sql.replace("! =", "!=")
        utterance_sql = utterance_sql.replace("> =", ">=")
        utterance_sql = utterance_sql.replace("< =", "<=")  
        try: 
            answer = cur.execute(utterance_sql).fetchone()
        except Exception as e:
            continue
        # GPT sql query
        utterance_sql_gpt = utterance['query_GPT3.5-turbo_improved3.0+']
        utterance_sql_gpt = utterance_sql_gpt.replace("\n", " ")
        utterance_sql_gpt = utterance_sql_gpt.replace("sql", " ")
        utterance_sql_gpt = utterance_sql_gpt.replace("##", " ")
        utterance_sql_gpt = utterance_sql_gpt.replace("```", " ")
        utterance_sql_gpt = utterance_sql_gpt.replace(";","")
        utterance_sql_gpt_0 = utterance_sql_gpt
        if (('where' in utterance_sql_gpt) or ('WHERE' in utterance_sql_gpt) or ('Where' in utterance_sql_gpt)):
        # if ('=' in utterance_sql_gpt):
            utterance_sql_gpt = utterance_sql_gpt + " COLLATE NOCASE"
        utterance_sql_gpt = re.sub(r'\s+', ' ', utterance_sql_gpt)
        try:
            answer_gpt = cur.execute(utterance_sql_gpt).fetchone()
        except Exception as e_gpt: 
            fva += 1        
            continue
        # if (answer == None) & (answer_gpt == None):
        #     sum_none += 1 
        # if (answer_gpt == None):
        #     answer_gpt_none += 1        
        # 
        if ExecutionAccuracy(answer, answer_gpt):           
            qex += 1
        else:
            # print(utterance_text)
            # print(utterance_sql)
            # print(answer)
            # print(utterance_sql_gpt)
            # print(answer_gpt)
            cha_x = 0
    
        sql, sql_gpt = ExactMatch(utterance_sql, utterance_sql_gpt_0)
        if(sql == sql_gpt):
            qem += 1
        else:
            cha_m = 0

    if cha_x:
        iex += 1

    if cha_m:
        iem +=1

    cur.close()
    conn.close()

f.close()

# print("same:", same)
# print("sum:", sum)
# print("acc:", same/sum)

# print("none none: ", sum_none)
# print("answer gpt none", answer_gpt_none)

# print("error original：", error)
# print("error gpt:", error_gpt)  
print("VA: ", "%.1f"%((sum_q-fva)/sum_q*100))
print("QEM:", "%.1f"%(qem/sum_q*100))
print("IEM:", "%.1f"%(iem/sum_i*100))
print("QEX:", "%.1f"%(qex/sum_q*100))
print("IEX:", "%.1f"%(iex/sum_i*100))
print("-")