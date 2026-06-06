import subprocess
import sys
import threading
import time

AVAILABLE_COMMANDS = {
    "exit": ["exit", "quit", "stop"],
}

def system():
    if sys.platform == "win32":
        return "windows"
    else:
        return "linux"
    
def stream_output(process, prefix="Launcher"):
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(f"\r[{prefix}]\t{output.strip()}")
            print("\r> ", end="", flush=True)

def exit_processes(processes):
    for process in processes:
        process.terminate()

def main():
    if system() == "windows":
        should_restart = True
        while should_restart:
            should_restart = False
            stop_event = threading.Event()
            backend = None
            whs_frontend = None

            def input_listener():
                while not stop_event.is_set():
                    try:
                        command = input("> ")
                    except (EOFError, KeyboardInterrupt):
                        break

                    command = command.strip().lower()
                    if not command:
                        continue

                    found = False
                    for cmd, aliases in AVAILABLE_COMMANDS.items():
                        if command in aliases:
                            found = True
                            if cmd == "exit":
                                print("\r[Launcher]\tExiting...", flush=True)
                                exit_processes([backend, whs_frontend])
                                stop_event.set()
                            break

                    if not found:
                        print(f"\r[Launcher]\tUnknown command: {command}", flush=True)

            try:
                backend = subprocess.Popen(
                    "venv\\Scripts\\python.exe -m uvicorn main:app --reload",
                    cwd="backend",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                )
                threading.Thread(target=stream_output, args=(backend, "Backend"), daemon=True, name="Backend").start()

                whs_frontend = subprocess.Popen(
                    "npm run dev",
                    cwd="whs",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                )
                threading.Thread(target=stream_output, args=(whs_frontend, "WHS-Frontend"), daemon=True, name="WHS-Frontend").start()

                threading.Thread(target=input_listener, daemon=True, name="InputListener").start()

                while not stop_event.is_set() and backend.poll() is None and whs_frontend.poll() is None:
                    time.sleep(0.5)
            except KeyboardInterrupt:
                print("\r[Launcher]\tExiting...", flush=True)
                exit_processes([backend, whs_frontend])
                sys.exit(0)

            exit_processes([backend, whs_frontend])
            if backend:
                backend.wait()
            if whs_frontend:
                whs_frontend.wait()

        sys.exit(0)
    else:
        print("Linux & MacOS support is not implemented yet.")
        sys.exit(1)

if __name__ == "__main__":
    main()
