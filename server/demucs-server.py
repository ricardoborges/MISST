import flask
import os
import shutil
import subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create the application.
APP = flask.Flask(__name__)

# Create a URL route in our application for "/"
@APP.route('/')
def home():
    return "demucs-server V0.1"

@APP.route('/demucs-upload', methods=['POST'])
def upload():
    f = flask.request.files['file']
    f_extension = flask.request.files['file'].filename.split('.')[-1]
    if os.path.exists('./tmp'):
        pass
    else:
        os.mkdir('./tmp')
    f.save(f'./tmp/{f.filename}.{f_extension}')
    file_path = os.path.abspath(f'./tmp/{f.filename}.{f_extension}')
    cmd = subprocess.run(f'python -m demucs -d cuda "{file_path}"', check=True)
    print(f'done: {cmd.returncode}')
    print("File Processed")
    for i in os.listdir('./tmp'):
        os.remove(f'./tmp/{i}')
    os.rmdir('./tmp')
    print("Temp Folder Removed")
    shutil.make_archive(f'./separated/mdx_extra_q/{f.filename}', 'zip', f'./separated/mdx_extra_q/{f.filename}')
    print("Archive Created")
    for i in os.listdir(f'./separated/mdx_extra_q/{f.filename}'):
        os.remove(f'./separated/mdx_extra_q/{f.filename}/{i}')
    os.rmdir(f'./separated/mdx_extra_q/{f.filename}')
    print("Temp Folder Removed")
    print("Done")
    return "OK"

@APP.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    dir = os.path.abspath('./separated/mdx_extra_q/')
    return flask.send_from_directory(directory=dir, path=filename)

if __name__ == '__main__':
    port = 5000
    host = "127.0.0.1"
    APP.run(host=host, port=port)
    #APP.run(debug=True)