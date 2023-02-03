import subprocess


class Builder():
    """
    This class is used to build the application using pyinstaller
    """
    def __init__(self):
        pass
    def _run_pyinsteller(self):
        build_script = "npm run build"
        pipe = subprocess.Popen(build_script.split(" "), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if pipe.stdout:
            for line in pipe.stdout.readlines():
                if(line.find(b"completed successfully.") >= 0):
                    return True
        return False

    def start(self):
        package = self._run_pyinsteller()
        if not package:
            print("Error: Package failed")
            return False
        
        # TODO: use nsis or other tools to create a installer.
        # pass
        print("Package completed successfully, check the dist/clip-wizard folder for the executable.")

builder = Builder()
builder.start()
