"""
Xiaotong Wang

question 2
"""
import re
import pandas as pd

input_file_path = 'example_invoice.txt'
output_path = 'cleaned_invoice.txt'
processed_data = []
# Regular expression pattern to extract data
pattern = r'(\d+)([A-Za-z]+)\s*([A-Za-z]+)(GS|GO|GP)(\d{4})([A-Z]{4})(SHIRT WORK LS|SHIRT WORK SS|COVERALL GAS CO COTTON|PANT WORK TWILL).*Rent(\d+\.\d{2})'

with (open(input_file_path, 'r')) as input_file:
    for lines in input_file:
        line = lines.strip().split('\n')
        for n in line:
            match = re.search(pattern, n)
            if match:
                # Extract data using the matched groups
                wearer_number = match.group(1)
                wearer_first = match.group(2)
                wearer_last = match.group(3)
                item_code = match.group(4) + match.group(5)  # GS|GO|GP + four digits
                item_description = match.group(7)  # Description of the item
                cost = match.group(8)  # Total cost

                processed_data.append({
                    'wearer_number': wearer_number,
                    'wearer_first': wearer_first,
                    'wearer_last': wearer_last,
                    'item_code': item_code,
                    'item_description': item_description,
                    'cost': cost
                })

        df = pd.DataFrame(processed_data)
        # Save the DataFrame to a CSV file
        df.to_csv(output_path, index=False)


