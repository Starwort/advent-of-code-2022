#![feature(iter_array_chunks)]

use std::env::args;
use std::hint::black_box;
use std::time::Instant;

use lazy_static::lazy_static;
use rayon::prelude::{IntoParallelRefIterator, ParallelIterator};
use regex::Regex;

const INPUT: &str =
    include_str!(concat!(env!("HOME"), "/.config/aoc_helper/2022/19.in"));

#[derive(Debug, Clone, Copy)]
struct State {
    geodes: u32,
    obsidian: u32,
    clay: u32,
    ore: u32,
    ore_robot: u32,
    clay_robot: u32,
    obsidian_robot: u32,
    time_left: u32,
}
impl State {
    fn wait(&mut self) {
        self.ore += self.ore_robot;
        self.clay += self.clay_robot;
        self.obsidian += self.obsidian_robot;
        self.time_left -= 1;
    }

    #[inline]
    fn may_buy_ore(&self, blueprint: &([u32; 7], u32)) -> bool {
        self.ore_robot < blueprint.1
    }

    #[inline]
    fn can_buy_ore(&self, blueprint: &([u32; 7], u32)) -> bool {
        let [_, ore_cost, _, _, _, _, _] = blueprint.0;
        self.ore >= ore_cost
    }

    fn buy_ore(mut self, blueprint: &([u32; 7], u32)) -> Option<Self> {
        if !self.may_buy_ore(blueprint) {
            return None;
        }
        let &([_, ore_cost, _, _, _, _, _], _) = blueprint;
        while !self.can_buy_ore(blueprint) {
            self.wait();
            if self.time_left == 0 {
                return None;
            }
        }
        self.wait();
        self.ore -= ore_cost;
        self.ore_robot += 1;
        Some(self)
    }

    #[inline]
    fn may_buy_clay(&self, blueprint: &([u32; 7], u32)) -> bool {
        let [_, _, _, _, obsidian_cost_clay, _, _] = blueprint.0;
        self.clay_robot < obsidian_cost_clay
    }

    #[inline]
    fn can_buy_clay(&self, blueprint: &([u32; 7], u32)) -> bool {
        let [_, _, clay_cost, _, _, _, _] = blueprint.0;
        self.ore >= clay_cost
    }

    fn buy_clay(mut self, blueprint: &([u32; 7], u32)) -> Option<Self> {
        if !self.may_buy_clay(blueprint) {
            return None;
        }
        let &([_, _, clay_cost, _, _, _, _], _) = blueprint;
        while !self.can_buy_clay(blueprint) {
            self.wait();
            if self.time_left == 0 {
                return None;
            }
        }
        self.wait();
        self.ore -= clay_cost;
        self.clay_robot += 1;
        Some(self)
    }

    #[inline]
    fn may_buy_obsidian(&self, blueprint: &([u32; 7], u32)) -> bool {
        let [_, _, _, _, _, _, geode_cost_obsidian] = blueprint.0;
        self.obsidian_robot < geode_cost_obsidian
    }

    #[inline]
    fn can_buy_obsidian(&self, blueprint: &([u32; 7], u32)) -> bool {
        let [_, _, _, obsidian_cost_ore, obsidian_cost_clay, _, _] = blueprint.0;
        self.ore >= obsidian_cost_ore && self.clay >= obsidian_cost_clay
    }

    fn buy_obsidian(mut self, blueprint: &([u32; 7], u32)) -> Option<Self> {
        if !self.may_buy_obsidian(blueprint) {
            return None;
        }
        let [_, _, _, obsidian_cost_ore, obsidian_cost_clay, _, _] = blueprint.0;
        while !self.can_buy_obsidian(blueprint) {
            self.wait();
            if self.time_left == 0 {
                return None;
            }
        }
        self.wait();
        self.ore -= obsidian_cost_ore;
        self.clay -= obsidian_cost_clay;
        self.obsidian_robot += 1;
        Some(self)
    }

    #[inline]
    fn can_buy_geode(&self, blueprint: &([u32; 7], u32)) -> bool {
        let [_, _, _, _, _, geode_cost_ore, geode_cost_obsidian] = blueprint.0;
        self.ore >= geode_cost_ore && self.obsidian >= geode_cost_obsidian
    }

    fn buy_geode(mut self, blueprint: &([u32; 7], u32)) -> Option<Self> {
        let [_, _, _, _, _, geode_cost_ore, geode_cost_obsidian] = blueprint.0;
        while !self.can_buy_geode(blueprint) {
            self.wait();
            if self.time_left == 0 {
                return None;
            }
        }
        self.wait();
        self.ore -= geode_cost_ore;
        self.obsidian -= geode_cost_obsidian;
        self.geodes += self.time_left;
        Some(self)
    }

    fn best_possible_score(&self) -> u32 {
        self.geodes + (0..self.time_left).sum::<u32>()
    }
}

