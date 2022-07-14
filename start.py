from minecraft.networking.connection import ServerThread

thread = ServerThread(100)
thread.start()

try:
    input("Press Enter to exit...\n")
except SyntaxError:
    pass

thread.close_server()
thread.join()