def calculate_total_calories(elves_data):
    max_calories = 0

    for elf_data in elves_data:
        calories = list(map(int, elf_data.strip().split('\n')))
        total_calories = sum(calories)
        max_calories = max(max_calories, total_calories)

    return max_calories

if __name__ == "__main__":
    import sys

    # Read puzzle input from stdin
    input_text = sys.stdin.read()

    elves_data = input_text.strip().split('\n\n')
    result = calculate_total_calories(elves_data)

    print("Total Calories carried by the Elf with the most Calories:", result)
