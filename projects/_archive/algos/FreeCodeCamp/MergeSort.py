def MergeSort(arr):
    # Divide : Find midpoint of list, split list into sublists
    # Conquer: Recursivly sort the sublists 
    # Combine: Merge sorted sublists 
    
    if len(arr) <= 1: return arr

    # DIVIDE
    midpoint = len(arr) // 2
    left_half = arr[:midpoint]
    right_half = arr[midpoint:]

    # CONQUER
    left = MergeSort(left_half)
    right = MergeSort(right_half)


    # COMBINE
    l = []
    i = 0
    j = 0
    while i < len(left) and j < len(right): #sorting loop
        if left[i] < right[j]:
            l.append(left[i])
            i += 1
        else:
            l.append(right[j])
            j += 1

    while i < len(left): # uneven lists:  [0,0] vs [0]
        l.append(left[i])
        i += 1
    while j < len(right): 
        l.append(right[j])
        j += 1
    return l





# calling functions down here
import random

arr = [random.randint(0,100) for x in range(10)]
sorted_arr = MergeSort(arr)

print("unsorted:", arr)
print("sorted:", sorted_arr)