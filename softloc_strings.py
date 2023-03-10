#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import io
import logging
from xml.dom.minidom import parseString
# import pandas as pd
# from pprint import pprint
#
# from collections import OrderedDict
# from romagnolo.lexicon.dit_frog import DitFrog, tsv_to_dataframe
# from romagnolo.text import generic

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

logger = logging.getLogger()


def display_strings(args):
    # input = [x for x in args]
    # print(args[0]["PermissionReadBookmarksLabel"], args[1]["PermissionReadBookmarksLabel"])
    for key in args[0].keys():
        out = [key]
        for i in range(len(args)):
            if key in args[i]:
                out.append(args[i][key])
            else:
                out.append("--")
        print("\t".join(out))

    return None

# TODO I JUST PASTED METHODS WITH 02_XML_EXTRACTOR.PY
# I SHOULD MAKE A CLASS AND START RE-USING SOME CODE

def _team_from_path(path):
    rteam = path.find("team_") + 5
    return path[rteam:rteam+2]

def get_diff_strings(strings, files):
    for i in range(len(strings) -1):
        strings_a = strings[i]
        for j in range(i+1, len(strings)):
            strings_b = strings[j]
            equal = 0
            different = 0
            for key in strings_a.keys():
                if strings_a[key] == strings_b[key]:
                    equal +=1
                else:
                    different += 1
                    # print("\t".join([key, strings_a[key], strings_b[key]]))
            logger.info("%s vs %s", _team_from_path(files[i]), _team_from_path(files[j]))
            logger.info("%d out of %d instances are identical", equal, len(strings_a))
            logger.info("%d out of %d instances are different", different, len(strings_a))
    return None


def get_equal_strings(strings_a, strings_b):
    equal = 0
    different = 0
    for key in strings_a.keys():
        if strings_a[key] == strings_b[key]:
            equal +=1
            print("\t".join([key, strings_a[key], strings_b[key]]))
        else:
            different += 1

    logger.info("%d out of %d instances are identical", equal, len(strings_a))
    logger.info("%d out of %d instances are different", different, len(strings_a))
    return None


def get_strings(xml_files):
    all_entries = []
    for xml_file in xml_files:
        entries = {}
        f = open(xml_file, 'r').read()
        dom = parseString(f)
        strings = dom.getElementsByTagName('string')
        for string in strings:
            try:
                text = string.firstChild.nodeValue.strip()
            except:
                text = ""

            if text is None :
                text = string.firstChild.firstChild.nodeValue
            text = text.replace("\n", " ")
            # print(string.getAttribute('name'), text)

            entries[string.getAttribute('name')] = text
            # print(string.getAttribute('name'), "\t\t", text)
        all_entries.append(entries)
        logger.info("Extracted %d entries from %s", len(entries), xml_file)

    # AQUI VOY. FALTAN LOS OTROS TIPOS DE STRINGS
    return all_entries


def main(param):
    files = param['input']
    # print(files)
    # file_b = param['jnput']
    extract = param['extract']
    diff = param['diff']
    equal = param['equal']

    strings = get_strings(files)

    if extract:
        display_strings(strings)

    if diff:
        if len(strings) < 2:
            logging.error("I need at least two files to compute differences")
        get_diff_strings(strings, files)

    if equal:
        if len(strings) < 2:
            logging.error("I need at least two files to get common strings")
        get_equal_strings(strings[0], strings[1])

    # if file_b:
    #     strings_b = get_strings(file_b)
    #     if extract:
    #         extract_strings(strings_a, strings_b)
    #     if diff:
    #         diff(strings_a, strings_b)

    # else:
    #
    #
    #     if diff:
    #         logging.error("I need a second file to compute differences")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", "--input", required=True, nargs='+',  # "../data/xtrain.txt"
    #                    help="input dataset")

    parser.add_argument("-i", "--input", dest='input', nargs='+', required=True,
                        help="first strings xml file ")

    # parser.add_argument("-j", "--jnput", dest='jnput', required=False,
    #                     help="second strings xml file ")

    parser.add_argument("-e", "--extract", dest="extract", required=False,
                        action='store_true', help="extract the strings ")

    parser.add_argument("-d", "--diff", dest="diff", required=False,
                        action='store_true', help="show different lines")

    parser.add_argument("-q", "--equal", dest="equal", required=False,
                        action='store_true', help="show equal lines")


    arguments = parser.parse_args()

    param = {}
    param['input'] = arguments.input
    # param['jnput'] = arguments.jnput
    param['extract'] = arguments.extract
    param['diff'] = arguments.diff
    param['equal'] = arguments.equal

    main(param)


# $ path=/Users/albarron/projects/My_Website/files/softloc/tintbrowser; python3 softloc_strings.py -i $path/en/strings.xml $path/afternoon-fr-1/strings.xml $path/afternoon-it-2/strings.xml $path/afternoon-it-4/strings.xml $path/afternoon-it-6/strings.xml $path/morning-es-1/strings.xml $path/morning-it-3/strings.xml $path/morning-it-5/strings.xml $path/afternoon-it-1/strings.xml $path/afternoon-it-3/strings.xml $path/afternoon-it-5/strings.xml $path/morning-it-2/strings.xml $path/morning-it-4/strings.xml $path/switch-it-1/strings.xml -e > kk

# Getting all the entries
# $ path=/Users/albarron/projects/My_Website/files/softloc/tintbrowser; python3 softloc_strings.py -i $path/en/strings.xml $path/afternoon-fr-1/strings.xml $path/afternoon-it-2/strings.xml $path/afternoon-it-4/strings.xml $path/afternoon-it-6/strings.xml $path/morning-es-1/strings.xml $path/morning-it-3/strings.xml $path/morning-it-5/strings.xml $path/afternoon-it-1/strings.xml $path/afternoon-it-3/strings.xml $path/afternoon-it-5/strings.xml $path/morning-it-2/strings.xml $path/morning-it-4/strings.xml $path/switch-it-1/strings.xml -e > kk

# Computing which ones have "not" been translated (may include non-translatable)
# $ for d in morning-es-1 morning-it-2 morning-it-3 morning-it-4 morning-it-5 afternoon-fr-1 afternoon-it-1 afternoon-it-2 afternoon-it-3 afternoon-it-4 afternoon-it-5 afternoon-it-6 switch-it-1; do  echo $d; python3 softloc_strings.py -i $path/en/strings.xml $path/$d/strings.xml -d > kk ; echo; echo; done

# Computing the differences between all pairs (only possible for Italian)

