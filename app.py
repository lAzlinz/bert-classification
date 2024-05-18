from flask import Flask, render_template, request
import re
from question_answering import get_answer, classifier

def add_links(response):
	link_pattern: str = r'(https?://[A-Za-z0-9/_\.\-]+)'
	replacement: str = r'<a href="\1">\1</a>'
	return re.sub(link_pattern, replacement, response)

bot_name = "chatBUt-NLP"

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
	return render_template('home.html', name="Azriel")

@app.route('/chatBUt')
def app_function():
	return render_template('app.html')

@app.route('/get')
def get_bot_response():
	user_text = request.args.get('msg')
	answer: str = get_answer(user_text)
	answer = add_links(answer)
	return answer

@app.route('/test')
def get_user_message():
	return request.args.get('msg')

hosts: dict[str] = {
	'BUWifiPortal': '172.16.7.38',
	'3rdFloor': '10.0.1.62', # 10.0.1.205
	'localhost': 'localhost'
}

if __name__ == '__main__':
	app.run(
		host=hosts['3rdFloor'],
		debug=True
	)