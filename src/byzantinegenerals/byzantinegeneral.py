import threading
import copy
import json

global ATTACK
ATTACK = True
global RETREAT
RETREAT = False

class General():
    def __init__(self, num, loyalty):
        self.id = num
        self.loyal = loyalty #expecting boolean
        self.vals_received = []
        self.vals_mutex = threading.Semaphore(1)

    def send_value(self, val, m, lts_ids, ids_lts_mapping):
        #safely access list of values received
        self.vals_mutex.acquire()
        self.vals_received.append(val)
        self.vals_mutex.release()

        if m > 0:
            threads = []
            #make deep copy of list of lieutenant ids
            ids_copy = copy.deepcopy(lts_ids)
            ids_copy.remove(self.id)

            #send message to each of the other lieutenants
            for id in ids_copy:
                l = ids_lts_mapping[id] #lookup lietenant by id
                send_val = val
                if (not self.loyal) and (l.id % 2 == 0):
                    #send reverse order
                    send_val = not val
                t = threading.Thread(target=General.send_value, args=(l, send_val, m-1, ids_copy, ids_lts_mapping))
                threads.append(t)
                t.start()

            #wait for threads to finish
            for n in range(len(threads)):
                threads[n].join()

def majority_vote(votes):
    AVotes, RVotes = 0, 0
    #poll votes
    for v in votes:
        if v == ATTACK:
            AVotes += 1
        elif v == RETREAT:
            RVotes += 1
        #ignore other values for votes

    #determine relative majority
    if AVotes > RVotes:
        return ATTACK
    elif AVotes < RVotes:
        return RETREAT
    else:
        return None #tie

def main():
    #read inputs from file
    m = 1 #number of traitors
    G0 = General(0,False) #commander
    generals = [General(1,False), General(2,True), General(3,False)]
    generals += [General(i, True) for i in range(4,7)]
    Oc = ATTACK #commander's order (check != null)

    threads = []
    id_ls = [i for i in range(1, len(generals)+1)]
    id_gen_mapping = {}
    #create mapping between generals and their ids
    for i in range(1, len(generals)+1):
        id_gen_mapping[i] = generals[i-1]

    #send message to each general
    for g in generals:
        t = threading.Thread(target=General.send_value, args=(g, Oc, m, id_ls, id_gen_mapping))
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

main()
