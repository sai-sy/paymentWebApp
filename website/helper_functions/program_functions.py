def partition(array, start, end):
    pivot = array[start]
    low = start + 1
    high = end

    while True:
        # If the current value we're looking at is larger than the pivot
        # it's in the right place (right side of pivot) and we can move left,
        # to the next element.
        # We also need to make sure we haven't surpassed the low pointer, since that
        # indicates we have already moved all the elements to their correct side of the pivot
        while low <= high and array[high] >= pivot:
            high = high - 1

        # Opposite process of the one above
        while low <= high and array[low] <= pivot:
            low = low + 1

        # We either found a value for both high and low that is out of order
        # or low is higher than high, in which case we exit the loop
        if low <= high:
            array[low], array[high] = array[high], array[low]
            # The loop continues
        else:
            # We exit out of the loop
            break

    array[start], array[high] = array[high], array[start]

    return high

def quick_sort(array, start, end):
    if start >= end:
        return

    p = partition(array, start, end)
    quick_sort(array, start, p-1)
    quick_sort(array, p+1, end)

def custom_sort(arr):
    """
    This function takes an array as a parameter in (value, label)
    pairs and sorts them based on the label
    """
    quick_sort(arr, 0, len(arr), -1)
    return arr

def negtrunc(number):
    '''
    If number is less then 0, returns 0. Otherwise returns the number passed
    '''
    if number < 0:
        return 0
    else:
        return number

if __name__ == "__main__":
    array = [(1, 'sai - Saihaan Syed'), (8, 'ishmam - Ishmam Saidur'), (19, 'irfan - Hamza Irfan')]
    custom_sort(array)
    print(array)