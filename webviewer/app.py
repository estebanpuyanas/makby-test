"""
Simple Flask web viewer for the makby-test exercises.
Run with:  .venv/bin/python webviewer/app.py
then open  http://localhost:5000
"""
import os, sys

# Ensure src/ utilities are importable from project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, 'src')
sys.path.insert(0, SRC)

from flask import Flask, render_template, send_file, Response
import markdown as md_lib

app = Flask(__name__, template_folder='templates')

# ── Paths ────────────────────────────────────────────────────────────────────
GCODE_PATH = os.path.join(SRC, 'exercise1', 'exercise1.gcode')
MD_PATH    = os.path.join(SRC, 'exercise3', 'solution.md')

GCODE_PREVIEW_LINES = 40   # lines shown by default before "expand"

# ── Routes: pages ────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/exercise/1')
def exercise1():
    # Read gcode preview
    with open(GCODE_PATH, 'r') as f:
        all_lines = f.readlines()
    preview = ''.join(all_lines[:GCODE_PREVIEW_LINES])
    total   = len(all_lines)
    return render_template('ex1.html',
                           gcode_preview=preview,
                           gcode_total=total,
                           preview_lines=GCODE_PREVIEW_LINES)

@app.route('/exercise/2')
def exercise2():
    return render_template('ex2.html')

@app.route('/exercise/3')
def exercise3():
    with open(MD_PATH, 'r') as f:
        raw = f.read()
    html_body = md_lib.markdown(raw, extensions=['extra', 'toc', 'footnotes'])
    return render_template('ex3.html', md_html=html_body)

# ── Routes: data ─────────────────────────────────────────────────────────────

@app.route('/plot/1.png')
def plot1():
    from plots import gen_ex1_plot
    return Response(gen_ex1_plot(), mimetype='image/png')

@app.route('/plot/2.png')
def plot2():
    from plots import gen_ex2_plot
    return Response(gen_ex2_plot(), mimetype='image/png')

@app.route('/gcode/full')
def gcode_full():
    """Return the entire gcode file as plain text (used by JS expand button)."""
    with open(GCODE_PATH, 'r') as f:
        content = f.read()
    return Response(content, mimetype='text/plain')

@app.route('/gcode/download')
def gcode_download():
    return send_file(GCODE_PATH,
                     as_attachment=True,
                     download_name='exercise1.gcode',
                     mimetype='text/plain')

@app.route('/ex3/print')
def ex3_print():
    """Standalone print-friendly page for exercise 3 (for save-as-PDF)."""
    with open(MD_PATH, 'r') as f:
        raw = f.read()
    html_body = md_lib.markdown(raw, extensions=['extra', 'toc', 'footnotes'])
    return render_template('ex3_print.html', md_html=html_body)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
