# The correct paths for the uploaded files
file1_path = r"auth\db\models.py"
file2_path = r"general_settings\db\models.py"

# Since they both have the same name, I will open them individually.
with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
    file1_content = file1.read()
    file2_content = file2.read()

import difflib

# Create a differ object and get the diff between the two files
differ = difflib.Differ()
diff = list(differ.compare(file1_content.splitlines(), file2_content.splitlines()))

# Filter the diff output to show only the lines with differences
diff = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]

import pprint
pprint.pprint(diff)
