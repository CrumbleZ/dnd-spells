from argparse import ArgumentParser
import fetcher


def main():
    #Define script options
    parser = ArgumentParser()
    parser.add_argument("-l", "--update-list", action="store_true",
                        help="Updates the list of known spells",)

    #Execute script options
    args = parser.parse_args()

    if args.update_list:
        fetcher.update_spell_list()
