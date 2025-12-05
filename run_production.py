import eventlet
eventlet.monkey_patch()

from wsgi import app, socketio
import eventlet.wsgi

if __name__ == "__main__":
    print("🚀 Starting Production Server with Eventlet...")
    print("✅ Serving on http://0.0.0.0:8080")
    
    # Use socketio.run which automatically uses eventlet if installed
    # log_output=True allows us to see the logs
    socketio.run(app, host='0.0.0.0', port=8080, debug=False, use_reloader=False, log_output=True)
