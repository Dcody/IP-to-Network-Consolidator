#!/usr/bin/env python3
"""
Flask web application for IP Consolidator
Provides a simple web interface for the consolidation tool
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for, session
import os
import json
import hashlib
import time
import threading
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from core_consolidation import extract_host_ips
from analysis import run_consolidation_analysis
from output_generator import generate_asa_output, write_asa_file

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Improved secret key handling
def get_secret_key():
    """Get secret key from environment variable or generate a secure one"""
    # Try to get from environment variable first
    secret_key = os.environ.get('SECRET_KEY')
    
    if secret_key:
        return secret_key
    
    # If no environment variable, generate a secure random key
    # Note: This will change on each restart unless SECRET_KEY is set
    import secrets
    return secrets.token_hex(32)

app.secret_key = get_secret_key()

def delayed_file_cleanup(file_path, delay_seconds=300):
    """Clean up file after a configurable delay with retry mechanism"""
    def cleanup():
        # Wait for initial delay
        time.sleep(delay_seconds)
        
        # Try to clean up the file, with retries every 30 seconds
        retry_interval = 30  # seconds
        max_retries = 20  # Maximum 10 minutes of retries (20 * 30 seconds)
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
                    print(f"Cleaned up file after {delay_seconds + (retry_count * retry_interval)} seconds: {os.path.basename(file_path)}")
                    return  # Successfully cleaned up, exit the loop
                else:
                    print(f"File no longer exists: {os.path.basename(file_path)}")
                    return  # File already gone, exit the loop
            except PermissionError:
                # File might be in use (being downloaded), retry
                retry_count += 1
                if retry_count < max_retries:
                    print(f"File in use, retrying cleanup in {retry_interval} seconds: {os.path.basename(file_path)} (attempt {retry_count}/{max_retries})")
                    time.sleep(retry_interval)
                else:
                    print(f"Failed to clean up file after {max_retries} retries: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"Error cleaning up file {os.path.basename(file_path)}: {e}")
                return  # Exit on other errors
    
    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup, daemon=True)
    cleanup_thread.start()

def immediate_file_cleanup(file_path):
    """Clean up file after 30 second delay with retry mechanism every 30 seconds"""
    def cleanup():
        # Wait 30 seconds before first attempt
        initial_delay = 30  # seconds
        time.sleep(initial_delay)
        
        retry_interval = 30  # seconds
        max_retries = 10  # Maximum 5 minutes of retries (10 * 30 seconds)
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
                    print(f"Cleaned up file after {initial_delay + (retry_count * retry_interval)} seconds: {os.path.basename(file_path)}")
                    return  # Successfully cleaned up, exit the loop
                else:
                    print(f"File no longer exists: {os.path.basename(file_path)}")
                    return  # File already gone, exit the loop
            except PermissionError:
                # File might be in use (being downloaded), retry
                retry_count += 1
                if retry_count < max_retries:
                    print(f"File in use, retrying cleanup in {retry_interval} seconds: {os.path.basename(file_path)} (attempt {retry_count}/{max_retries})")
                    time.sleep(retry_interval)
                else:
                    print(f"Failed to clean up file after {initial_delay + (max_retries * retry_interval)} seconds: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"Error cleaning up file {os.path.basename(file_path)}: {e}")
                return  # Exit on other errors
    
    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup, daemon=True)
    cleanup_thread.start()

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "font-src 'self' https://cdn.jsdelivr.net; "
        "img-src 'self' data:; "
        "connect-src 'self';"
    )
    return response

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'cfg', 'conf', 'csv', 'log', 'dat', 'lst', 'ip', 'hosts'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_secure_filename(original_filename, file_content=None):
    """
    Generate a secure, hashed filename to prevent information leakage
    """
    # Get file extension from original filename
    if '.' in original_filename:
        extension = '.' + original_filename.rsplit('.', 1)[1].lower()
    else:
        extension = ''
    
    # Create a unique identifier using timestamp and random data
    timestamp = str(int(time.time() * 1000000))  # Microsecond precision
    random_salt = os.urandom(16).hex()  # 32 character random salt
    
    # If we have file content, hash it for additional uniqueness
    if file_content:
        content_hash = hashlib.sha256(file_content).hexdigest()[:16]
        base_name = f"{content_hash}_{timestamp}{random_salt}"
    else:
        base_name = f"{timestamp}{random_salt}"
    
    return base_name + extension

def cleanup_uploads():
    """Clean up all files in the uploads directory"""
    import shutil
    try:
        # Remove all files in uploads directory
        for filename in os.listdir(UPLOAD_FOLDER):
            # Additional security: validate filename before deletion
            if '..' in filename or '/' in filename or '\\' in filename:
                print(f"Skipping suspicious filename: {filename}")
                continue
                
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            # Additional security: ensure file is within upload directory
            real_file_path = os.path.realpath(file_path)
            real_upload_path = os.path.realpath(UPLOAD_FOLDER)
            
            if not real_file_path.startswith(real_upload_path):
                print(f"Skipping file outside upload directory: {filename}")
                continue
                
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print(f"Cleaned up {UPLOAD_FOLDER} directory")
    except Exception as e:
        print(f"Error cleaning uploads: {e}")

def cleanup_session_files():
    """Clean up session-specific files"""
    try:
        # Get current session file references
        analysis_file = session.get('analysis_file')
        networks_file = session.get('networks_file')
        
        # Clean up analysis file
        if analysis_file:
            analysis_filepath = os.path.join(UPLOAD_FOLDER, analysis_file)
            if os.path.exists(analysis_filepath):
                os.unlink(analysis_filepath)
                print(f"Cleaned up session analysis file: {analysis_file}")
        
        # Clean up networks file
        if networks_file:
            networks_filepath = os.path.join(UPLOAD_FOLDER, networks_file)
            if os.path.exists(networks_filepath):
                os.unlink(networks_filepath)
                print(f"Cleaned up session networks file: {networks_file}")
                
    except Exception as e:
        print(f"Error cleaning session files: {e}")

# Clean up uploads directory on startup
cleanup_uploads()

def allowed_file(filename):
    """Check if file extension is allowed"""
    if not filename or '.' not in filename:
        return False
    
    # Additional security checks
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    # Clean up any existing session files
    cleanup_session_files()
    # Clear any existing session data when starting fresh
    session.pop('analysis_file', None)
    session.pop('networks_file', None)
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and run analysis"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Check file size (limit to 100MB for performance)
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        max_size = 100 * 1024 * 1024  # 100MB
        if file_size > max_size:
            flash(f'File too large. Maximum size is 100MB. Your file is {file_size / (1024*1024):.1f}MB')
            return redirect(url_for('index'))
        
        # Read file content for hashing
        file_content = file.read()
        file.seek(0)  # Reset file pointer for processing
        
        # Generate secure filename
        secure_filename_hash = generate_secure_filename(file.filename, file_content)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename_hash)
        file.save(filepath)
        
        try:
            # Use chunked processing for large files
            chunk_size = 5000 if file_size > 10 * 1024 * 1024 else 10000  # 10MB threshold
            host_ips = extract_host_ips(filepath, chunk_size)
            
            if not host_ips:
                flash('No host IPs found in the file')
                return redirect(url_for('index'))
            
            # Run analysis
            results, frontier = run_consolidation_analysis(host_ips)

            # Compute recommended (minimum score among Pareto frontier)
            recommended = min(frontier, key=lambda r: r['score'])
            
            # Store results in session or temporary storage
            # Convert IPv4Network objects to strings for JSON serialization
            serializable_results = []
            for result in results:
                serializable_result = result.copy()
                serializable_result['networks'] = [str(network) for network in result['networks']]
                serializable_results.append(serializable_result)
            
            serializable_frontier = []
            for frontier_result in frontier:
                serializable_frontier_result = frontier_result.copy()
                serializable_frontier_result['networks'] = [str(network) for network in frontier_result['networks']]
                serializable_frontier.append(serializable_frontier_result)
            
            analysis_data = {
                'host_ips_count': len(host_ips),
                'results': serializable_results,
                'frontier': serializable_frontier,
                'filepath': filepath,
                'recommended': {
                    'threshold': recommended['threshold'],
                    'score': recommended['score'],
                    'objects_defined': recommended['objects_defined'],
                    'missing_ips_included': recommended['missing_ips_included'],
                    'expansion_percent': recommended['expansion_percent']
                }
            }
            
            # Store data in temporary files to avoid session size limits
            # Generate unique session ID for this analysis
            session_id = f"session_{int(time.time() * 1000000)}{os.urandom(8).hex()}"
            
            # Create networks data
            networks_data = {
                'host_ips_count': len(host_ips),
                'results': serializable_results,
                'frontier': serializable_frontier,
                'filepath': filepath,
                'recommended': {
                    'threshold': recommended['threshold'],
                    'score': recommended['score'],
                    'objects_defined': recommended['objects_defined'],
                    'missing_ips_included': recommended['missing_ips_included'],
                    'expansion_percent': recommended['expansion_percent']
                },
                'networks_by_threshold': {}
            }
            
            # Store networks as strings for each threshold
            for result in results:
                threshold = result['threshold']
                networks_data['networks_by_threshold'][str(threshold)] = [
                    str(network) for network in result['networks']
                ]
            
            # Store analysis data in file
            analysis_filename = f"analysis_{session_id}.json"
            analysis_filepath = os.path.join(app.config['UPLOAD_FOLDER'], analysis_filename)
            with open(analysis_filepath, 'w') as f:
                json.dump(analysis_data, f, default=str)
            
            # Store networks data in file
            networks_filename = f"networks_{session_id}.json"
            networks_filepath = os.path.join(app.config['UPLOAD_FOLDER'], networks_filename)
            with open(networks_filepath, 'w') as f:
                json.dump(networks_data, f, default=str)
            
            # Store only file references in session
            session['analysis_file'] = analysis_filename
            session['networks_file'] = networks_filename
            
            # Clean up uploaded file after processing
            try:
                os.unlink(filepath)
                print(f"Cleaned up uploaded file: {secure_filename_hash}")
            except Exception as e:
                print(f"Error cleaning up uploaded file: {e}")
            

            
            flash(f'Successfully processed {len(host_ips)} host IPs')
            return redirect(url_for('results'))
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('index'))
    
    flash('Invalid file type')
    return redirect(url_for('index'))

@app.route('/results')
def results():
    """Display analysis results"""
    # Get file references from session
    analysis_file = session.get('analysis_file')
    
    if not analysis_file:
        flash('No analysis data found. Please upload a file first.')
        return redirect(url_for('index'))
    
    # Load data from file
    analysis_filepath = os.path.join(app.config['UPLOAD_FOLDER'], analysis_file)
    if not os.path.exists(analysis_filepath):
        flash('Analysis data not found. Please upload a file first.')
        return redirect(url_for('index'))
    
    with open(analysis_filepath, 'r') as f:
        analysis_data = json.load(f)
    
    # Backfill recommended if missing (for older analysis files)
    if 'recommended' not in analysis_data or not analysis_data.get('recommended'):
        frontier = analysis_data.get('frontier', [])
        if frontier:
            best = min(frontier, key=lambda r: r.get('score', float('inf')))
            analysis_data['recommended'] = {
                'threshold': best.get('threshold'),
                'score': best.get('score'),
                'objects_defined': best.get('objects_defined'),
                'missing_ips_included': best.get('missing_ips_included'),
                'expansion_percent': best.get('expansion_percent'),
            }
    
    return render_template('results.html', data=analysis_data)

@app.route('/api/generate_output', methods=['POST'])
def generate_output():
    """Generate output for a specific threshold in specified format"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        threshold = data.get('threshold', 25)
        output_format = data.get('output_format', 'asa')
        
        # Validate threshold
        try:
            threshold = int(threshold)
            if threshold < 0 or threshold > 100:
                return jsonify({'error': 'Invalid threshold value'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid threshold value'}), 400
        
        # Validate output format
        if output_format not in ['asa', 'raw']:
            return jsonify({'error': 'Invalid output format'}), 400
        
        # Load the networks data from file
        networks_file = session.get('networks_file')
        
        if not networks_file:
            return jsonify({'error': 'No networks data found. Please upload a file first.'}), 404
        
        # Load data from file
        networks_filepath = os.path.join(app.config['UPLOAD_FOLDER'], networks_file)
        if not os.path.exists(networks_filepath):
            return jsonify({'error': 'Networks data not found. Please upload a file first.'}), 404
        
        with open(networks_filepath, 'r') as f:
            networks_data = json.load(f)
        

        
        # Find the result for the specified threshold
        result = None
        for r in networks_data['results']:
            if r['threshold'] == threshold:
                result = r
                break
        
        if not result:
            return jsonify({'error': 'Threshold not found'}), 400
        
        # Get networks for this threshold
        threshold_str = str(threshold)
        if threshold_str not in networks_data['networks_by_threshold']:
            return jsonify({'error': 'Network data not found for threshold'}), 400
        
        networks = networks_data['networks_by_threshold'][threshold_str]
        
        # Generate output based on format
        if output_format == 'asa':
            # Generate ASA output
            object_lines, group_lines = generate_asa_output(networks, threshold)
            
            # Create temporary file with unique naming
            timestamp = int(time.time() * 1000000)  # Microsecond precision
            random_suffix = os.urandom(8).hex()  # 16 character random suffix
            output_filename = f"asa_output_{threshold}percent_{timestamp}{random_suffix}.txt"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            write_asa_file(object_lines, group_lines, threshold, output_path)
        else:  # raw format
            # Generate raw IP addresses
            timestamp = int(time.time() * 1000000)  # Microsecond precision
            random_suffix = os.urandom(8).hex()  # 16 character random suffix
            output_filename = f"raw_ips_{threshold}percent_{timestamp}{random_suffix}.txt"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            with open(output_path, 'w') as f:
                f.write(f"# Raw IP Addresses for {threshold}% threshold\n")
                f.write(f"# Generated from uploaded file\n")
                f.write(f"# Objects: {result['objects_defined']}\n")
                f.write(f"# Missing IPs: {result['missing_ips_included']}\n")
                f.write(f"# Expansion: {result['expansion_percent']:.1f}%\n\n")
                
                for network in networks:
                    f.write(f"{network}\n")
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'objects_count': result['objects_defined'],
            'missing_ips': result['missing_ips_included'],
            'expansion_percent': result['expansion_percent']
        })
        
    except FileNotFoundError:
        return jsonify({'error': 'Analysis data not found. Please upload a file first.'}), 404
    except Exception as e:
        return jsonify({'error': f'Error generating output: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated ASA output file"""
    try:
        # Validate filename to prevent path traversal
        if not filename or '..' in filename or '/' in filename or '\\' in filename:
            flash('Invalid filename')
            return redirect(url_for('index'))
        
        # Only allow specific generated file patterns
        allowed_patterns = [
            'asa_output_',
            'raw_ips_'
        ]
        
        # Validate that filename matches expected pattern with unique suffix
        if not any(filename.startswith(pattern) for pattern in allowed_patterns):
            flash('Invalid file type')
            return redirect(url_for('index'))
        
        # Additional validation: ensure filename has the expected format with timestamp and random suffix
        if not (filename.endswith('.txt') and 
                ('percent_' in filename) and 
                len(filename.split('_')) >= 4):  # Should have at least 4 parts: type, threshold, percent, timestamp+suffix
            flash('Invalid filename format')
            return redirect(url_for('index'))
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Additional security check - ensure file is within upload directory
        real_file_path = os.path.realpath(file_path)
        real_upload_path = os.path.realpath(app.config['UPLOAD_FOLDER'])
        
        if not real_file_path.startswith(real_upload_path):
            flash('Access denied')
            return redirect(url_for('index'))
        
        # Send file
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
        
        # Schedule cleanup with 30-second initial delay and retry mechanism
        # This will wait 30 seconds, then try to delete the file and retry every 30 seconds
        immediate_file_cleanup(file_path)
        print(f"Scheduled cleanup for {filename} with 30-second initial delay and retries")
        
        return response
    except FileNotFoundError:
        flash('File not found')
        return redirect(url_for('index'))

@app.route('/api/analysis_data')
def get_analysis_data():
    """Get analysis data for AJAX requests"""
    # Get file references from session
    analysis_file = session.get('analysis_file')
    
    if not analysis_file:
        return jsonify({'error': 'No analysis data found'}), 404
    
    # Load data from file
    analysis_filepath = os.path.join(app.config['UPLOAD_FOLDER'], analysis_file)
    if not os.path.exists(analysis_filepath):
        return jsonify({'error': 'Analysis data not found'}), 404
    
    with open(analysis_filepath, 'r') as f:
        analysis_data = json.load(f)
    
    return jsonify(analysis_data)

@app.route('/api/cleanup', methods=['POST'])
def api_cleanup():
    """API endpoint to manually clean up uploads directory and session data"""
    try:
        cleanup_uploads()
        # Clear session data
        session.pop('analysis_file', None)
        session.pop('networks_file', None)
        return jsonify({'success': True, 'message': 'Uploads directory and session data cleaned successfully'})
    except Exception as e:
        return jsonify({'error': f'Error cleaning up: {str(e)}'}), 500

if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    # For production, set debug=False
    app.run(debug=debug_mode, host=host, port=port)
