import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from predict import BotanicalDiagnosticEngine
import uuid

app = Flask(__name__)
app.secret_key = "botanical_diagnostic_system_secure_token_99x"

# System configuration variables
STORAGE_DIR = os.path.join('static', 'uploads')
VALID_FORMATS = {'png', 'jpg', 'jpeg'}
COMPLIMENTARY_SCANS = 100

app.config['STORAGE_DIR'] = STORAGE_DIR

# Verify storage directory availability
os.makedirs(STORAGE_DIR, exist_ok=True)

# Boot sequence: Load AI inference engine
try:
    print("Bootstrapping inference engine...")
    inference_engine = BotanicalDiagnosticEngine()
    engine_ready = True
except Exception as err:
    print(f"System Alert: Diagnostics module offline. Details: {err}")
    inference_engine = None
    engine_ready = False

def is_valid_format(file_name):
    """Validates if the provided file extension is supported by the system."""
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in VALID_FORMATS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_credential = request.form.get('contact')
        if user_credential and len(user_credential) >= 5:
            session['logged_in'] = True
            session['contact'] = user_credential
            flash("Authentication successful. Welcome to the portal.")
            return redirect(url_for('index'))
        else:
            flash("Authentication failed. Please provide a valid identifier.")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Session terminated securely.")
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
def index():
    """Primary dashboard view for diagnostic uploads."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    # Generate unique session identifier tracking
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['scans_completed'] = 0
        
    available_scans = COMPLIMENTARY_SCANS - session.get('scans_completed', 0)
    return render_template('index.html', model_loaded=engine_ready, trials_remaining=available_scans, max_trials=COMPLIMENTARY_SCANS)

@app.route('/predict', methods=['POST'])
def upload_predict():
    """Handles image ingestion and triggers the AI diagnostic pipeline."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if session.get('scans_completed', 0) >= COMPLIMENTARY_SCANS:
        flash("Your scan quota has been depleted. Account upgrade required.")
        return redirect(url_for('index'))
        
    if not engine_ready:
        flash("Diagnostic engine is currently offline. Administrator intervention required.")
        return redirect(url_for('index'))

    if 'file' not in request.files:
        flash('Upload payload empty. No image detected.')
        return redirect(url_for('index'))
        
    target_asset = request.files['file']
    
    if target_asset.filename == '':
        flash('Invalid selection. File name cannot be empty.')
        return redirect(url_for('index'))
        
    if target_asset and is_valid_format(target_asset.filename):
        safe_name = secure_filename(target_asset.filename)
        destination = os.path.join(app.config['STORAGE_DIR'], safe_name)
        target_asset.save(destination)
        
        # Execute diagnostic analysis
        analysis = inference_engine.predict(destination)
        
        if analysis['success']:
            session['scans_completed'] = session.get('scans_completed', 0) + 1
            available_scans = COMPLIMENTARY_SCANS - session['scans_completed']
            
            return render_template(
                'index.html', 
                filename=safe_name, 
                prediction=analysis['class'], 
                confidence=f"{analysis['confidence']*100:.2f}%",
                prevention=analysis.get('prevention', 'No specific protocol available.'),
                model_loaded=engine_ready,
                trials_remaining=available_scans,
                max_trials=COMPLIMENTARY_SCANS
            )
        else:
            flash(f"Diagnostic failure: {analysis.get('error')}")
            return redirect(url_for('index'))
            
    else:
        flash('Unsupported specification. Please use PNG or JPG formats.')
        return redirect(url_for('index'))

@app.route('/display/<filename>')
def display_image(filename):
    """Serves the uploaded diagnostic image from local storage."""
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)
