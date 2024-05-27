from gptdemo import OpenAI
import json
import tiktoken


model_name = "gpt-3.5-turbo-0125"
# API KEY
client = OpenAI(api_key = 'sk-')
# Returns the number of tokens in a text string.
def num_tokens_from_string(string: str, encoding_name: str) -> int:

    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

f = open('C:/programming/cosql_dataset/sql_state_tracking/sparc_dev_gpt3.5-3+3wog_God_guidance_all.json' , 'r')
data = json.load(f)
conclusion_head = '##### Next, some guiding suggestions will be given. Your task is to integrate these scattered recommendations into a comprehensive and concise overarching guiding principle. Please try to categorize these suggestions by similarity or logical order to better organize the information. Remember, the goal is to create a general guidance recommendation that is easy to understand and apply, which will serve as the basis for decisions and actions.\n'
gather = []
conclusion_piece = ''
for i in range(len(data)):
    set = data[i]
    sub_conclusion = set['conclusion']
    sub_conclusion = sub_conclusion.replace("###", "")
    sub_conclusion = sub_conclusion.replace("### ", "")
    sub_conclusion = sub_conclusion.replace("##", "")
    sub_conclusion = sub_conclusion.replace("## ", "")
    sub_conclusion = sub_conclusion.replace("#", "")
    sub_conclusion = sub_conclusion.replace("\n\n", "\n")
    sub_conclusion = sub_conclusion.replace("\n \n", "\n")    
    sub_conclusion = sub_conclusion.replace("# ", "")
    conclusion_piece += "### Section %d: \n" % (i+1) + sub_conclusion + '\n'
    tokens_num = num_tokens_from_string(conclusion_piece, "cl100k_base")
completion = client.chat.completions.create(
                            model = model_name,
                            messages = [{"role": "system","content": conclusion_head},
                                        {"role": "user", "content": conclusion_piece},
                                        ],
                            temperature=0.0)
output = completion.choices[0].message.content
new_file_path = 'C:/programming/cosql_dataset/sql_state_tracking/Sparc_Sub_Conclusion0407_all' + '.json' 
with open(new_file_path, 'w', errors = 'ignore') as f:
            json.dump(gather, f, indent=4, ensure_ascii=False, sort_keys=True)