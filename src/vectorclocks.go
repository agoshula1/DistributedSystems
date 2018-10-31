/* Vector Clock solution*/

package main

import {
  "fmt"
}

//since max function for integers does not exist in "math" library
func max(x, y int) int {
    if x < y {
      return y
    }
    return x
}

type VClock struct {
  value = make(map[string]int)
}

func (v *VClock) increment(nodeId string) void {
  //check if clock for node has been initialized
  elem, ok := v.value[nodeId]
  if ok {
    v.value[nodeId] += 1
  } else {
    //initialize node clock
    v.value[nodeId] = 1
  }
}

func (v *Vclock) merge(other *VClock) void {
  result = make(map[string]int)
  //todo
}
