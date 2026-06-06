import subprocess
import sys
import threading
import time

AVAILABLE_COMMANDS = {
    "exit": ["exit", "quit", "stop"],
    "restart": ["restart", "reload", "r"],
    "help": ["help", "?"]
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
            print(f"\b\b[{prefix}] {output.strip()}")
            print("> ", end="", flush=True)

def exit_processes(processes):
    for process in processes:
        process.terminate()

def main():
    if system() == "windows":
        def input_listener():
            while True:
                try:
                    command = input("> ")
                except (EOFError, KeyboardInterrupt):
                    print("\b\bExiting...")
                    exit_processes([backend, whs_frontend])
                    break

                found = False
                for cmd, aliases in AVAILABLE_COMMANDS.items():
                    if command.lower() in aliases:
                        found = True
                        if cmd == "exit":
                            print("\b\bExiting...")
                            exit_processes([backend, whs_frontend])
                            backend.wait()
                            whs_frontend.wait()
                            break
                        elif cmd == "restart":
                            print("\b\bRestarting...")
                            exit_processes([backend, whs_frontend])
                            backend.wait()
                            whs_frontend.wait()
                            return main()
                        elif cmd == "help":
                            print("\b\bAvailable commands:")
                            for cmd_name, aliases in AVAILABLE_COMMANDS.items():
                                print(f"  {cmd_name}: {', '.join(aliases)}")
                        else:
                            print(f"\b\bUnknown command: {command}")
                
                if not found:
                    print(f"\b\bUnknown command: {command}")

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
            
            while backend.poll() is None and whs_frontend.poll() is None:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\b\bExiting...")
            exit_processes([backend, whs_frontend])
            sys.exit(0)
            return
    else:
        print("Linux & MacOS support is not implemented yet.")
        sys.exit(1)
        return
    exit_processes([backend, whs_frontend])
    sys.exit(0)
    return

if __name__ == "__main__":
    main()
