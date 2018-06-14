import math
import numpy as np 
import socket

# declare global variables in separate module and import it in all module that require it
a_bq = []
a_mq = []
w_mq = []
a_localq = []
d_q = []
sc_q = []
sd_q = []

def gpd():
    # a_b is vector
    global a_bq, a_mq, w_mq, a_localq, d_q, sc_q, sd_q

    t = len(a_bq) - 1
    #
    s = 10
    if t >= 2*s + 1:
        a_local_squared = 0
        j = t - 1
        while j <= t - 1 and j >= t - s - 1:
            k = j - s
            a_avg = 0
            while k <= j:
                a_avg = a_avg + a_bq[k]
                k = k + 1
            a_avg = a_avg/(2*s + 1)

            a_local_squared += (a_bq[-1] - a_avg)**2    # check this
            j = j - 1

        a_local_squared /= 2*s + 1
        a_local = a_local_squared**(0.5)
        a_localq.append(a_local) 
    else:
        j = t - 1
        k = 0
        a_avg = 0
        while k <= j:
            a_avg = a_avg + a_bq[k]
            k += 1
        a_local_squared = a_avg**(2)/(k + 1)
        a_local = a_local_squared**(0.5)
        a_localq.append(a_local)
        #print(a_local_squared)

    d_new = np.linalg.norm(a_localq[-1] - a_localq[-2]) + np.linalg.norm(a_mq[-1] - a_mq[-2]) + np.linalg.norm(w_mq[-1] - w_mq[-2])
    d_q.append(d_new)
    sc_new = sum(d_q[-5:-1])/5
    sc_q.append(sc_new)
    sd_new = (sd_q[-2] + sc_q[-1])/2
    sd_q.append(sd_new)

    if sd_q[-1] <= sc_q[-1]:
        max_cd = sc_q[-1]
    else:
        max_cd = sd_q[-1]
    
    if len(sc_q) <= 100:
        Mc = max(sc_q)
    else:
        Mc = max(sc_q[-100:-50])
    if len(sd_q) <= 100:
        Md = max(sd_q)
    else:
        Md = max(sd_q[-100:-50])
    

    th = abs(Mc - Md)
    
    if max_cd <= th:
        return True, th
    else:
        return False, th


#initializations
sc_q.append(0.8)
sd_q.extend([0, 0])
a_localq.extend([0,0,0,0,0])  
a_mq.extend([0,0,0,0,0])
w_mq.extend([0,0,0,0,0])
d_q.extend([0,0,0,0,0])

UDP_IP = "192.168.43.30"
UDP_PORT = 5000
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
count = 0

while True:
    raw_data, addr = sock.recvfrom(1024)
    data_str = raw_data.split()
    #data_str[0] = ''.join(list(data_str[0])[2:])
    #data_str[-1] = ''.join(list(data_str[-1])[:-3])
    data = [float(x) for x in data_str]
    a_bq.append(np.array([data[0], data[1], data[2]]).reshape(3, 1))
    a_mq.append(np.array([data[3], data[4], data[5]]).reshape(3, 1))
    w_mq.append(np.array([data[6], data[7], data[8]]).reshape(3, 1))
    val, th= gpd()
    count += 1
    print(int(val), th, count)
    #print(data)



