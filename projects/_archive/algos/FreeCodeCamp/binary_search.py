def binary_search(list , target):
    first = 0
    last = len(list) - 1

    while first <= last:
        midpoint = (first + last) // 2
        if list[midpoint] == target:
            return midpoint
        elif list[midpoint] < target:
            first = midpoint
        elif list[midpoint] > target:
            last = midpoint
        print(f"searching at midpoint index: {midpoint} | Value: {list[midpoint]}...")

    return None






numbers = [x for x in range(0,100,5)]
target = 15
search_index = binary_search(numbers , 15 )
print(numbers)
print(search_index)