"""
Simple status API for the Slack bot
Provides health checks and query interface for the admin UI
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/status', methods=['GET'])
def get_status():
    """
    Returns the current status of the bot
    """
    try:
        # Check if required files exist
        chunks_exist = os.path.exists('chunks.json')
        vectors_exist = os.path.exists('vectors.json')

        # Check if we can load the data
        chunks_loaded = False
        vector_count = 0

        if chunks_exist:
            try:
                with open('chunks.json', 'r') as f:
                    chunks = json.load(f)
                    chunks_loaded = True
                    vector_count = len(chunks)
            except Exception as e:
                logger.error(f"Error loading chunks: {e}")

        return jsonify({
            'status': 'ok',
            'timestamp': datetime.now().isoformat(),
            'chunks_exist': chunks_exist,
            'vectors_exist': vectors_exist,
            'chunks_loaded': chunks_loaded,
            'vector_count': vector_count,
            'ready': chunks_loaded and vectors_exist
        })

    except Exception as e:
        logger.error(f"Status check error: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/query', methods=['POST'])
def handle_query():
    """
    Processes a query and returns the response
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # Import here to avoid circular imports
        from query import answer_question

        start_time = datetime.now()
        answer = answer_question(query)
        end_time = datetime.now()

        response_time = (end_time - start_time).total_seconds() * 1000  # ms

        return jsonify({
            'query': query,
            'answer': answer,
            'response_time': response_time,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Query processing error: {e}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
