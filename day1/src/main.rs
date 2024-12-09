fn main() {
    let start = std::time::Instant::now();
    let input = std::fs::read_to_string("input").unwrap();
    let mut l1 = Vec::<i32>::with_capacity(1000);
    let mut l2 = Vec::<i32>::with_capacity(1000);
    for line in input.lines().collect::<Vec<&str>>() {
        let v = line
            .split("   ")
            .map(|x| x.parse::<i32>().unwrap())
            .collect::<Vec<i32>>();
        l1.push(v[0]);
        l2.push(v[1]);
    }

    l1.sort();
    l2.sort();

    let pairs = l1.iter().zip(l2.iter());

    let mut total_distance = 0;
    for (a, b) in pairs {
        total_distance += i32::abs(a - b);
    }
    println!("Total distance: {}", total_distance);
    let duration = start.elapsed();
    println!("Time elapsed: {:?}", duration);
}
