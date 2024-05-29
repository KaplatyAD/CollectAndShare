import asyncio
import requests
import socket

import copy

old_list = [*range(10)]
new_list = old_list
new_list.append(1)
print(old_list)


class Cat:
    def __init__(self, breed, name):
        self.breed = breed
        self.name = name


class Kitten(Cat):
    def __init__(self, breed, name, age):
        super().__init__(breed, name)
        self.age = age

    def __call__(self, *args, **kwargs):
        print(args, kwargs)


import time

c = Kitten(breed='Kitten', name='Kitten', age=10)


class StringByLetter:
    def __init__(self, letter):
        self.letter = letter
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.letter):
            self.index += 1
            return self.letter[self.index]
        else:
            raise StopIteration


def palindrome(lst: list) -> bool:
    middle = len(lst) // 2
    for i in range(middle):
        if lst[i] != lst[-i - 1]:
            return False
    return True


print(palindrome([1, 2, 3, 2, 1]))
lst = [*range(20)]


def binary_search(lst: list, target: int) -> bool:
    start = 0
    end = len(lst) - 1
    while start <= end:
        middle = (start + end) // 2
        if lst[middle] == target:
            return True
        elif lst[middle] < target:
            start = middle + 1
        else:
            end = middle - 1
    return False


lst_with_zeroes = [1, 3, 5, 0, 6, 0, 0, 10, 11]


def zeros_to_end(lst: list) -> list:
    zero_index = 0
    for index, value in enumerate(lst):
        if lst[index] != 0:
            lst[index] = value
            if index != zero_index:
                lst[index], lst[zero_index] = lst[zero_index], lst[index]
            zero_index += 1
    return lst


print(zeros_to_end(lst_with_zeroes))


def generator():
    for i in range(10):
        yield i


res = generator()

print(next(res))
print(next(res))
import unittest


class Singletone:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            Singletone.instance = super().__new__(cls)

        return Singletone.instance


tmp1 = Singletone()
tmp2 = Singletone()

print(tmp1 is tmp2)


def decorator(func):
    def wrapper(*args, **kwargs):
        if wrapper.counter < 3:
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time() - start
            print(f'функция выполнена за {end}')
            wrapper.counter += 1
            return res
        else:
            raise Exception('Количество вызовов превышено')
    wrapper.counter = 0
    print(wrapper.__dict__)
    return wrapper




import functools

@decorator
def add(a, b):
    return a + b

add(2, 2)
add(2, 2)
add(2, 2)
add(2, 2)
add(2, 2)
