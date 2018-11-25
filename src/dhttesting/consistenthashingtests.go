package main

import (
	"fmt"
	"github.com/arriqaaq/xring"
	"math/rand"
  "time"
)

// tests adapted from example code by Farhan Ali Khan:
// https://github.com/arriqaaq/xring/tree/master/examples

func test1(ld float64) {
	//initialize nodes and hash ring
  nodes := []string{"a", "b", "c", "d"}
	cnf := &xring.Config{
		VirtualNodes: 100,
		LoadFactor:   ld,
	}
	hashRing := xring.NewRing(nodes, cnf)

	keyCount := 1000000
  //to record distribution of keys among  nodes
	distribution := make(map[string]int)
	key := make([]byte, 4)

  //calculate key distribution
	for i := 0; i < keyCount; i++ {
		rand.Read(key)
    //find node where key is stored
		node, err := hashRing.Get(string(key))
		if err != nil {
			fmt.Println("error: ", err)
			continue
		}
		hashRing.Done(node)
		distribution[node]++
	}
	for node, count := range distribution {
		fmt.Printf("node: %s, key count: %d\n", node, count)
	}
}

func test2(deleteFreq int) {
  nodes := []string{"a", "b", "c", "d", "e", "f", "g", "h"}
	cnf := &xring.Config{
		VirtualNodes: 100,
		LoadFactor:   2,
	}
	hashRing := xring.NewRing(nodes, cnf)

  keyCount := 5000000
  distribution := make(map[string]int)
  key := make([]byte, 4)
  nextRemoved := 0

	for i := 0; i < keyCount; i++ {
		//remove a node occasionally to imitate partition
    if i % deleteFreq == 0  {
      fmt.Printf("next to be removed: %s\n", nodes[nextRemoved])
      hashRing.Remove(nodes[nextRemoved]) //causes runtime error
      nextRemoved++
    }
    rand.Read(key)
		node, err := hashRing.Get(string(key))
		if err != nil {
			fmt.Println("error: ", err)
			continue
		}
		hashRing.Done(node)
		distribution[node]++
	}
	for node, count := range distribution {
		fmt.Printf("node: %s, key count: %d\n", node, count)
	}
}

func main() {
  //experiment with different load balances to observe impact to performance (if any)
  start := time.Now()
  test1(1)
  end := time.Now()
  difference := end.Sub(start)
  fmt.Printf("Load of 1: Time elapsed (sec) = %f\n", difference.Seconds())

  start = time.Now()
  test1(100)
  end = time.Now()
  difference = end.Sub(start)
  fmt.Printf("Load of 100: Time elapsed (sec) = %f\n", difference.Seconds())

  start = time.Now()
  test1(10000)
  end = time.Now()
  difference = end.Sub(start)
  fmt.Printf("Load of 10000: Time elapsed (sec) = %f\n", difference.Seconds())

  //trying to model partitions (causes run time error, seems to be from a bug
  //in the dht implementation)
  test2(1000000)
}
