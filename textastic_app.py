from textastic import Textastic
import pprint as pp
import textastic_parsers as tp


def main():
    # initialize framework
    tt = Textastic()

    # register some text files
    tt.load_text('file1.txt', 'A')
    tt.load_text('file2.txt', 'B')
    tt.load_text('file3.txt', 'C')
    tt.load_text('myfile.json', 'J', parser=tp.json_parser)

    # produce some visualizations
    pp.pprint(tt.data)
    tt.compare_num_words()


if __name__ == '__main__':
    main()
