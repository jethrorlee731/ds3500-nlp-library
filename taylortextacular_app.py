from nlp import Nlp
import pprint as pp
import nlp_parsers as np


def main():
    # initialize framework
    tt = Nlp()

    # register some text files
    tt.load_text('TaylorSwiftOurSong.txt', 'OurSong')
    tt.load_text('TaylorSwiftFearless.txt', 'Fearless')
    tt.load_text('TaylorSwiftDearJohn.txt', 'DearJohn')
    tt.load_text('TaylorSwiftRed.txt', 'Red')

    # produce some visualizations
    # pp.pprint(tt.data)
    # tt.compare_num_words()


if __name__ == '__main__':
    main()
