# https://chat.deepseek.com/a/chat/s/6dafc3d1-b7f9-4555-9ca2-49559b28dec8

def fractional_knapsack(capacity, weights, values):
    # Calculate value-to-weight ratio for each item and store with weight and value
    n = len(weights)
    items = [(values[i] / weights[i], weights[i], values[i]) for i in range(n)]
    # Sort items by ratio in descending order
    items.sort(reverse=True)

    # Initialize total value accumulated in the knapsack to 0
    total_value = 0.0
    for ratio, weight, value in items:
        if capacity == 0:
            break
        # Take as much as possible from the current item
        take = min(weight, capacity)
        total_value += take * ratio
        capacity -= take
    return total_value

# Example usage:
if __name__ == "__main__":
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    max_value = fractional_knapsack(capacity, weights, values)
    print(f"Maximum value in knapsack: {max_value}")

"""
Potential Solution Explanation:
- Calculate the value-to-weight ratio for each item.
- Sort all items in descending order of this ratio.
- Iterate through the sorted items:
    - Take as much as possible from the item (either the whole item or the remaining capacity).
    - Add the value of the taken amount to the total value.
    - Reduce the remaining capacity accordingly.
- Stop when the knapsack is full or all items are considered.
- Return the total value accumulated, which is the maximum value for the given capacity.
"""