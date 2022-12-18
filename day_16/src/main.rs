use std::ops::{Index, IndexMut};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Instant;

use array_macro::array;
use rayon::prelude::{IntoParallelIterator, ParallelIterator};
use text_io::scan;

fn parse_input() -> (Vec<(usize, Vec<usize>)>, usize) {
    fn parse_line(line: &str) -> (String, usize, Vec<String>) {
        let (name, rate, connections): (String, usize, String);
        let line = line
            .replace("tunnels", "tunnel")
            .replace("leads", "lead")
            .replace("valves", "valve");
        scan!(
            line.bytes() => "Valve {} has flow rate={}; tunnel lead to valve {}\n",
            name,
            rate,
            connections
        );
        let connections = connections.split(", ").map(str::to_owned).collect();
        (name, rate, connections)
    }
    let input = std::fs::read_to_string(concat!(
        env!("HOME"),
        "/.config/aoc_helper/2022/16.in"
    ))
    .expect(concat!(
        env!("HOME"),
        "/.config/aoc_helper/2022/16.in missing"
    ));
    let mut data = input.lines().map(parse_line).collect::<Vec<_>>();
    data.sort_by_key(|(_, rate, _)| *rate == 0);
    (
        data.iter()
            .map(|(_, rate, connections)| {
                (
                    *rate,
                    connections
                        .iter()
                        .map(|i| {
                            data.iter()
                                .enumerate()
                                .find(|(_, (name, _, _))| name == i)
                                .expect("Malformed input")
                                .0
                        })
                        .collect(),
                )
            })
            .collect(),
        data.iter()
            .enumerate()
            .find(|(_, (name, _, _))| name == "AA")
            .unwrap()
            .0,
    )
}

fn pathfind(a: usize, b: usize, data: &[(usize, Vec<usize>)]) -> usize {
    // BFS
    let mut queue = std::collections::VecDeque::from([(a, 0)]);
    let mut visited = std::collections::HashSet::new();
    while let Some((node, cost)) = queue.pop_front() {
        if node == b {
            return cost;
        }
        for &next in &data[node].1 {
            if !visited.contains(&next) {
                visited.insert(next);
                queue.push_back((next, cost + 1));
            }
        }
    }
    unreachable!()
}

#[derive(Clone)]
struct Grid<T> {
    data: Vec<T>,
    width: usize,
}
impl<T> Grid<T> {
    fn new(width: usize, height: usize, default: T) -> Self
    where
        T: Copy,
    {
        Self {
            data: vec![default; width * height],
            width,
        }
    }

    fn new_factory(
        width: usize,
        height: usize,
        factory: impl Fn(usize, usize) -> T,
    ) -> Self {
        Self {
            data: (0..width * height)
                .map(|i| factory(i % width, i / width))
                .collect(),
            width,
        }
    }

    fn flat(&self) -> &[T] {
        &self.data
    }

    fn width(&self) -> usize {
        self.width
    }
}
impl<T> Index<(usize, usize)> for Grid<T> {
    type Output = T;

    fn index(&self, (x, y): (usize, usize)) -> &Self::Output {
        &self.data[y * self.width + x]
    }
}
impl<T> IndexMut<(usize, usize)> for Grid<T> {
    fn index_mut(&mut self, (x, y): (usize, usize)) -> &mut Self::Output {
        &mut self.data[y * self.width + x]
    }
}

fn part_one(
    data: &[(usize, Vec<usize>)],
    start: usize,
) -> ([Grid<Option<usize>>; 31], usize) {
    let n_nonzero = data.iter().filter(|(rate, _)| *rate != 0).count();
    let mut pairwise_distances = Grid::new(n_nonzero, data.len(), 0);
    for from in 0..data.len() {
        for to in 0..n_nonzero {
            pairwise_distances[(from, to)] = pathfind(from, to, data);
        }
    }
    let pairwise_distances = pairwise_distances;
    let mut dp_table = array![Grid::new(n_nonzero, 1<<n_nonzero, None); 31];
    for (i, (rate, _)) in data.iter().enumerate() {
        if *rate != 0 {
            dp_table[pairwise_distances[(start, i)] + 1][(i, 1 << i)] = Some(*rate);
        }
    }
    let mut flow = Vec::<usize>::with_capacity(1 << n_nonzero);
    for x in 0..(1 << n_nonzero) {
        flow.push(
            (0..n_nonzero)
                .filter(|i| x & (1 << i) != 0)
                .map(|i| data[i].0)
                .sum(),
        );
    }
    let flow = flow;
    let mut answer = 0;
    for i in 1..31 {
        for j in 0..n_nonzero {
            for (k, flow) in flow.iter().enumerate() {
                if let Some(prev) = dp_table[i - 1][(j, k)] {
                    let if_stay = prev + flow;
                    #[allow(clippy::match_on_vec_items)]
                    match dp_table[i][(j, k)] {
                        Some(x) if x > if_stay => (),
                        _ => {
                            dp_table[i][(j, k)] = Some(if_stay);
                            answer = answer.max(if_stay);
                        },
                    }
                }
                if k & (1 << j) == 0 {
                    continue;
                }
                if let Some(current) = dp_table[i][(j, k)] {
                    for l in (0..n_nonzero).filter(|l| k & (1 << l) == 0) {
                        let next = k | (1 << l);
                        let dist = pairwise_distances[(j, l)];
                        if i + dist > 29 {
                            continue;
                        }
                        let if_go = current + flow * (dist + 1);
                        #[allow(clippy::match_on_vec_items)]
                        match dp_table[i][(l, next)] {
                            Some(x) if x > if_go => (),
                            _ => {
                                dp_table[i][(l, next)] = Some(if_go);
                                answer = answer.max(if_go);
                            },
                        }
                    }
                }
            }
        }
    }
    (dp_table, answer)
}

fn part_two(dp_table: &[Grid<Option<usize>>; 31]) -> usize {
    let n_nonzero = dp_table[0].width();
    let answer = AtomicUsize::new(0);
    (0..(1 << n_nonzero)).into_par_iter().for_each(|i| {
        let mut j = 0;
        while {
            // increase j to the next value that doesn't intersect with i
            // technically this is making an assumption that the elephant
            // shouldn't do nothing but that seems like a reasonable
            // assumption to make
            j += 1;
            while j & i != 0 {
                j += j & i;
            }
            j < (1 << n_nonzero)
        } {
            let entry = &dp_table[26];
            let Some(a) = (0..n_nonzero).filter_map(|k|entry[(k, i)]).max() else {
                continue;
            };
            let Some(b) = (0..n_nonzero).filter_map(|k|entry[(k, j)]).max() else {
                continue;
            };
            answer.fetch_max(a + b, Ordering::Relaxed);
        }
    });
    answer.into_inner()
}

fn main() {
    let start = Instant::now();
    let input = parse_input();
    println!("[{}µs] Parsed input", start.elapsed().as_micros());
    let (dp_table, ans_one) = part_one(&input.0, input.1);
    println!("[{}ms] Part one: {}", start.elapsed().as_millis(), ans_one);
    let ans_two = part_two(&dp_table);
    println!("[{}ms] Part two: {}", start.elapsed().as_millis(), ans_two);
}
