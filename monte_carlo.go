package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"math/rand"
	"os"
	"time"
)

// This function will generate a random point and test if its inside the circle and add them to the total count
// this will be run in the nodes amount of threads
func monteCarloPi(c chan int, N int) {
	count := 0
	for i := 0; i < N; i++ {
		x := rand.Float64()
		y := rand.Float64()
		if x*x+y*y < 1 {
			count++
		}
	}
	c <- count
}

// This function will run the monteCarloPi function in the nodes amount of threads and then sum the total count and keep track of the time that it took
func monteCarloPi_run(nodes int, points int) (int, time.Duration) {
	c := make(chan int, 1000) //Channels!
	var start_time = time.Now()

	total := 0
	for i := 0; i < nodes; i++ {
		go monteCarloPi(c, points/nodes)
	}
	for i := 0; i < nodes; i++ {
		total += <-c
	}
	return total, time.Since(start_time)
}

// run this function to test the monteCarloPi_run function with multiple nodes and points and output all data to a csv file
func main() {
	//points := [8]int{100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000}
	points := [7]int{100, 1000, 10000, 100000, 1000000, 10000000, 100000000}

	nodes := [6]int{2, 4, 8, 16, 32, 64}

	file, err := os.Create("go_output.csv")

	if err != nil {
		log.Fatal("Cannot create file", err)
	}
	csvwriter := csv.NewWriter(file)
	csvwriter.Write([]string{"Points", "Threads", "Pi", "Time"})

	total_time := 0.0
	total_points := 0
	for _, nodes := range nodes {
		for _, points := range points {
			total, time := monteCarloPi_run(nodes, points)
			total_time += time.Seconds()
			total_points += points
			println(fmt.Sprintf("Go process with %d points and %d threads has finished in %0.8f seconds and a Pi estimation of %0.8f", points, nodes, time.Seconds(), 4*float64(total)/float64(points)))
			if time.Seconds() == 0 {
				csvwriter.Write([]string{fmt.Sprintf("%d", points), fmt.Sprintf("%d", nodes), fmt.Sprintf("%0.8f", 4*float64(total)/float64(points)), fmt.Sprintf("0.00000000%0.8d", time.Nanoseconds())})
			} else {
				csvwriter.Write([]string{fmt.Sprintf("%d", points), fmt.Sprintf("%d", nodes), fmt.Sprintf("%0.8f", 4*float64(total)/float64(points)), fmt.Sprintf("%0.8f", time.Seconds())})
			}
			csvwriter.Flush()
		}
	}
	println(fmt.Sprintf("Total time: %0.8f seconds for a total of %d points", total_time, total_points))
}
