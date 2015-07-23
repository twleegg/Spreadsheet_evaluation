#! /usr/bin/python
# -*- coding: utf-8 -*-
# Author: Tzu-Wen Lee

# global import
import sys
import re

# global variables
OPERANDS = ['+', '-', '*', '/']


class Cell:
    def __init__(self, s):
        self.items = map(lambda x: self.standardize(self, x), s.split())

        self.references = set()
        for item in self.items:
            if isinstance(item, tuple):
                self.references.add(item)

        if not self.references:
            self.post_order(self)
        else:
            self.val = 0

    def __str__(self):
        return str(self.val).rstrip('0').rstrip('.')    # remove trailing zeros

    # Standardize the input as following
    # numeric -> float, operand -> string, reference -> tuple
    @staticmethod
    def standardize(self, s):
        try:
            return float(s)
        except ValueError:
            pass

        if s in OPERANDS:
            return s
        else:
            match = re.match(r'^([A-Za-z]+)([0-9]+)$', s)
            groups = match.groups()
            return int(groups[1])-1, self.get_column(self, groups[0])

    # Get Column index from alphabetic representation
    # for example: AB -> 28
    @staticmethod
    def get_column(self, column):
        column = column.upper()
        n = 0
        for i in xrange(len(column)):
            n *= 26
            n += ord(column[i]) - ord('A')
        return n

    # Calculate the post order commands saved in self.items
    # and store the result to self.val
    @staticmethod
    def post_order(self):
        stack = []
        for x in self.items:
            if isinstance(x, float):
                stack.append(x)
            elif x in OPERANDS:
                try:
                    a, b = stack.pop(), stack.pop()
                except IndexError:
                    print "Error. There is not enough value to do the calculation."
                    return
                if x == '+':
                    stack.append(a+b)
                elif x == '-':
                    stack.append(a-b)
                elif x == '*':
                    stack.append(a*b)
                elif x == '/':
                    stack.append(a/b)
            else:
                print 'Error. Cannot recognize operand.'
                return

        if stack:
            self.val = stack.pop()
        else:
            return 'Error. There is no result for the operation.'


def evaluate(input_file, output_file):
    # Read the input file and convert each cell into Cell instance
    try:
        table = []
        with open(input_file, 'r') as f:
            for line in f.readlines():
                table.append(map(lambda c: Cell(c), line.strip().split(',')))

                # check whether the number of columns
                if len(table[-1]) != len(table[0]):
                    print "Error. Number of columns are not consistent."
                    return
    except IOError:
        print "Error. Cannot read input file."
        return

    # Calculate the dimensions of table
    m = len(table)
    n = len(table[0])

    # Record the cells need to be solved
    unsolved = set([(i, j) for i in xrange(m) for j in xrange(n) if len(table[i][j].references) > 0])

    # Recursively solve the cells
    while unsolved:
        solved = set()
        for i, j in unsolved:
            # find the cells whose references has been solved
            if not table[i][j].references & unsolved:
                cell = table[i][j]
                # convert references into values
                for k in xrange(len(cell.items)):
                    if isinstance(cell.items[k], tuple):
                        x, y = cell.items[k]
                        cell.items[k] = table[x][y].val

                # calculate the value
                Cell.post_order(cell)
                solved.add((i, j))
        if not solved:
            print "Error. Some reference(s) cannot be solved."
            return
        unsolved -= solved

    # Write result into output file
    try:
        with open(output_file, 'w') as f:
            for row in table:
                f.write(','.join(map(str, row)))
                f.write('\n')
    except IOError:
        print "Error. Cannot write output file."
        return


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: % python <inputfile> <outputfile>"
    else:
        evaluate(sys.argv[1], sys.argv[2])