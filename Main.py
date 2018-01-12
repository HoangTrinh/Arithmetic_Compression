import Arithmetic
import support_functions
import random

# Run 1 time
support_functions.read_save_textdata_from_pdf_folder('pdf_data', 'text_data')

# Read data from text
data = support_functions.read_text_data('text_data')

codeword_table = Arithmetic.create_dictionary()

compression_ratio_of_data = 0
i = 1

# list of files
for pdf_file in data:
    print('\nstart a new file:')
    compression_ratio_of_pdf_file = 0
    save_data = []

    lines = support_functions.split_string(pdf_file, random.randrange(16, 64))
    # list of lines
    for line in lines:

        print('original data: ', line)

        # compress + convenience purpose
        compressed_data, line_len, binary_code = Arithmetic.encode(line, codeword_table)
        print('compressed_data: ', binary_code)

        # decompress
        decompressed_data = Arithmetic.decode(compressed_data, line_len, codeword_table)

        # check result
        if line == decompressed_data:
            print('decompressed_data equal original_data, Good job!')
        else:
            exit(404, 'POOR Algorithm')

        print('decompressed_data: ', decompressed_data)

        # calculate compression ratio per page
        binary_code = binary_code[2:]
        binary_code = int(''.join(binary_code),2)

        compression_ratio = support_functions.calculate_compress_ratio(line, binary_code)

        print('compression_ratio: %0.2f' % compression_ratio)
        compression_ratio_of_pdf_file += compression_ratio

        save_data.append(binary_code)

    support_functions.save_text_file_into_folder('compressed_' + str(i) + '.txt', save_data, 'compressed_data')
    i += 1
    compression_ratio_of_pdf_file /= len(lines)

    print('average compression ratio for this file: ', compression_ratio_of_pdf_file)
    compression_ratio_of_data += compression_ratio_of_pdf_file

# average compression ratio for the whole data
compression_ratio_of_data /= len(data)
real_compression_ratio = support_functions.calculate_real_compress_ratio_from_file('text_data', 'compressed_data')
print('\naverage compression ratio: %0.2f' % compression_ratio_of_data)

with open('record.txt', 'w') as result:
    result.write('Theory: ' + str(compression_ratio) + ' Real: ' + str(real_compression_ratio))
