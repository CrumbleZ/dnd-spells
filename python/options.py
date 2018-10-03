import fetcher
from argparse import ArgumentParser
from sys import exit as sysexit


def main():
    #Define script options
    parser = ArgumentParser()
    parser.add_argument("-l", "--update-list", action="store_true",
                        help="Updates the list of known spells")
    parser.add_argument("-d", "--download", action="store_true",
                        help="Updates the spell cache, without overwriting existing files.")
    parser.add_argument("-D", "--download-overwrite", action="store_true",
                        help="Updates the spell cache and overwrites existing files.")

    args = parser.parse_args()

    #Handle options conflict
    if args.download_overwrite and args.download:
        print("You can't specify both caching options")
        sysexit(0)

    #Execute script options
    if args.update_list:
        fetcher.update_spell_list()

    if args.download:
        fetcher.get_all_spells(overwrite_existing=False)

    if args.download_overwrite:
        fetcher.get_all_spells(overwrite_existing=True)
