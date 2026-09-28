numbers = [10, 5, 8, 20, 15]

largest = numbers[0]
sec_largest = numbers[0]

for num in numbers:
    if num > largest:
        sec_largest = largest
        largest = num

    elif num > sec_largest:
        sec_largest = num

print(sec_largest)