# -*- coding: utf-8 -*-
#/usr/bin/python2
'''
Borrowed
from https://github.com/keithito/tacotron/blob/master/text/numbers.py
By kyubyong park. kbpark.linguist@gmail.com.
https://www.github.com/kyubyong/g2p
'''
from __future__ import print_function
import inflect
import re



_inflect = inflect.engine()
_comma_number_re = re.compile(r'([0-9][0-9\,]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]*)\.([0-9]+)')
_pounds_re = re.compile(r'£([0-9\.\,]*[0-9]+)')
_dollars_re = re.compile(r'\$([0-9\.\,]*[0-9]+)')
_ordinal_re = re.compile(r'[0-9]+(st|nd|rd|th)')
_number_re = re.compile(r'[0-9]+s*')
_final_s = re.compile(r's$')
_final_y = re.compile(r'y$')


def _remove_commas(m):
    return m.group(1).replace(',', '')


def _expand_decimal_point(m):
    strs = [_expand_number(m.group(1)), 'point', str.join(' ', [_inflect.number_to_words(n) for n in m.group(2)])]
    return str.join(' ', filter(lambda s: s != None and len(s) > 0, strs))


def _expand_dollars(m):
    match = m.group(1)
    parts = match.split('.')
    if len(parts) > 2:
        return match + ' dollars'    # Unexpected format
    dollars = int(parts[0]) if parts[0] else 0
    cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    if dollars and cents:
        dollar_unit = 'dollar' if dollars == 1 else 'dollars'
        cent_unit = 'cent' if cents == 1 else 'cents'
        return '%s %s, %s %s' % (dollars, dollar_unit, cents, cent_unit)
    elif dollars:
        dollar_unit = 'dollar' if dollars == 1 else 'dollars'
        return '%s %s' % (dollars, dollar_unit)
    elif cents:
        cent_unit = 'cent' if cents == 1 else 'cents'
        return '%s %s' % (cents, cent_unit)
    else:
        return 'zero dollars'


def _expand_ordinal(m):
    return _inflect.number_to_words(m.group(0))


def _expand_number_from_group(m):
    return _expand_number(m.group(0))

def _expand_number(group_text):
    has_s = _final_s.search(group_text)
    if has_s:
      group_text = re.sub(_final_s, '', group_text)
    
    num = int(group_text)
    if num > 1000 and num < 3000:
        if num == 2000:
            final_text = 'two thousand'
        elif num > 2000 and num < 2010:
            final_text = 'two thousand ' + _inflect.number_to_words(num % 100)
        elif num % 100 == 0:
            final_text = _inflect.number_to_words(num // 100) + ' hundred'
        else:
            final_text = _inflect.number_to_words(num, andword='', zero='oh', group=2).replace(', ', ' ')
    else:
        final_text = _inflect.number_to_words(num, andword='')
    
    if has_s:
        final_text = re.sub(_final_y, 'ie', final_text) + 's'
    return final_text

def normalize_numbers_before_tokenized(text):
    text = re.sub(_comma_number_re, _remove_commas, text)
    return text

def normalize_numbers(text):
    text = re.sub(_pounds_re, r'\1 pounds', text)
    text = re.sub(_dollars_re, _expand_dollars, text)
    text = re.sub(_decimal_number_re, _expand_decimal_point, text)
    text = re.sub(_ordinal_re, _expand_ordinal, text)
    text = re.sub(_number_re, _expand_number_from_group, text)
    return text
