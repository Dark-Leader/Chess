import subprocess


class Engine:

    def __init__(self):
        self.engine = subprocess.Popen("chess/stockfish.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       universal_newlines=True)

    def put_command(self, command):
        self.engine.stdin.write(command + "\n")

    def get_response(self):
        for line in self.engine.stdout:
            print(line.strip())


