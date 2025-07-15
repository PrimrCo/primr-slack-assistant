"""
Simple status API for the Slack Assistant
Run this alongside the Slack bot to provide status information
"""
from flask import Flask, jsonify
import json
import os
from datetime import datetime
import glob

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def get_status():
    """Get current knowledge base status"""
    try:
        status = {
            "timestamp": datetime.now().isoformat(),
            "data_folder_exists": os.path.exists("data"),
            "total_files": 0,
            "total_chunks": 0,
            "last_indexed": None,
            "index_exists": False,
            "files": []
        }

        # Count files in data directory
        if os.path.exists("data"):
            files = glob.glob("data/*.md") + glob.glob("data/*.txt")
            status["total_files"] = len(files)
            status["files"] = [os.path.basename(f) for f in files]

        # Check chunks.json
        if os.path.exists("chunks.json"):
            with open("chunks.json", "r", encoding="utf-8") as f:
                chunks = json.load(f)
                status["total_chunks"] = len(chunks)

            # Get last modified time
            stat = os.stat("chunks.json")
            status["last_indexed"] = datetime.fromtimestamp(stat.st_mtime).isoformat()

        # Check vector index
        status["index_exists"] = os.path.exists("vectors.json")

        # Load vector info if available
        if os.path.exists("vectors.json"):
            try:
                with open("vectors.json", "r", encoding="utf-8") as f:
                    vector_data = json.load(f)
                    status["vector_count"] = len(vector_data.get("texts", []))
                    status["embedding_model"] = vector_data.get("embedding_model", "unknown")
                    status["vector_dimensions"] = vector_data.get("dimensions", 0)
                    status["vector_created"] = vector_data.get("created_at", None)
            except Exception as e:
                status["vector_error"] = str(e)

        # Load metadata if available
        if os.path.exists("index_info.json"):
            with open("index_info.json", "r", encoding="utf-8") as f:
                metadata = json.load(f)
                status.update(metadata)

        return jsonify(status)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reindex', methods=['POST'])
def trigger_reindex():
    """Trigger re-indexing of the knowledge base"""
    try:
        import subprocess
        result = subprocess.run(
            ["python", "enhanced_ingest.py"],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            return jsonify({
                "message": "Re-indexing completed successfully",
                "output": result.stdout
            })
        else:
            return jsonify({
                "error": "Re-indexing failed",
                "output": result.stderr
            }), 500

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Re-indexing timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "primr-slack-assistant"
    })

if __name__ == '__main__':
    # Run on a different port than the main Next.js app
    app.run(host='0.0.0.0', port=5001, debug=True)
