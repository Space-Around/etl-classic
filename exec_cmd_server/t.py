import psutil


for proc in psutil.process_iter():
    try:
        # Get process name & pid from process object.
        if ('python' in proc.name()):
            path_cmd = proc.cwd()

            print(proc.pid)
            p = psutil.Process(proc.ppid())
            print(p.open_files())

            # print(dir(proc))

            if 'bazaraki' in path_cmd:
                proc.kill()

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
