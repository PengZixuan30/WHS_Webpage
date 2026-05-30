import subprocess
import sys
import os
import threading
import signal
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
IS_WIN = sys.platform == "win32"

POPFLAGS = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW} if IS_WIN else {}


def find_venv_python(backend_dir: str) -> str:
    if IS_WIN:
        candidate = os.path.join(backend_dir, "venv", "Scripts", "python.exe")
    else:
        candidate = os.path.join(backend_dir, "venv", "bin", "python")

    if not os.path.isfile(candidate):
        print(f"[ERROR] Python venv not found: {candidate}")
        print("  Run: cd backend && python -m venv venv")
        sys.exit(1)
    return candidate


def stream_output(pipe, prefix: str):
    try:
        for line in iter(pipe.readline, ""):
            if line:
                print(f"{prefix} {line}", end="", flush=True)
    except ValueError:
        pass
    finally:
        pipe.close()


def main():
    print("=" * 50)
    print("  WHS Webpage — Starting Services")
    print("=" * 50)
    print()

    backend_dir = os.path.join(ROOT, "backend")
    python_exe = find_venv_python(backend_dir)

    backend = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "main:app",
         "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace",
        **POPFLAGS,
    )
    print("[Backend]  Launching FastAPI on http://localhost:8000 ...")

    frontend_dir = os.path.join(ROOT, "whs")
    npm_cmd = "npm.cmd" if IS_WIN else "npm"

    frontend = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace",
        **POPFLAGS,
    )
    print("[WHS-Frontend] Launching Vite on http://localhost:5173 ...")

    t1 = threading.Thread(
        target=stream_output,
        args=(backend.stdout, "[Backend] "),
        daemon=True,
    )
    t2 = threading.Thread(
        target=stream_output,
        args=(frontend.stdout, "[WHS-Frontend]"),
        daemon=True,
    )
    t1.start()
    t2.start()

    print()
    print("All services running. Press Ctrl+C to stop.")
    print()

    def cleanup(sig=None, frame=None):
        print("\nShutting down...")
        for name, proc in (("Backend", backend), ("WHS-Frontend", frontend)):
            if proc.poll() is not None:
                print(f"[{name}] Already stopped.")
                continue

            if IS_WIN:
                proc.kill()
                proc.wait(timeout=5)
                print(f"[{name}] Stopped.")
            else:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                    print(f"[{name}] Normal shutdown.")
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
                    print(f"[{name}] Forced shutdown (timeout).")
        print("All services stopped.")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        while True:
            if backend.poll() is not None and frontend.poll() is not None:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        cleanup()

    cleanup()


if __name__ == "__main__":
    main()
