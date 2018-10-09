#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

import importlib
from optparse import OptionParser

class Sumire:

	def __init__(self):
		# Compile regular expressions
		self.a_pattern = re.compile(r'^@|^EOS|^$')
		self.c_pattern = re.compile(r'^名詞|^動詞|^形容詞|^副詞')

		self.parse_cabocha_pattern = re.compile(r' |,|\t')
		self.parse_knp_pattern = re.compile(r' ')
		self.parse_mecab_pattern = re.compile(r'\t|,')

		parser = OptionParser()
		parser.set_defaults(input_type='mecab',
							rouge_n=1)
		parser.add_option('-c', '--cabocha',
						  action='store_const',
						  dest='input_type',
						  const='cabocha')
		parser.add_option('-k', '--knp',
						  action='store_const',
						  dest='input_type',
						  const='knp')
		parser.add_option('-m', '--mecab',
						  action='store_const',
						  dest='input_type',
						  const='mecab')
		parser.add_option('-n', '--rouge_n',
						  action='store',
						  dest='rouge_n',
						  type='int')
		parser.add_option('-r', '--reference',
						  action='store',
						  dest='reference_file',
						  type='string')
		parser.add_option('-s', '--summary',
						  action='store',
						  dest='summary_file',
						  type='string')
		(self.options, self.args) = parser.parse_args()

	def calculate_rouge(self, **kwargs):

		# Interpret options from kwargs
		self.options.input_type = kwargs['input_type'] if 'input_type' in kwargs else self.options.input_type

		# Reference and summary are given as files
		if self.options.reference_file and self.options.summary_file:
			lines = self._read_input(self.options.reference_file)
			r_dist = self._make_distribution(lines)

			lines = self._read_input(self.options.summary_file)
			s_dist = self._make_distribution(lines)

		# Reference and summary are given as sentences
		elif ('reference' in kwargs and 'summary' in kwargs):
			lists = self._parse_sentence(reference)
			lines = self._read_input_from_lines(lists)
			r_dist = self._make_distribution(lines)

			lists = self._parse_sentence(summary)
			lines = self._read_input_from_lines(lists)
			s_dist = self._make_distribution(lines)

		# Reference and summary are given as lists
		elif ('reference_list' in kwargs and 'summary_list' in kwargs):
			lines = self._read_input_from_lines(kwargs['reference_list'])
			r_dist = self._make_distribution(lines)

			lines = self._read_input_from_lines(kwargs['summary_list'])
			s_dist = self._make_distribution(lines)
		
		return self._calculate_overlap(r_dist, s_dist)

	def _calculate_overlap(self, r_dist, s_dist):
		overlap = 0
		total   = 0
		for key, value in list(r_dist.items()):
			if key in s_dist:
				overlap = overlap + min(r_dist[key], s_dist[key])
			else:
				pass
			total = total + r_dist[key]
		return float(overlap) / total

	def _make_distribution(self, lines):
		distribution = {}
		sequence = []
		for line in lines:
			if self.options.input_type == 'default':
				array = line.split(' ')
				for word in array:
					distribution, sequence = self._add_word_into_distribution(distribution, sequence, word)

			elif self.options.input_type == 'cabocha':
				array = self.parse_cabocha_pattern.split(line)
				surface = array[0]
				pos		= array[1]
				c_match = self.c_pattern.match(pos)
				if c_match:
					distribution, sequence = self._add_word_into_distribution(distribution, sequence, surface)

			elif self.options.input_type == 'knp':
				array = self.parse_knp_pattern.split(line)
				surface = array[0]
				pos     = array[3]
				c_match = self.c_pattern.match(pos)
				if c_match:
					distribution, sequence = self._add_word_into_distribution(distribution, sequence, surface)

			elif self.options.input_type == 'mecab':
				array = self.parse_mecab_pattern.split(line)
				surface = array[0]
				pos     = array[1]
				c_match = self.c_pattern.match(pos)
				if c_match:
					distribution, sequence = self._add_word_into_distribution(distribution, sequence, surface)

		return distribution

	def _add_word_into_distribution(self, distribution, sequence, word):
		sequence.append(word)
		if len(sequence) == self.options.rouge_n:
			word = '-'.join(sequence)
			if word in distribution:
				distribution[word] = distribution[word] + 1
			else:
				distribution[word] = 1
			sequence.pop(0)
						
		return distribution, sequence

	def _parse_sentence(self, sentence):
		lists = [[]]
		self.MeCab = importlib.import_module('MeCab')
		mecab = self.MeCab.Tagger()
		array = mecab.parse(sentence).split('\n')
		for e in array:
			lists[0].append(e)
		return lists

	def _read_input(self, file_path):
		lines = []
		f = open(file_path, 'r')
		for line in f.readlines():
			#line = str(line, 'utf-8')
			line = line.rstrip()
			a_match = self.a_pattern.match(line)
			if a_match == None:
				lines.append(line)
		return lines

	def _read_input_from_lines(self, array):
		lines = []
		for line in array:
			line = line.rstrip()
			a_match = self.a_pattern.match(line)
			if a_match == None:
				lines.append(line)
		return lines

	#def _read_input_from_lines(self, array):
	#	lines = []
	#	for i in range(0, len(array)):
	#		for j in range(0, len(array[i])):
	#			a_match = self.a_pattern.match(array[i][j])
	#			if a_match == None:
	#				lines.append(array[i][j])
	#	return lines

if __name__ == '__main__':
	smr = Sumire()
	reference = "今日はとても暑いが私は好きです．"
	summary = "今日はとても寒くて私は嫌いです．"
	print((smr.calculate_rouge(reference = reference, 
							   summary = summary)))