import csv
from sys import argv, exit

#Check for the max number of STR repeated
def STR_repeat(s, sub):
    ans = [0] * len(s)
    for i in range(len(s) - len(sub), -1, -1):
        if s[i: i + len(sub)] == sub:
            if i + len(sub) > len(s) - 1:
                ans[i] = 1
            else:
                ans[i] = 1 + ans[i + len(sub)]
    return max(ans)

#Matches the csv file with the dna sequences analyzed
def print_match(reader, dna_dtb):
    for line in reader:
        person = line[0]
        values = [int(val) for val in line[1:]]
        if values == dna_dtb:
            print(person)
            return
    print("No match")

#Open the files and check if the command line argument is correct
def main():
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    with open(argv[1]) as csv_file:
        reader = csv.reader(csv_file)
        all_sequences = next(reader)[1:]

        with open(argv[2]) as txt_file:
            s = txt_file.read()
            dna_dtb = [STR_repeat(s, seq) for seq in all_sequences]

        print_match(reader, dna_dtb)

#Calls main
if __name__ == "__main__":
    main()


