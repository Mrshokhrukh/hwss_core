import json

# Open the original JSON file with specified encoding
with open('dump.json', 'r', encoding='latin-1') as f:
    data = f.read()

# Replace any non-UTF-8 characters with empty string
data = data.encode('utf-8', 'ignore').decode('utf-8')

# Write the processed data to a new JSON file
with open('dump_processed.json', 'w', encoding='utf-8') as f:
    f.write(data)
