from flask import Flask, render_template, jsonify, request
from flask_classful import FlaskView, route

"""To run the script use the command 'flask run --cert=adhoc' to enable HTTPS locally"""
app = Flask(__name__,
            static_url_path='',
            static_folder='persona_vision_engine/static',
            template_folder='persona_vision_engine/static')


class MyServer(FlaskView):

    def __init__(self):
        self.request = None

    def index(self):  # put application's code here
        return render_template('persona.html')

    @route('/data', methods=['POST'])
    def receive(self):
        # POST request
        if request.method == 'POST':
            print('Incoming..')
            self.request = request.get_json()
            print(self.request)  # parse as JSON
            return 'OK', 200


MyServer.register(app, route_base='/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc')
