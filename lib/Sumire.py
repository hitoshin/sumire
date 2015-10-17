#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys

from optparse import OptionParser

class Sumire:

    def __init__(self):
        
        parser = OptionParser()
        parser.set_defaults(input_type='default')
        parser.add_option('-k', '--knp',       action='store_const',
                          dest='input_type',     const='knp')
        parser.add_option('-r', '--reference', action='store',
                          dest='reference_file', type='string')
        parser.add_option('-s', '--summary',   action='store',
                          dest='summary_file',   type='string')
        (self.options, self.args) = parser.parse_args()

    def ReadInput(self, file_path):
        a_pattern = re.compile(u'^@|^EOS')
        lines = []
        f = open(file_path, 'r')
        for line in f.readlines():
            line = unicode(line, 'utf-8')
            line = line.rstrip()
            a_match = a_pattern.match(line)
            if a_match == None:
                lines.append(line)
        return lines

    def MakeDistribution(self, lines):
        distribution = {}
        c_pattern = re.compile(u'^名詞|^動詞|^形容詞')
        for line in lines:
            if self.options.input_type == 'default':
                array = line.split(u' ')
                for word in array:
                    if word in distribution:
                        distribution[word] = distribution[word] + 1
                    else:
                        distribution[word] = 1
            else:
                array = line.split(u' ')
                surface = array[0]
                pos     = array[3]
                c_match = c_pattern.match(pos)
                if c_match:
                    if surface in distribution:
                        distribution[surface] = distribution[surface] + 1
                    else:
                        distribution[surface] = 1
        return distribution

    def Calculate(self):
        lines = self.ReadInput(self.options.reference_file)
        r_dist = self.MakeDistribution(lines)
        
        lines = self.ReadInput(self.options.summary_file)
        s_dist = self.MakeDistribution(lines)
        
        print self.CalculateOverlap(r_dist, s_dist)

    def CalculateOverlap(self, r_dist, s_dist):
        overlap = 0
        total   = 0
        for key, value in r_dist.items():
            if key in s_dist:
                overlap = overlap + min(r_dist[key], s_dist[key])
            else:
                pass
            total = total + r_dist[key]
        return float(overlap) / total

if __name__ == '__main__':
    smr = Sumire()
    smr.Calculate()