import requests
from flask import Flask, render_template, jsonify, request
from flask_classful import FlaskView, route

"""To run the script use the command 'flask run --cert=adhoc' to enable HTTPS locally"""
app = Flask(__name__,
            static_url_path='',
            static_folder='persona_vision_engine/static',
            template_folder='persona_vision_engine/static')

persona_gui_addr = "http://localhost:5000/"

class MyServer(FlaskView):

    def __init__(self):
        self.received = None

    def index(self):  # put application's code here
        return render_template('persona.html')

    @route('/data', methods=['POST'])
    def receive(self):
        # POST request
        if request.method == 'POST':
            print('Incoming..')
            self.received = request.get_json() # parse as JSON
            print(self.received['facing'])
            return 'OK', 200

    def send_learned_parameter(self, learned):
        # make a POST request
        dictToSend = {'learned': learned}
        res = requests.post(persona_gui_addr + "/learned", json=dictToSend)
        print('response from server:', res.text)
        dictFromServer = res.json()


MyServer.register(app, route_base='/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc')
