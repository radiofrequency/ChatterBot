# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from bottle import route, run, template, get, post, request

from chatterbot.trainers import ChatterBotCorpusTrainer
import json

import sys


chatbot = ChatBot(
	'Angie', 
	storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
	logic_adapters=[
		{
			'import_path': 'chatterbot.logic.BestMatch'
		},
		{
			'import_path': 'chatterbot.logic.LowConfidenceAdapter',
			'threshold': 0.90,
			'default_response': 'DOESNOTCOMPUTE'
		},
		{
			'import_path': 'chatterbot.logic.SpecificResponseAdapter',
			'input_text': 'help',
			'output_text': 'static command help'
		}])
#chatbot = 

chatbot.set_trainer(ListTrainer)


def test_chat(chat):
	print chat
	print chatbot.get_response(chat)


@route('/train', method='POST')
def index():
	print request.body
	l = json.load(request.body)
	print l
	chatbot.train(l["convo"])
	return json.dumps({"message": "ok"});


@route('/ask', method='POST')
def index():
	print request.body
	l = json.load(request.body)
	 
	m = l["message"].encode('utf-8')

	print "got question:" +m
	reload(sys)
	sys.setdefaultencoding("utf-8")

	CONVERSATION_ID = chatbot.storage.create_conversation()
	#input_statement = bot.input.process_input_statement()
	#statement, response = bot.generate_response(input_statemenet, )
	answer = chatbot.get_response(m, CONVERSATION_ID)
	print type(answer.text)

	proper = answer.text.encode('utf-8')




	
	#print answer


	return json.dumps({"message": proper}, ensure_ascii=False, encoding="utf-8")

run(host='localhost', port=8888)