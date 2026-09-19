"""
Question 3 (20 marks)
Describe the purpose and syntax of list comprehensions. Write a list
comprehension to generate a list of all odd numbers between 1 and 50
that are divisible by 3.

--------------------------------------------------------------------------
Purpose and syntax
--------------------------------------------------------------------------
A list comprehension is a concise way to build a new list by applying an
expression to every item in an iterable, optionally filtering items with
a condition. It replaces the more verbose pattern of creating an empty
list and appending to it inside a for loop, while being more readable
and generally faster.

General syntax:

    new_list = [expression for item in iterable if condition]

  - expression : what to put in the new list for each item (can transform
    the item)
  - item       : the loop variable, one value from the iterable per pass
  - iterable   : the sequence/range being looped over
  - condition  : optional filter; item is only included if this is True
"""

# List comprehension: odd numbers between 1 and 50 that are divisible by 3
odd_divisible_by_3 = [n for n in range(1, 51) if n % 2 != 0 and n % 3 == 0]


# Equivalent using a plain for loop, for comparison:
def equivalent_with_loop():
    result = []
    for n in range(1, 51):
        if n % 2 != 0 and n % 3 == 0:
            result.append(n)
    return result


if __name__ == "__main__":
    print("List comprehension result:", odd_divisible_by_3)
    print("Loop-based result:        ", equivalent_with_loop())
    assert odd_divisible_by_3 == equivalent_with_loop()
