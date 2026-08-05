"""
Start both Flask apps:
  - Dashboard      → http://127.0.0.1:5000
  - Patient Form   → http://127.0.0.1:5001

Run:  python start.py
"""
import subprocess, sys, time, os, webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
PY   = sys.executable

print("Starting Dashboard      → http://127.0.0.1:5000")
p1 = subprocess.Popen([PY, os.path.join(ROOT, 'app.py')],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Starting Patient Form   → http://127.0.0.1:5001")
p2 = subprocess.Popen([PY, os.path.join(ROOT, 'predict_app.py')],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

time.sleep(2)
print("\nBoth servers are running. Press Ctrl+C to stop.\n")
webbrowser.open('http://127.0.0.1:5000')
webbrowser.open('http://127.0.0.1:5001')

try:
    p1.wait()
    p2.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
    p1.terminate()
    p2.terminate()
