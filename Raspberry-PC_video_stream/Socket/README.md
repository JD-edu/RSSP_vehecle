# 라즈베리파이 - PC socket 카메라 영상 전 파이썬 코드 에제 
## 라즈베리파이 - PC UDP 통신
라즈베리파이에서 촬영한 영상을 UDP 소켓으로 전송려면 다음 두가지 파이썬 코드를 사용합니다.

### rpi-pc-video-server-udp.py
이 파이썬 코드는 라즈베리파이에서 실행됩니다. 이 예제에서 라즈베리파이는 서버의 역할입니다.
라즈베리파이에 연결된 pi 카메라 혹은 웹캠을 통하여 촬영된 비디오를 클라이언트로 전송합니다. 

#### UDP 소켓 
이 예제는 UDO 소켓을 사용합니다. 라즈베리파이의 IP번호를 파악해서 다음 코드에 넣어주어야 합니다. 
영상정보는 1~2프레임의 손실이 생겨도 큰 문제가 없으므로 TCP 대신 UDP 소켓을 사용합니다.  

```python
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '172.31.99.46'#  socket.gethostbyname(host_name)
```
#### 서버의 실행 
파이썬 코드를 터미널이나 VS Code를 실행하면 다음과 같이 실행이 됩니다. 이 상태는 클라이언트를 기다리는 상태입니다. 

```
conner@ubuntu_vb$ python rpi-pc-video-server-udp.py
192.168.35.54
Listening at: ('192.168.35.54', 9999)
```

### rpi-pc-video-client-udp.py
이 파이썬 코드는 PC에서 실행합니다. 이 예제에서 PC는 클라이언트 역할입니다. 
이미 라즈베리파이에서 서버역할의 파이썬 코드(rpi-pc-video-server-udp.py)를 실행한 상태에서 이 파이썬 코드를 실행하면 
라즈베리파이에서 전송한 영상이 OpenCV창에 디스플레이 됩니다. 

#### UDP 소켓사용 
클라이언트 코드에서는 서버의 IP를 셋팅합니다. 
```python
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '172.30.1.62'#  socket.gethostbyname(host_name)
```

#### 클라이언트의 실행 
라즈베리파이에서 서버가 실행된 상태에서, 이 클라이언트 코드를 터미널이나 VS Code에서 실행합니다. 
서버와 연결이 되면 다음과 같은 메시지가 터미널에 나오고 영상윈도가 듭니다. 

```python
PS C:\Users\conne\Downloads\RSSP_vehecle-main\Raspberry-PC_video_stream\Socket python .\rpi-pc-video-client-udp.py
192.168.35.54
C:\Users\conne\Downloads\RSSP_vehecle-main\Raspberry-PC_video_stream\Socket\rpi-pc-video-client-udp.py:21: DeprecationWarning: The binary mode of fromstring is deprecated, as it behaves surprisingly on unicode inputs. Use frombuffer instead
  npdata = np.fromstring(data,dtype=np.uint8)
```

## TCP 통신 
라즈베리파이와 PC 사이의 데이터 통신을 위해서는 TCP 프로토콜을 이용해서 통신을 합니다. 
다음 두가지 파이썬 코드를 사용합니다. 

### rpi-pc-video-server-multi.py
이 파이썬 코드는 라즈베리파이에서 실행됩니다. 이 예제에서 라즈베리파이는 서버의 역할입니다.
라즈베리파이에 연결된 pi 카메라 혹은 웹캠을 통하여 촬영된 비디오를 클라이언트로 전송합니다. 
그리고 별도의 thread를 만들어서 TCP 소켓을 열고 이 소켓을 통해 데이터 통신을 수행합니다. 

```python
class TcpThread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_address = (self.ip, self.port)
        self.tcp_server.bind(tcp_address) 
        print('Listening TCP at: ',tcp_address)
...
```

### rpi-pc-video-client-multi.py
이 파이썬 코드는 PC에서 실행합니다. 이 예제에서 PC는 클라이언트 역할입니다. 
이미 라즈베리파이에서 서버역할의 파이썬 코드(rpi-pc-video-server-multi.py)를 실행한 상태에서 이 파이썬 코드를 실행하면 
라즈베리파이에서 전송한 영상이 OpenCV창에 디스플레이 됩니다. 
PC에서 라즈베리파이로 데이터를 보내기 위해서 pygame 모듈을 사용합니다. 서버와 클라이언트 코드를 별도의 터미널에서 실행하면 클라이언트 코드로부터 pygame 창이 뜹니다. 
여기서 4방향 화살표키를 누르면 서버 터미널에서 눌러진 키를 표시해 줍니다. 
