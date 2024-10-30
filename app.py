# app.py
from flask import Flask, request, render_template, flash
import os
from werkzeug.utils import secure_filename
import subprocess
import tempfile

app = Flask(__name__)
# print = app.logger.info
app.secret_key = 'secret-key'  # Required for flash messages
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def print_file(filepath):
    app.logger.info(f"Printing file: {filepath}")
    try:
        # Get default printer
        # get_printer_cmd = ['lpstat', '-d']
        # # lpinfo -v
        # # get_printer_cmd = ['lpinfo', '-v']
        # printer_info = subprocess.check_output(get_printer_cmd, universal_newlines=True)
        # # take the line that starts with direct
        # printer_info = printer_info.split('\n')
        # for line in printer_info:
        #     if line.startswith('direct'):
        #         default_printer = line.split(' ')[1]
        #         break
        # # default_printer = printer_info.split(': ')[-1].strip()
        # app.logger.info(f"Default printer: {default_printer}")

        # Print the file using lp command
        print_cmd = ['lp', filepath]
        subprocess.run(print_cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        app.logger.info(f"Printing error: {str(e)}")
        return False
    except Exception as e:
        app.logger.info(f"Unexpected error: {str(e)}")
        return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return render_template('upload.html')
            
        file = request.files['file']
        
        # If no file was selected
        if file.filename == '':
            flash('No file selected')
            return render_template('upload.html')
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Try to print the file
            if print_file(filepath):
                flash('File has been sent to printer')
            else:
                flash('Error occurred while printing')
                
            # Clean up the file after printing
            os.remove(filepath)
            
        else:
            flash('Invalid file type')
            
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
