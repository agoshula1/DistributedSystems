from vectorclock import VClock
import threading

#mutex mostly to avoid interleaving of output from different nodes
process_mutex = threading.Semaphore(1)
class Node():
    def __init__(self, id):
        self.id = id
        self.vector = VClock()
        self.mutex = threading.Semaphore(1) #protect vector from concurrent access

    #send vector to other node for merging
    def send_message(self, other):
        self.mutex.acquire()
        self.vector.increment(self.id) #update current node's clock before sending
        process_mutex.acquire()
        print "{} sending message to {}\n".format(self.id, other.id)
        print "{}: {}\n".format(self.id,self.vector.value)
        process_mutex.release()
        copy = self.vector.value.copy()
        self.mutex.release()
        other.receive_message(self.id,copy)

    #receive vector from other node for merging
    def receive_message(self, other_id, other_clock):
        self.mutex.acquire()
        self.vector.merge(other_clock)
        self.vector.increment(self.id) #update current node's clock after merge
        process_mutex.acquire()
        print "{} receiving message from {}\n".format(self.id,other_id)
        print "{}: {}\n".format(self.id,self.vector.value)
        process_mutex.release()
        self.mutex.release()

'''
testing framework - checking output of simulation

loosely based on example given in text book:
http://book.mixu.net/distsys/time.html
'''
def node_A(nodes):
    nodes["A"].send_message(nodes["B"])

def node_B(nodes):
    B = nodes["B"]
    A = nodes["A"]
    C = nodes["C"]
    B.send_message(A)
    B.send_message(C)
    B.send_message(C)

def node_C(nodes):
    B = nodes["B"]
    A = nodes["A"]
    C = nodes["C"]
    C.send_message(B)
    C.send_message(A)
    C.send_message(A)

def simulation():
    nodes = {"A":Node("A"),"B":Node("B"),"C":Node("C")}
    threads = []

    A = threading.Thread(target=node_A, args=(nodes,))
    threads.append(A)
    B = threading.Thread(target=node_B, args=(nodes,))
    threads.append(B)
    C = threading.Thread(target=node_C, args=(nodes,))
    threads.append(C)
    C.start()
    B.start()
    A.start()
    for n in range(3):
        #wait for threads to complete
        threads[n].join()

#run test
simulation()
