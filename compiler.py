"""
created by Amirhossein Bagheri - 98105621 -> ahbagheri01@gmail.com
       &   Mohammad Jafari     - 98105654 -> mamad.jafari91@gmail.com
"""
import Scanner
import Parser
read_path = "./input.txt"
save_path = "/"
#scanner = Scanner.Scanner(path)
parser = Parser.Parser(read_path,save_path)
parser.parse()

