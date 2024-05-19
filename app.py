from flask import Flask, render_template, request, jsonify
import re
from new_question_answering import get_result

def add_links(result):
	link_pattern: str = r'(https?://[A-Za-z0-9/_\.\-]+)'
	replacement: str = r'<a href="\1">\1</a>'
	result = {
		'score': result['score'],
		'question': result['question'],
		'answer': re.sub(link_pattern, replacement, result['answer'])
	}
	
	return result

bot_name = "chatBUt-NLP"

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
	return render_template('home.html', name="Azriel")

@app.route('/chatBUt')
def app_function():
	return render_template('app.html')

@app.route('/ajax_endpoint', methods=['POST'])
def get_bot_response():
	user_text = request.form['question']
	result: str = get_result(user_text)
	result = add_links(result)
	return jsonify(result)

@app.route('/test')
def get_user_message():
	return request.args.get('msg')

hosts: dict[str] = {
	'BUWifiPortal': '172.16.7.38',
	'3rdFloor': '10.0.1.62', # 10.0.1.205
	'localhost': 'localhost',
	'all': '0.0.0.0'
}

if __name__ == '__main__':
	app.run(
		host=hosts['all'],
		debug=True
	)