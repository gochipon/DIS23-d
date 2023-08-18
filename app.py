import openai
from flask import Flask, render_template, request, redirect, url_for, session
import datetime
import json
import create
import get_calendar


dt = datetime.datetime.today() + datetime.timedelta(days = 1)# ローカルな現在の日付と時刻を取得
d=dt.date()

openai.api_key = "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" 

app = Flask(__name__)
app.config['SECRET_KEY'] = '0a1b2c3d4e5f6789abcdef1234567890b'  # セッションを暗号化するためのキー

def Ask_ChatGPT(message):
    
    # 応答設定
    completion = openai.ChatCompletion.create(
                 model    = "gpt-3.5-turbo",    
                 messages = [{
                     "role":"system",
                     "content":'あなたは、タスク管理やスケジュール管理が得意な人です。'},
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
	return render_template('index.html', message = 'フォームに回答してください')


# postのときの処理	
@app.route('/', methods=['POST'])
def post():
    name = request.form['name']
    limit = request.form['limit']
    first_time = request.form['first_time']
    last_time = request.form['last_time']
    req = request.form['req']
	
    calen = get_calendar.get_calen()
    
    print(calen)
	# GPT-3に1週間のスケジュールを生成させる
    '''
    prompt = (
    f"私は{name}を{limit}までに達成したい。取り組み可能開始時間{first_time}、"
    f"取り組み可能修了時間{last_time}、{d}からの1週間のスケジュールを{calen}以外の時間で、以下の順でjson形式のみ提案してください。\n"
    "スケジュールの出力例\n"
    "'2023-08-22': [\n    {"
    "'start_time': '00:00',\n"
    "'end_time': '00:00',\n"
    "'task': '具体的なタスク内容'},\n"
    f"さらに{req}という条件も考慮してください。\n"
    f"もしタスクを具体的にするために必要な情報が足りないときは，文頭に'infomation\n'と書いた上で、私に回答例を提示しながら一つづつ質問してください。"
        )
    '''
    prompt = (
    f"私は{name}を{limit}までに達成したい。取り組み可能開始時間{first_time}。\n"
    f"取り組み可能修了時間{last_time}。{calen}の時間にはスケジュールを組まないことが一番優先事項。\n"
    f"もしタスクを具体的にするために必要な情報が足りないときは，文頭に'infomation\n'と書いた上で、私に回答例を提示しながら一つづつ質問してください。\n"
    f"情報が十分な場合は{d}からの1週間のスケジュールを{req}という条件も考慮しながら、以下の順でjson形式のみ提案してください。\n"
    "スケジュールの出力例\n"
    "'2023-08-22': [\n    {"
    "'start_time': '00:00',\n"
    "'end_time': '00:00',\n"
    "'task': '具体的なタスク内容'},\n"
        )
    session['previous_prompt'] = prompt
    message = Ask_ChatGPT(prompt)
    print(message)
    if message.split('\n')[0] == 'infomation':
        print(message.split('\n')[1:])
        return render_template('addinfo.html', message = message.split('\n')[1:])
    else:
        try:
            message = json.loads(message)
            session['message'] = message
            return render_template('schedule.html', schedule = message)
        except json.JSONDecodeError:
            return render_template('index.html', message = 'もう一度記入してください')

@app.route('/upload_google', methods=['POST'])
def upload_google():
    message = session.get('message', '')
    create.create(message)
    
    return render_template('finish.html', schedule = message)
    
@app.route('/upload', methods=['POST'])
def upload():
    change_data = request.form['add']
    #sub_prompt = (f"条件は同じで、{change_data}を考慮して")
    # `change_data`を使って`prompt`を変更するロジックをここに実装
    old_prompt = session.get('previous_prompt', '')
    new_prompt =  " 新しい情報: " + change_data + old_prompt
    # 例: new_prompt をデータベースに保存するなど
    print(new_prompt)
    message = Ask_ChatGPT(new_prompt)
    print(message)
    if message.split('\n')[0] == 'infomation':
        return render_template('addinfo.html', message = message.split('\n')[1:])
    
    else:
        try:
            message = json.loads(message)
            session['message'] = message
            return render_template('schedule.html', schedule = message)
        except json.JSONDecodeError:
            return render_template('addinfo.html', message = 'もう一度記入してください')
	    

@app.route('/update_point', methods=['POST'])
def update_point():
    change_data = request.form['change']
    #sub_prompt = (f"条件は同じで、{change_data}を考慮して")
    # `change_data`を使って`prompt`を変更するロジックをここに実装
    old_prompt = session.get('previous_prompt', '')
    new_prompt = " 新しい情報: " + change_data + old_prompt
    # 例: new_prompt をデータベースに保存するなど
    print(new_prompt)
    message = Ask_ChatGPT(new_prompt)
    if message.split('\n')[0] == 'infomation':
        return render_template('addinfo.html', message = message.split('\n')[1:])
    
    else:
        try:
            message = json.loads(message)
            session['message'] = message
            return render_template('schedule.html', schedule = message)
        except json.JSONDecodeError:
            return render_template('addinfo.html', message = 'もう一度記入してください')

    # 必要に応じて、新しいページや元のページにリダイレクトする
	
@app.route('/back', methods=['POST'])
def back():
    return redirect(url_for('get'))



if __name__ == '__main__':
	app.run()


