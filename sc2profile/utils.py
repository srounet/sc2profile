#!/usr/bin/env python
"""
----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <srounet@gmail.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return Fabien Reboia
 * ----------------------------------------------------------------------------
"""

def replace_html_code(string):
    string = string.replace(u"\xc2\xa0\xe2\x80\x9c", ' "')
    string = string.replace(u"\xe2\x80\x9d", '"')
    string = string.replace(u"\xe2\x80\x99", "'")
    string = string.replace(u"\xe2\x80\xa6", "...")
    return string
