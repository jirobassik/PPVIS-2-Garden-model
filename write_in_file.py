import sys
def write_in_file(string):
    with open('history.txt', 'a') as f:
        original_stdout = sys.stdout
        sys.stdout = f
        print(string)
        sys.stdout = original_stdout
