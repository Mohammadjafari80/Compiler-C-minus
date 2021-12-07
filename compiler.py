"""
created by Amirhossein Bagheri - 98105621 -> ahbagheri01@gmail.com
       &   Mohammad Jafari     - 98105654 -> mamad.jafari91@gmail.com
"""
import Scanner
import Parser


for i in range(220):
    read_path = "./tests/PA1_extra_samples/T%03d" % (i+1)
    save_path = "./tests/PA1_extra_samples/T%03d" % (i+1)
    scanner = Scanner.Scanner(path=save_path, save_path=save_path)
    parser = Parser.Parser(read_path, save_path)
    parser.parse()

