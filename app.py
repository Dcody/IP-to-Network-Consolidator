#!/usr/bin/env python3
"""
Flask web application for IP Consolidator
Provides a simple web interface for the consolidation tool
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import os
import json
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
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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
            analysis_data = {
                'filename': filename,
                'host_ips_count': len(host_ips),
                'results': results,
                'frontier': frontier,
                'filepath': filepath,
                'recommended': {
                    'threshold': recommended['threshold'],
                    'score': recommended['score'],
                    'objects_defined': recommended['objects_defined'],
                    'missing_ips_included': recommended['missing_ips_included'],
                    'expansion_percent': recommended['expansion_percent']
                }
            }
            
            # Store in a simple way (in production, use proper session management)
            with open(os.path.join(app.config['UPLOAD_FOLDER'], 'analysis_data.json'), 'w') as f:
                json.dump(analysis_data, f, default=str)
            
            # Store networks as strings for safe JSON serialization
            networks_data = {
                'filename': filename,
                'host_ips_count': len(host_ips),
                'results': results,
                'frontier': frontier,
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
            
            with open(os.path.join(app.config['UPLOAD_FOLDER'], 'networks_data.json'), 'w') as f:
                json.dump(networks_data, f, default=str)
            
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
    try:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'analysis_data.json'), 'r') as f:
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
    except FileNotFoundError:
        flash('No analysis data found. Please upload a file first.')
        return redirect(url_for('index'))

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
        
        # Load the networks data from JSON
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'networks_data.json'), 'r') as f:
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
            
            # Create temporary file
            output_filename = f"asa_output_{threshold}percent.txt"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            write_asa_file(object_lines, group_lines, threshold, output_path)
        else:  # raw format
            # Generate raw IP addresses
            output_filename = f"raw_ips_{threshold}percent.txt"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            with open(output_path, 'w') as f:
                f.write(f"# Raw IP Addresses for {threshold}% threshold\n")
                f.write(f"# Generated from {networks_data['filename']}\n")
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
        
        if not any(filename.startswith(pattern) for pattern in allowed_patterns):
            flash('Invalid file type')
            return redirect(url_for('index'))
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Additional security check - ensure file is within upload directory
        real_file_path = os.path.realpath(file_path)
        real_upload_path = os.path.realpath(app.config['UPLOAD_FOLDER'])
        
        if not real_file_path.startswith(real_upload_path):
            flash('Access denied')
            return redirect(url_for('index'))
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    except FileNotFoundError:
        flash('File not found')
        return redirect(url_for('index'))

@app.route('/api/analysis_data')
def get_analysis_data():
    """Get analysis data for AJAX requests"""
    try:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'analysis_data.json'), 'r') as f:
            analysis_data = json.load(f)
        return jsonify(analysis_data)
    except FileNotFoundError:
        return jsonify({'error': 'No analysis data found'}), 404

if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    # For production, set debug=False
    app.run(debug=debug_mode, host=host, port=port)
