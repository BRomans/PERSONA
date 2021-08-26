from flask import Flask, render_template, jsonify, request
from .softmax_model import run_simulation

"""To run the script use the command 'flask run --cert=adhoc' to enable HTTPS locally"""
app = Flask(__name__,
            static_url_path='',
            static_folder='persona_vision_engine/static',
            template_folder='persona_vision_engine/static')


@app.route('/')
def load_engine():  # put application's code here
    return render_template('persona.html')


@app.route('/data', methods=['POST'])
def receive():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200



if __name__ == '__main__':
    app.run(ssl_context='adhoc')
    SoftMax.run_simulation()
    SoftMax.get_result()
    send_result(UE)

