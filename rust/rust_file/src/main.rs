use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut n = 0;
    if let Ok(lines) = read_lines("/home/cheny/personal_prj/rust_file/eve.json") {
        lines.for_each(|line| {
            if let Ok(_line) = line {
                // println!("{}", line);
                n += 1;
            }
        });
    }
    println!("n is {}", n);
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

