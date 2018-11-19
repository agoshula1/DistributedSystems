from enum import Enum
import threading
import copy

class Order(Enum):
    ATTACK = 1
    RETREAT = 2

class General():
    def __init__(self, num, loyalty):
        self.id = num
        self.loyal = loyalty #expecting boolean
        self.vals_received = []
        self.vals_mutex = threading.Semaphore(1)

    def send_value(self, val, m, lieutenants):
        #safely access list of values received
        self.vals_mutex.acquire()
        self.vals_received.append(val)
        self.vals_mutex.release()

        if m > 0:
            threads = []
            #make deep copy of list of lieutenants
            lts_copy = copy.deepcopy(lieutenants)
            lts_copy.remove(self)

            #send message to each of the other lieutenants
            for l in lts_copy:
                if (not self.loyal) and (l.id % 2 == 0):
                    #send reverse order
                    if val == Order.ATTACK:
                        val = Order.RETREAT
                    else:
                        val = Order.ATTACK
                t = threading.Thread(target=General.send_value, args=(l, val, m-1, lts_copy))
                threads.append(t)
                t.start()

            #wait for threads to finish
            for n in range(len(threads)):
                threads[n].join()

def majority_vote(votes):
    AVotes,RVotes = 0
    #poll votes
    for v in votes:
        if vote == Order.ATTACK:
            AVotes += 1
        elif vote == Order.RETREAT:
            RVotes += 1
        #ignore other values for votes

    #determine relative majority
    if AVotes > RVotes:
        return Order.Attack
    elif AVotes < RVotes:
        return order.RETREAT
    else:
        return None #tie

def main():
    #read inputs from file
    m = 1 #number of traitors
    G0 = General(0,True) #commander
    generals = [General(1,True), General(2,True), General(3,False)]
    Oc = Order.ATTACK #commander's order

    threads = []
    #send message to each general
    for g in generals:
        t = threading.Thread(target=General.send_value, args=(g, Oc, m, generals))
        threads.append(t)
        t.start()

    #wait for threads to finish
    for n in range(len(threads)):
        threads[n].join()

    #calculate relative majority for each general's received values
    gen_votes = [majority_vote(g.vals_received) for g in generals]

    decision = majority_vote(gen_votes)
    passed = False if Oc != decision else True

    print "Test passed: {}".format(passed)
