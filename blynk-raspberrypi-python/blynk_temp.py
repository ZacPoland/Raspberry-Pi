import BlynkLib
from BlynkTimer import BlynkTimer
import socket
import DHT11

# Monkey-patch getaddrinfo to prefer IPv4 addresses
_old_getaddrinfo = socket.getaddrinfo
def ipv4_getaddrinfo(host, port, *args, **kwargs):
    results = _old_getaddrinfo(host, port, *args, **kwargs)
    # Filter for IPv4 (AF_INET)
    ipv4_results = [r for r in results if r[0] == socket.AF_INET]
    if ipv4_results:
        return ipv4_results
    return results # fallback if no IPv4 result
 
socket.getaddrinfo = ipv4_getaddrinfo
dht11 = DHT11.DHT11(17)


def getTem():
    count = 0
    while True:
        result = dht11.read_data()
        count+=1
        if result:
            break
        if count>=100:
            return None
    temp=float(f"{result[1]}")
    print("Temperature: "+str(temp))
    return temp

# Blynk
BLYNK_AUTH = 'o1pclGuxjW2rhtyGZ9w_SmRzHiAtu8Fu' #'YourAuthToken'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()


# Will only run once after 2 seconds
def hello_world():
    print("Start!")


# Will Print Every 10 Seconds
def publish_data():
    tempVal=getTem()
    blynk.virtual_write(5, tempVal)


# Add Timers
timer.set_timeout(2, hello_world)
timer.set_interval(10, publish_data)


while True:
    blynk.run()
    timer.run()
