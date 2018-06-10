import math
import numpy as np 

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
    if t >= 2*s + 1:
        j = t - 1
        a_local_squared = 0
        while j <= t - 1 and j >= t - s - 1:
            k = j - s
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
        while k <= j:
            a_avg = a_avg + a_bq[k]
            k += 1
        a_local_squared = a_avg/(k + 1)
        a_local = a_local_squared**(0.5)
        a_localq.append(a_local)

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
    
    if len(sc_q) <= 15:
        Mc = max(sc_q)
    else:
        Mc = max(sc_q[-15:-5])
    if len(sd_q) <= 15:
        Md = max(sd_q)
    else:
        Md = max(sd_q[-15:-5])
   
    th = abs(Mc - Md)
    
    if max_cd <= th:
        return True
    else:
        return False


#initializations

while True:
    # take data from imu, change the data input to file containing global variables
    f = open("%path%", "r")     
    data = f.read().split()
    # separate data
    # quaternion 
    # callbacks
        



