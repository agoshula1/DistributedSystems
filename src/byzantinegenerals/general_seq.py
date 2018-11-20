import threading
import copy

class SeqGeneral(): #calls other lieutenants sequentially
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
            #make copy of list of lieutenant ids
            #shallow copy is fine since list not nested
            ids_copy = copy.copy(lts_ids)
            ids_copy.remove(self.id)

            #send message to each of the other lieutenants
            for id in ids_copy:
                l = ids_lts_mapping[id] #lookup lietenant by id
                send_val = val
                if (not self.loyal) and (l.id % 2 == 0):
                    #send reverse order
                    send_val = not val
                l.send_value(send_val,m-1,ids_copy,ids_lts_mapping)
