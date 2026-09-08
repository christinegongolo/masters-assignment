"""
Question 4: product_of_multiples(factor, limit)

Returns the product of all positive multiples of `factor` that are
strictly less than `limit`, using a for loop and range().

If there are no such multiples, returns 1 (the multiplicative identity)
so the function composes cleanly with further multiplication.
"""


def product_of_multiples(factor: int, limit: int) -> int:
    product = 1
    for n in range(factor, limit, factor):
        product *= n
    return product


if __name__ == "__main__":
    # multiples of 3 below 20: 3,6,9,12,15,18 -> product
    print(product_of_multiples(3, 20))
    print(product_of_multiples(5, 5))   # no multiples below limit -> 1
