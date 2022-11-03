from word_breaker import break_into_words_and_generate_tokens
from file_functions import read_file, write_to_file
from helper_functions import generate_token
from SyntaxAnalyzer import SA

file_content = read_file('text_files/input.txt')

tokens = break_into_words_and_generate_tokens(file_content)
tokens.append(generate_token('$', -1))

print(SA.main(tokens))

write_to_file('text_files/output.js', tokens)
