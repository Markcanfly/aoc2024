fn consistent_with(list: &[i32], rules: &[(i32, i32)]) -> bool {
    for (index, element) in list.iter().enumerate() {
        for previous_element in list[0..index].iter() {
            let rule_mustnt_exist: (i32, i32) = (*element, *previous_element);
            if rules.contains(&rule_mustnt_exist) {
                return false;
            }
        }
    }
    return true;
}

fn main() {
    let start = std::time::Instant::now();

    let file_path = "data/input";

    let contents = std::fs::read_to_string(file_path).expect("should have input file at path");

    let parts: Vec<&str> = contents.split("\n\n").collect();

    let rules: Vec<(i32, i32)> = parts[0]
        .split("\n")
        .map(|s| s.split("|").collect::<Vec<&str>>())
        .filter_map(|inner| {
            if inner.len() == 2 {
                let first = inner[0].parse::<i32>().ok()?;
                let second = inner[1].parse::<i32>().ok()?;
                Some((first, second))
            } else {
                None
            }
        })
        .collect();

    let lists: Vec<Vec<i32>> = parts[1]
        .split("\n")
        .map(|s| s.split(",").collect::<Vec<&str>>())
        .filter_map(|inner| {
            let elements: Vec<i32> = inner
                .iter()
                .filter_map(|n_str| n_str.parse::<i32>().ok())
                .collect();
            if elements.len() > 0 {
                Some(elements)
            } else {
                None
            }
        })
        .collect();

    let mut middle_number_sum = 0;
    for list in lists {
        if consistent_with(&list, &rules) {
            middle_number_sum += list[list.len() / 2];
        }
    }
    println!("Middle number sum: {}", middle_number_sum);
    let duration = start.elapsed();
    println!("Time elapsed is: {:?}", duration);
}
