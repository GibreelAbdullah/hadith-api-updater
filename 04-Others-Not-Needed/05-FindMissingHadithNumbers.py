def find_missing_numbers(filename):
    missing_numbers = []
    current_number = 1

    with open(filename, 'r') as file:
        for line in file:
            try:
                line_number = int(line.split()[0])
                while current_number < line_number:
                    missing_numbers.append(current_number)
                    current_number += 1
                current_number += 1
            except:
                'print()'

    return missing_numbers

filename = '/home/alfi/Projects/hadith-api/database/linebyline/ara-tirmidhi.txt'
missing_numbers = find_missing_numbers(filename)
print("Missing numbers:", missing_numbers)