from word_breaker import break_into_words_and_generate_tokens
from file_functions import read_file, write_to_file

file_content = read_file('text_files/input.txt')

token = break_into_words_and_generate_tokens(file_content)

write_to_file('text_files/output.txt', token)