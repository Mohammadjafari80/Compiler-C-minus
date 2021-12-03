"""
created by Amirhossein Bagheri - 98105621   &   Mohammad Jafari - 98105654
"""
import Scanner

path = "./input.txt"
scanner = Scanner.Scanner(path)
token = "start"
while (token != "$"):
    token = scanner.get_next_token()
    print(token)

