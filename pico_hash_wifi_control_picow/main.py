from hashmoves import HashMoves
from hashfacialexp import HashFacialExp
from machine import I2C, Pin
from time import sleep
import network
import socket

ssid = 'YOUR WIFI NETWORK NAME'
password = 'YOUR WIFI NETWORK PASSWORD'

sda = Pin(0)
scl = Pin(1)
id = 0
i2c = I2C(0, sda=sda, scl=scl)

hf=HashFacialExp()  
hm=HashMoves()

hf.initialize(i2c)
hm.initialize(i2c)
hf.default_face()
sleep(2)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Pico Hash Control</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
            </head>
            <body>
            <div class="container">
            <h1 class="text-center">Hash Robotics</h1>
            <div class="row">
            <h2 class="text-center">Pico Hash Face Expression</h2>
            <div style="padding:10px" class="col-sm-12">                        
            <div class="col-sm-4"><form action="./default_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Default Face" /></form></div>
            <div class="col-sm-4"><form action="./happy_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Happy Face" /></form></div>
            <div class="col-sm-4"><form action="./sad_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Sad Face" /></form></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"><form action="./eyeclose_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Eye Close" /></form></div>
            <div class="col-sm-4"><form action="./blink"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Eye Blink" /></form></div>
            <div class="col-sm-4"><form action="./sleep_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Sleep Face" /></form></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"><form action="./wink_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Wink Face" /></form></div>
            <div class="col-sm-4"><form action="./hardcry_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Cry Face" /></form></div>
            <div class="col-sm-4"><form action="./love_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Love Face" /></form></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"><form action="./angry_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Angry Face" /></form></div>
            <div class="col-sm-4"><form action="./shock_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Shock Face" /></form></div>
            <div class="col-sm-4"><form action="./default_face"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Normal Face" /></form></div>			
            </div>
            </div>

            <div class="row">
            <h2 class="text-center">Pico Hash Body Movements</h2>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"></div>
            <div class="col-sm-4"><form action="./move_forward"><input class="btn btn-success btn-lg btn-block" type="submit" value="Move Forward" /></form></div>
            <div class="col-sm-4"></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"><form action="./turn_left"><input class="btn btn-success btn-lg btn-block" type="submit" value="Turn Left" /></form></div>
            <div class="col-sm-4"><form action="./initial_position"><input class="btn btn-success btn-lg btn-block" type="submit" value="Default Pose" /></form></div>
            <div class="col-sm-4"><form action="./turn_right"><input class="btn btn-success btn-lg btn-block" type="submit" value="Turn Right" /></form></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"></div>
            <div class="col-sm-4"><form action="./move_backward"><input class="btn btn-success btn-lg btn-block" type="submit" value="Move Backward" /></form></div>
            <div class="col-sm-4"></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"><form action="./say_hi"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Say Hi" /></form></div>
            <div class="col-sm-4"><form action="./hands_up"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Hands Up" /></form></div>
            <div class="col-sm-4"><form action="./hands_down"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Hands Down" /></form></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"><form action="./side_move_left"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Side Move Left" /></form></div>
            <div class="col-sm-4"><form action="./flying_move"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Flying Move" /></form></div>
            <div class="col-sm-4"><form action="./side_move_right"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Side Move Right" /></form></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"><form action="./left_slide_wave"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Left Wave Move" /></form></div>
            <div class="col-sm-4"><form action="./leg_head_shake"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Leg Head Shake" /></form></div>
            <div class="col-sm-4"><form action="./right_slide_wave"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Right Wave Move" /></form></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"><form action="./leg_shake"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Leg Shake" /></form></div>
            <div class="col-sm-4"><form action="./hand_straight_shake"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Hand Straight Shake" /></form></div>
            <div class="col-sm-4"><form action="./jump"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Jump" /></form></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"><form action="./left_hand_balance"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Left Hand Balance" /></form></div>
            <div class="col-sm-4"><form action="./side_shake"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Side Shake" /></form></div>
            <div class="col-sm-4"><form action="./right_hand_balance"><input class="btn btn-primary btn-lg btn-block" type="submit" value="Right Hand Balance" /></form></div>
            </div>
            </div>
            </div>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start a web server
    state = ''
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/default_face?':
            hf.default_face()
        elif request =='/happy_face?':
            hf.happy_face()
        elif request =='/sad_face?':
            hf.sad_face()
        elif request =='/eyeclose_face?':
            hf.eyeclose_face()    
        elif request =='/blink?':
            hf.blink(3) 
        elif request =='/sleep_face?':
            hf.sleep_face(3)
        elif request =='/wink_face?':
            hf.wink_face()
        elif request =='/hardcry_face?':
            hf.hardcry_face(3)
        elif request =='/love_face?':
            hf.love_face()
        elif request =='/angry_face?':
            hf.angry_face()
        elif request =='/shock_face?':
            hf.shock_face()
        elif request =='/default_face?':
            hf.default_face()
            
        elif request =='/move_forward?':
            hm.move_forward(500,5)
        elif request =='/turn_left?':
            hm.turn_left(500,5)
        elif request =='/initial_position?':
            hm.initial_position()
        elif request =='/turn_right?':
            hm.turn_right(500,5)
        elif request =='/move_backward?':
            hm.move_backward(500,5)
        elif request =='/say_hi?':
            hm.say_hi(2000,2)
        elif request =='/hands_up?':
            hm.hands_up(2000,1)
        elif request =='/hands_down?':
            hm.hands_down(2000,1)
        elif request =='/side_move_left?':
            hm.side_move_left(500,5)
        elif request =='/flying_move?':
            hm.flying_move(1000,3)
        elif request =='/side_move_right?':
            hm.side_move_right(500,5)
        elif request =='/left_slide_wave?':
            hm.left_slide_wave(2000,3)
        elif request =='/leg_head_shake?':
            hm.leg_head_shake(1000,3)
        elif request =='/right_slide_wave?':
            hm.right_slide_wave(2000,3)
        elif request =='/leg_shake?':
            hm.leg_shake(1000,3)
        elif request =='/hand_straight_shake?':
            hm.hand_straight_shake(1000,3)
        elif request =='/jump?':
            hm.jump(1000,3)
        elif request =='/left_hand_balance?':
            hm.left_hand_balance(2000,3)
        elif request =='/side_shake?':
            hm.side_shake(1000,2)
        elif request =='/right_hand_balance?':
            hm.right_hand_balance(2000,3)
            
         
        html = webpage(state)
        client.send(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()


