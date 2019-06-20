#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Utility functions used throughout charfetch
"""
import yaml

def load_yaml_file(fileName):
    """ Convenience function for loading yaml files """
    try:
        with open(fileName, 'r') as f:
            return yaml.safe_load(f)
    except:
        pass

def convert_to_char_list(data):
    """ Convert a dictionary of {region:{realm:[toons]}} to a list of characters """
    try:
        return [{'name' : character, 'realm' : realm, 'region' : region} for region,realms in data.items()
                for realm,characters in realms.items()
                for character in characters]
    except:
        pass

def flatten(l):
    output = []

    for i in l:
        if type(i) == list:
            output += flatten(i)
        else:
            output.append(i)

    return output
