import subprocess

def test_streamlit_runs():
    try:
        process = subprocess.run(
            ["streamlit", "run", "dashboard_app.py", "--server.headless", "true"],
            cwd = "monitoring",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        assert process.returncode == 0, f"streamlit failed to launch: /n{process.stderr.decode()}"
    except subprocess.TimeoutExpired:
        assert True