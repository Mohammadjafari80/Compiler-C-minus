"""
created by Amirhossein Bagheri - 98105621 -> ahbagheri01@gmail.com
       &   Mohammad Jafari     - 98105654 -> mamad.jafari91@gmail.com
"""
import Scanner

path = "./input.txt"
scanner = Scanner.Scanner(path)
token = "start"
while (token != "$"):
    token = scanner.get_next_token()
    print(token)

