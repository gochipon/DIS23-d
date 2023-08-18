import openai
from flask import Flask, render_template, request
import datetime
import json


dt = datetime.datetime.today()  # ローカルな現在の日付と時刻を取得
d=dt.date()

openai.api_key = "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" 

app = Flask(__name__)

def Ask_ChatGPT(message):
    
    # 応答設定
    completion = openai.ChatCompletion.create(
                 model    = "gpt-3.5-turbo",    
                 messages = [{
                     "role":"system",
                     "content":'あなたは、タスク管理やスケジュール管理が得意な人です。すべて日本語で具体的なタスクを答えてください。json形式のみで出力してください'},
                    {
                     "role":"user",      
                     "content":message,   
                            }],
            
                 n           = 1,                
                 stop        = None,            
                 temperature = 0.5,              
    )
    
    # 応答
    response = completion.choices[0].message["content"]
    
    # 応答内容出力
    return response

# getのときの処理
@app.route('/', methods=['GET'])
def get():
	return render_template('index.html')

# postのときの処理	
@app.route('/', methods=['POST'])
def post():
	name = request.form['name']
	limit = request.form['limit']
	first_time = request.form['first_time']
	last_time = request.form['last_time']
	max_time = request.form['max_time']
	req = request.form['req']
	
	# GPT-3に1週間のスケジュールを生成させる
	prompt = (
    f"私は{name}を{limit}までに達成したい。取り組み可能開始時間{first_time}、"
    f"取り組み可能修了時間{last_time}、1日の最大取り組み時間{max_time}、で{d}からの1週間のスケジュールをjson形式での順で提案してください。\n"
    "出力例\n"
    "'2023-08-22': [\n    {"
    "'start_time': '09:00',\n"
    "'end_time': '11:00',\n"
    "'task': 'リーディングの問題集を解く'},\n"
    f"ただし、{req}、そして、以下の時間は避けてスケジュールを組んでください。"
        )

	
	message = Ask_ChatGPT(prompt)
	message = json.loads(message)
	# print(message)
	return render_template('schedule.html', schedule = message)

if __name__ == '__main__':
	app.run()
