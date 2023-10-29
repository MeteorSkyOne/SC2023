def count_and_replace_terrible(input_file, output_file):
    try:
        with open(input_file, 'r') as file_to_read:
            content = file_to_read.read()

        # Split the content into words and initialize variables
        words = content.split()
        word_count = 0

        # Replace "terrible" with "pathetic" or "marvellous" based on count
        for i in range(len(words)):
            if words[i].strip(".,?!") == "terrible":
                word_count += 1
                if word_count % 2 == 0:
                    words[i] = "pathetic"
                else:
                    words[i] = "marvellous"

        # Join the modified words back into text
        modified_content = ' '.join(words)

        # Write the modified content to result.txt
        with open(output_file, 'w') as result_file:
            result_file.write(modified_content)

        print(f'Total occurrences of "terrible": {word_count}')

    except FileNotFoundError:
        print(f"The file '{input_file}' was not found.")

if __name__ == "__main__":
    input_file = "file_to_read.txt"
    output_file = "result.txt"
    count_and_replace_terrible(input_file, output_file)
