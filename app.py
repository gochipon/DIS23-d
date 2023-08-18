import openai
from flask import Flask, render_template, request

openai.api_key = "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" 

app = Flask(__name__)

def Ask_ChatGPT(message):
    
    # 応答設定
    completion = openai.ChatCompletion.create(
                 model    = "gpt-3.5-turbo",    
                 messages = [{
                     "role":"system",
                     "content":'あなたは優秀なアシスタントです。'},
                    {
                     "role":"user",      
                     "content":message,   
                            }],
    
                 max_tokens  = 1024,            
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
	prompt = f"私は{name}を{limit}までに達成したい。今日からの1週間のスケジュールをjson形式で提案してください。"
	massage = Ask_ChatGPT(prompt)
	# print(response)
	print(massage)
	return render_template('index.html')

if __name__ == '__main__':
	app.run()