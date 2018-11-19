from general import General
import threading
import json

global ATTACK
ATTACK = True
global RETREAT
RETREAT = False

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

def run_test(m, generals, Oc):
    G0 = generals.pop(0) #commander

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
    passed = False if Oc != decision else True #according to IC2 from paper

    print "Test passed: {}".format(passed)

def main():
    #read inputs from file
    with open('input.json') as f:
        inputs = json.load(f)

    for test in inputs:
        m = test["m"] #number of traitors
        general_objs = test["G"]
        generals = []
        for g in general_objs:
            key = g.keys()[0]
            generals.append(General(int(key), g[key]))
        Oc = ATTACK if test["Oc"] == "ATTACK" else RETREAT

        run_test(m, generals, Oc)

main()
