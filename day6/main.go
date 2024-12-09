package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strings"
)

func main() {
	// filename := os.Args[1]

	input, err := ioutil.ReadFile("data/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	groups := strings.Split(string(input), "\n\n")

	fmt.Printf("Groups: %v\n", groups)

}
