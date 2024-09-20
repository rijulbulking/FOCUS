#Module Import
import platform, os, socket, psutil

#Variable Assignment
Platform = platform.system()
with open('WhitePorts.txt', 'r') as WhitelistedPortsFile:
            WhitelistedPortsList = [int(port.strip()) for port in WhitelistedPortsFile.readlines()]

#Function 1
def clear():
  if Platform == 'Linux' or Platform == 'Darwin':
    os.system("clear")

  elif Platform == 'Windows':
    os.system("cls")

#Function 2
OpenPorts = []
target = "127.0.0.1"
def singlePortScanner(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        print(f"{port} is open")
        OpenPorts.append(port)
    except:
        print(f'{port} is closed')
        pass

#Function 3
def PortCloser(port):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conns in proc.connections(kind='inet'):
                if conns.laddr.port == port:
                    print(f"Process {proc.name()} (PID {proc.pid}) is using port {port}")
                    proc.terminate()
                    print('Process terminated')
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
