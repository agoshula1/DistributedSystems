class VClock():
    def __init__(self):
        self.value = {}

    def increment(self, nodeId):
      #check if clock for node has been initialized
      if self.value.has_key(nodeId):
          self.value[nodeId] += 1
      else:
          #initialize node clock
          self.value[nodeId] = 1

    def merge(self, other_value):
      result = {}
      a = self.value
      b = other_value

      #find union of key sets
      concat_keys = set(a.keys()).union(b.keys())

      #find max value between both nodes for each clock
      for i in range(len(concat_keys)):
          key = concat_keys.pop()
          if not a.has_key(key):
              result[key] = b[key]
          elif not b.has_key(key):
              result[key] = a[key]
          else:
              result[key] = max(a[key], b[key])
      self.value = result
