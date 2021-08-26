from flask import Flask, render_template, jsonify, request

app = Flask(__name__,
            static_url_path='',
            static_folder='persona_vision_engine/static',
            template_folder='persona_vision_engine/static')


@app.route('/')
def hello_world():  # put application's code here
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