fn dfs(blueprint: &([u32; 7], u32), state: State, best_geodes: &mut u32) {
    if state.time_left == 0 || state.best_possible_score() <= *best_geodes {
        return;
    }
    if let Some(next) = state.buy_geode(blueprint) {
        // println!("{next:?}");
        *best_geodes = (*best_geodes).max(next.geodes);
        dfs(blueprint, next, best_geodes);
    }
    if let Some(next) = state.buy_obsidian(blueprint) {
        dfs(blueprint, next, best_geodes);
    }
    if let Some(next) = state.buy_clay(blueprint) {
        dfs(blueprint, next, best_geodes);
    }
    if let Some(next) = state.buy_ore(blueprint) {
        dfs(blueprint, next, best_geodes);
    }
}

fn find_count_for(blueprint: &([u32; 7], u32), steps: u32) -> u32 {
    let mut best_geodes = 0;
    dfs(
        blueprint,
        State {
            ore: 0,
            clay: 0,
            obsidian: 0,
            geodes: 0,
            ore_robot: 1,
            clay_robot: 0,
            obsidian_robot: 0,
            time_left: steps,
        },
        &mut best_geodes,
    );
    best_geodes
}

fn parse_input(input: &str) -> Vec<([u32; 7], u32)> {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"(\d+)").unwrap();
    }
    RE.find_iter(input)
        .map(|m| m.as_str().parse::<u32>().unwrap())
        .array_chunks::<7>()
        .map(|data| (data, data[2].max(data[3]).max(data[5])))
        .collect()
}

fn main() {
    let start = Instant::now();
    let blueprints = parse_input(INPUT);
    let elapsed_input = start.elapsed();
    let ans1 = blueprints
        .par_iter()
        .map(|blueprint| find_count_for(blueprint, 24) * blueprint.0[0])
        .sum::<u32>();
    let elapsed_p1 = start.elapsed();
    let ans2 = blueprints[..3]
        .par_iter()
        .map(|blueprint| find_count_for(blueprint, 32))
        .product::<u32>();
    let elapsed_p2 = start.elapsed();
    println!(
        "[{:.3}ms] Parsed input",
        elapsed_input.as_micros() as f64 / 1000.0
    );
    println!(
        "[{:.3}ms] Part one: {ans1}",
        elapsed_p1.as_micros() as f64 / 1000.0
    );
    println!(
        "[{:.3}ms] Part two: {ans2}",
        elapsed_p2.as_micros() as f64 / 1000.0
    );
    if args().any(|arg| arg == "--bench") {
        const PARSE_RUNS: usize = 500_000;
        println!("---- BENCH ----");
        let start = Instant::now();
        for _ in 0..PARSE_RUNS {
            black_box(parse_input(black_box(INPUT)));
        }
        println!(
            "[Parse] {PARSE_RUNS} runs, avg. {:.3}ms",
            start.elapsed().as_micros() as f64 / 1000.0 / (PARSE_RUNS as f64)
        );
        const P1_RUNS: usize = 10_000;
        let start = Instant::now();
        for _ in 0..P1_RUNS {
            black_box(
                black_box(&blueprints)
                    .par_iter()
                    .map(|blueprint| find_count_for(blueprint, 24) * blueprint.0[0])
                    .sum::<u32>(),
            );
        }
        println!(
            "[Part one, rayon] {P1_RUNS} runs, avg. {:.3}ms",
            start.elapsed().as_micros() as f64 / 1000.0 / (P1_RUNS as f64)
        );
        let start = Instant::now();
        for _ in 0..P1_RUNS {
            black_box(
                black_box(&blueprints)
                    .iter()
                    .map(|blueprint| find_count_for(blueprint, 24) * blueprint.0[0])
                    .sum::<u32>(),
            );
        }
        println!(
            "[Part one, no rayon] {P1_RUNS} runs, avg. {:.3}ms",
            start.elapsed().as_micros() as f64 / 1000.0 / (P1_RUNS as f64)
        );
        const P2_RUNS: usize = 1_000;
        let start = Instant::now();
        for _ in 0..P2_RUNS {
            black_box(
                black_box(&blueprints[..3])
                    .par_iter()
                    .map(|blueprint| find_count_for(blueprint, 32))
                    .product::<u32>(),
            );
        }
        println!(
            "[Part two, rayon] {P2_RUNS} runs, avg. {:.3}ms",
            start.elapsed().as_micros() as f64 / 1000.0 / (P2_RUNS as f64)
        );
        let start = Instant::now();
        for _ in 0..P2_RUNS {
            black_box(
                black_box(&blueprints[..3])
                    .iter()
                    .map(|blueprint| find_count_for(blueprint, 32))
                    .product::<u32>(),
            );
        }
        println!(
            "[Part two, no rayon] {P2_RUNS} runs, avg. {:.3}ms",
            start.elapsed().as_micros() as f64 / 1000.0 / (P2_RUNS as f64)
        );
    }
}
