import requests
import socket
from flask import Flask, render_template, jsonify, request
from flask_classful import FlaskView, route
from persona_server.softmax_model import Simulation_run

"""To run the script use the command 'flask run --cert=adhoc --host=0.0.0.0 --port=5000' to enable HTTPS locally"""
app = Flask(__name__,
            static_url_path='',
            static_folder='persona_vision_engine/static',
            template_folder='persona_vision_engine/static')

persona_vision_addr = "http://localhost:5000/"
#persona_gui_addr = "192.168.43.130"
persona_gui_addr = "127.0.0.1"
persona_gui_port = 3002



class MyServer(FlaskView):

    def __init__(self):
        self.received = None
        #self.sim = Simulation_run()
        #self.sim.initialize(n_actions)
        #self.sim.run_simulation_threaded()


    def index(self):  # put application's code here
        return render_template('persona.html')

    @route('/data', methods=['POST'])
    def receive(self):
        # POST request
        if request.method == 'POST':
            #print('Incoming from Vision Engine..')
            self.received = request.get_json()  # parse as JSON
            packet = self.received['packet']
            facing = packet['facing']
            rightEyeX = round(packet['right_eye']['x'], 0)
            rightEyeY = round(packet['right_eye']['y'], 0)
            leftEyeX = round(packet['left_eye']['x'], 0)
            leftEyeY = round(packet['left_eye']['y'], 0)
            print("A person is facing :" , facing)
            if facing is True:
                self.send_learned_parameter_UDP("1" + "," + str(rightEyeX) + "," + str(rightEyeY) + "," + str(leftEyeX) + "," + str(leftEyeY))
            else:
                self.send_learned_parameter_UDP("0" + "," + str(rightEyeX) + "," + str(rightEyeY) + "," + str(leftEyeX) + "," + str(leftEyeY))
            return 'OK', 200

    @route('/learned', methods=['POST'])
    def fetch_learned_parameter(self):
        # POST request
        if request.method == 'POST':
            return {'learned': 1}

    def send_learned_parameter(self, learned):
        # make a POST request
        dictToSend = {'learned': learned}
        res = requests.post(persona_vision_addr + "/learned", json=dictToSend)
        print('response from server:', res.text)
        dictFromServer = res.json()

    def send_learned_parameter_UDP(self, parameter):
        print("Sending", parameter)
        bytesToSend = str.encode(parameter)
        serverAddressPort = (persona_gui_addr, persona_gui_port)
        bufferSize = 1024
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

MyServer.register(app, route_base='/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
