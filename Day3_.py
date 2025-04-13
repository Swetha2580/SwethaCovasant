def flatten(lst):
   
    flattened_list = []
    for item in lst:
        if isinstance(item, list):
            flattened_list.extend(flatten(item)) 
        else:
            flattened_list.append(item)
    return flattened_list


input_list = [1, 2, 3, [1, 2, 3, [3, 4], 2]]
output_list = flatten(input_list)
print(f"Input: {input_list}")
print(f"Output: {output_list}")

def convert(x):
   
    converted_list = []
    for item in x:
        if isinstance(item, list):
            converted_list.append(convert(item)) 
        elif isinstance(item, str) and item.startswith('(') and item.endswith(')'):
            try:
               
                numbers_str = item[1:-1].split(',')
                converted_list.append([int(num.strip()) for num in numbers_str])
            except ValueError:
               
                converted_list.append(item)
        else:
            converted_list.append(item)
    return converted_list


input_data = [[['(0,1,2)', '(3,4,5)'], ['(5,6,7)', '(9,4,2)']]]
output_data = convert(input_data)
print(f"\nInput: {input_data}")
print(f"Output: {output_data}")