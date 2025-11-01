#!/usr/bin/env python3
"""
Simple HTTP API Server for Breast Cancer AI
Works with the main_simple.py backend without FastAPI dependencies
"""

import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from main_simple import SimpleBreastCancerAPI

class CORSHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler with CORS support"""
    
    def __init__(self, *args, api_instance=None, **kwargs):
        self.api = api_instance
        super().__init__(*args, **kwargs)
    
    def _set_cors_headers(self):
        """Set CORS headers for cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
    
    def _send_json_response(self, data, status_code=200):
        """Send JSON response with proper headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        
        json_data = json.dumps(data, indent=2, default=str)
        self.wfile.write(json_data.encode('utf-8'))
    
    def _send_error_response(self, message, status_code=500):
        """Send error response"""
        error_data = {
            'error': message,
            'status_code': status_code
        }
        self._send_json_response(error_data, status_code)
    
    def _parse_json_body(self):
        """Parse JSON request body"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                return json.loads(body.decode('utf-8'))
            return {}
        except Exception as e:
            raise ValueError(f"Invalid JSON body: {e}")
    
    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/':
                # Root endpoint
                response = {
                    'message': 'Breast Cancer AI API',
                    'version': '1.0.0',
                    'status': 'active',
                    'authentication': 'Hospital staff only',
                    'endpoints': [
                        'GET /health',
                        'GET /models/available',
                        'GET /auth/validate',
                        'POST /analyze/comprehensive',
                        'POST /analyze/genomics',
                        'POST /analyze/imaging',
                        'POST /analyze/clinical-text'
                    ]
                }
                self._send_json_response(response)
                
            elif path == '/health':
                # Health check
                health_data = self.api.health_check()
                self._send_json_response(health_data)
                
            elif path == '/models/available':
                # Available models
                health_data = self.api.health_check()
                if health_data.get('status') == 'healthy':
                    models_data = {
                        'available_modalities': health_data.get('available_modalities', []),
                        'genomics_available': 'genomics' in health_data.get('available_modalities', []),
                        'imaging_available': 'imaging' in health_data.get('available_modalities', []),
                        'nlp_available': 'nlp' in health_data.get('available_modalities', [])
                    }
                    self._send_json_response(models_data)
                else:
                    self._send_error_response('Models not available', 503)
            
            elif path == '/auth/validate':
                # Simple auth validation endpoint
                auth_header = self.headers.get('Authorization', '')
                if auth_header.startswith('Bearer '):
                    # In a real system, validate the token here
                    # For demo, just return success
                    self._send_json_response({
                        'valid': True,
                        'message': 'Token is valid',
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
                else:
                    self._send_json_response({
                        'valid': False,
                        'message': 'No valid token provided'
                    }, 401)
                    
            else:
                self._send_error_response('Endpoint not found', 404)
                
        except Exception as e:
            print(f"GET Error: {e}")
            self._send_error_response(str(e), 500)
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            # Parse request body
            patient_data = self._parse_json_body()
            
            if path == '/analyze/comprehensive':
                # Comprehensive analysis
                result = self.api.comprehensive_analysis(patient_data)
                if 'error' in result:
                    self._send_error_response(result['error'], 500)
                else:
                    self._send_json_response(result)
                    
            elif path == '/analyze/genomics':
                # Genomics analysis
                result = self.api.genomics_analysis(patient_data)
                if 'error' in result:
                    self._send_error_response(result['error'], 500)
                else:
                    self._send_json_response(result)
                    
            elif path == '/analyze/imaging':
                # Imaging analysis
                result = self.api.imaging_analysis(patient_data)
                if 'error' in result:
                    self._send_error_response(result['error'], 500)
                else:
                    self._send_json_response(result)
                    
            elif path == '/analyze/clinical-text':
                # Clinical text analysis
                result = self.api.nlp_analysis(patient_data)
                if 'error' in result:
                    self._send_error_response(result['error'], 500)
                else:
                    self._send_json_response(result)
                    
            else:
                self._send_error_response('Endpoint not found', 404)
                
        except ValueError as e:
            self._send_error_response(f"Invalid request: {e}", 400)
        except Exception as e:
            print(f"POST Error: {e}")
            self._send_error_response(str(e), 500)
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

class APIServer:
    """Simple API Server wrapper"""
    
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.api = SimpleBreastCancerAPI()
        self.server = None
        self.server_thread = None
    
    def create_handler(self):
        """Create request handler with API instance"""
        def handler(*args, **kwargs):
            return CORSHTTPRequestHandler(*args, api_instance=self.api, **kwargs)
        return handler
    
    def start(self):
        """Start the API server"""
        try:
            print(f"🚀 Starting Breast Cancer AI API Server...")
            print(f"📍 Server URL: http://{self.host}:{self.port}")
            
            # Create server
            handler = self.create_handler()
            self.server = HTTPServer((self.host, self.port), handler)
            
            print(f"✅ Server started successfully!")
            print(f"🔗 Available endpoints:")
            print(f"   GET  http://{self.host}:{self.port}/health")
            print(f"   GET  http://{self.host}:{self.port}/models/available")
            print(f"   POST http://{self.host}:{self.port}/analyze/comprehensive")
            print(f"   POST http://{self.host}:{self.port}/analyze/genomics")
            print(f"   POST http://{self.host}:{self.port}/analyze/imaging")
            print(f"   POST http://{self.host}:{self.port}/analyze/clinical-text")
            print(f"")
            print(f"🌐 Frontend can connect to: http://{self.host}:{self.port}")
            print(f"⏹️  Press Ctrl+C to stop the server")
            print(f"=" * 60)
            
            # Start server
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped by user")
            self.stop()
        except Exception as e:
            print(f"❌ Server error: {e}")
            self.stop()
    
    def start_threaded(self):
        """Start server in a separate thread"""
        if self.server_thread and self.server_thread.is_alive():
            print("Server is already running")
            return
        
        self.server_thread = threading.Thread(target=self.start, daemon=True)
        self.server_thread.start()
        time.sleep(1)  # Give server time to start
    
    def stop(self):
        """Stop the API server"""
        if self.server:
            print("🛑 Stopping API server...")
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        
        if self.server_thread:
            self.server_thread = None

def main():
    """Main function to run the server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Breast Cancer AI API Server')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    parser.add_argument('--test', action='store_true', help='Run a quick test of the API')
    
    args = parser.parse_args()
    
    if args.test:
        # Run a quick test
        print("🧪 Testing API functionality...")
        api = SimpleBreastCancerAPI()
        
        # Test health check
        health = api.health_check()
        print(f"Health Check: {health['status']}")
        
        # Test sample analysis
        sample_data = {
            'patient_id': 'API_TEST_001',
            'age': 45,
            'genomic_alterations': [{'gene': 'BRCA1', 'mutation': 'Pathogenic'}],
            'biomarkers': {'ER_status': 'Positive'}
        }
        
        result = api.comprehensive_analysis(sample_data)
        if 'error' not in result:
            print(f"✅ Sample analysis successful")
            print(f"   Patient: {result.get('patient_id')}")
            print(f"   Risk: {result.get('overall_risk_assessment', {}).get('overall_risk', 'N/A')}")
        else:
            print(f"❌ Sample analysis failed: {result['error']}")
        
        return
    
    # Start the server
    server = APIServer(host=args.host, port=args.port)
    server.start()

if __name__ == "__main__":
    main()