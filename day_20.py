import aoc_helper
from aoc_helper import (
    Grid,
    PrioQueue,
    SparseGrid,
    decode_text,
    extract_ints,
    extract_iranges,
    extract_ranges,
    extract_uints,
    frange,
    irange,
    iter,
    list,
    map,
    range,
    tail_call,
)

raw = aoc_helper.fetch(20, 2022)


def parse_raw(raw):
    return extract_ints(raw)


data = parse_raw(raw)

# @dataclasses.dataclass
# class Node:
#     data: int
#     next: "Node"
#     prev: "Node"

#     def __init__(self, data, prev=None, next=None):
#         self.data = data
#         self.prev = prev or self
#         self.next = next or (prev and prev.next) or self
#         self.prev.next = self
#         self.next.prev = self

#     def shift(self):
#         node = self.prev
#         self.prev.next = self.next
#         self.next.prev = self.prev
#         for _ in range(abs(self.data)):
#             if self.data < 0:
#                 node = node.prev
#             else:
#                 node = node.next
#         self.prev = node
#         self.next = node.next
#         self.prev.next = self.next.prev = self

#     def find(self, data: int):
#         if self.data == data:
#             return self
#         node = self.next
#         while node != self:
#             # print(f"Finding {data} in {node.data}")
#             if node.data == data:
#                 return node
#             node = node.next

#     def nth(self, n):
#         node = self
#         for _ in range(n):
#             node = node.next
#         return node

#     def to_list(self):
#         out = [self.data]
#         node = self.next
#         while node != self:
#             out.append(node.data)
#             node = node.next
#         return out


# def mix(data: list[int]):
#     nums = Node(data[0])
#     for num in data[1:]:
#         nums = Node(num, nums)

#     for to_move in data:
#         # print(to_move)
#         nums.find(to_move).shift()
#     return nums


# def part_one(data: list[int]):
#     nums = mix(data)
#     zero = nums.find(0)
#     return zero.nth(1000).data + zero.nth(2000).data + zero.nth(3000).data


def mix(data: list[int]):
    nums = data.enumerated()
    for i, to_move in data.enumerated():
        if len(nums) < 10:
            print(nums)
        place = nums.index((i, to_move))
        nums.pop(place)
        nums.insert((place + to_move) % len(nums), to_move)
    return nums


def part_one(data: list[int]):
    nums = mix(data)
    i_0 = nums.index(0)
    if len(nums) < 10:
        print(nums)
    return (
        nums[(1000 + i_0) % len(nums)]
        + nums[(2000 + i_0) % len(nums)]
        + nums[((3000 + i_0) % len(nums))]
    )


aoc_helper.lazy_test(day=20, year=2022, parse=parse_raw, solution=part_one)


def part_two(data: list[int]):
    nums = data.mapped(lambda i: i * 811589153).enumerated()
    for _ in range(10):
        for i, to_move in nums.sorted():
            if len(nums) < 10:
                print(nums)
            place = nums.index((i, to_move))
            nums.pop(place)
            nums.insert((place + to_move) % len(nums), (i, to_move))
    nums = nums.mapped(lambda i: i[1])
    i_0 = nums.index(0)
    return (
        nums[(1000 + i_0) % len(nums)]
        + nums[(2000 + i_0) % len(nums)]
        + nums[((3000 + i_0) % len(nums))]
    )


aoc_helper.lazy_test(day=20, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=20, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=20, year=2022, solution=part_two, data=data)
