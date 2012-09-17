'''
 ====================================================================
 Copyright (c) 2005-2006 Barry A Scott.  All rights reserved.

 This software is licensed as described in the file LICENSE.txt,
 which you should have received as part of this distribution.

 ====================================================================
'''

import sys, os, cStringIO, re, pprint, string
import difflib

_debug = 0

class LiteralMatch:
    def __init__(self,start,end):
        self.start_pos = start
        self.end_pos = end

    def start(self):
        return self.start_pos
    def end(self):
        return self.end_pos


class LiteralSearch:
    def __init__(self, substring):
        self.substring = substring

    def search(self,line):
        try:
            start_pos = line.index( self.substring )
            end_pos = start_pos + len(self.substring)
            return LiteralMatch( start_pos, end_pos )
        except ValueError, detail:
            return None

class LiteralCaseBlindSearch:
    def __init__(self, substring):
        self.substring = substring.lower()

    def search(self,line):
        try:
            start_pos = line.lower().index( self.substring )
            end_pos = start_pos + len(self.substring)
            return LiteralMatch( start_pos, end_pos )
        except ValueError, detail:
            return None

class ReplaceDirtInString:
    def __init__(self, lines_list):
        self.lines_list = lines_list
        self.workdir = self.find( 'WorkDir' )
        self.python = self.find( 'PYTHON' )
        self.username = self.find( 'Username' )
        self.username_spaces = self.username
        while len(self.username_spaces) < 10:
            self.username_spaces = self.username_spaces + ' '

        # ------------------------------------------------------------------------
        # Version strings:
        # Date/Timestamps:
        #   2001-03-27-15-36-10
        #   19-Mar-01 14:52:12
        #   Jan 20 14:35
        #   Jan 20  2004
        # UUID:
        #   467a5469-d6df-e448-9de8-282096145563
        # Directory path:
        #   Drawn from TestRoot: xxxx
        # Username, Hostname:
        #   Drawn from Username: xxx & Hostname: xxx
        #

        dateAlphaNumeric_re = re.compile(r'\d+-[JFMASOND][a-z][a-z]-\d+ [ 0-9]\d:\d\d:\d\d')
        dateNumeric_re = re.compile(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(.\d+)?Z?')
        dateUnixLs1_re = re.compile(r'[JFMASOND][a-z][a-z] \d+ \d\d:\d\d')
        dateUnixLs2_re = re.compile(r'[JFMASOND][a-z][a-z]  \d\d\d\d')
        uuid_re = re.compile(r'[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}')
        checksum_re = re.compile(r'[0-9a-z]{32}')

        self.replacement_list = \
                    [(dateAlphaNumeric_re,          '<alpha-date-and-time>'),
                     (dateNumeric_re,               '<numeric-date-and-time>'),
                     (uuid_re,                      '<UUID>'),
                     (checksum_re,                  '<checksum>'),
                     (dateUnixLs1_re,               '<ls-date-and-time>'),
                     (dateUnixLs2_re,               '<ls-date-and-time>'),
                    ]


        if self.workdir:
                workdir_re1 = LiteralCaseBlindSearch( self.workdir )
                workdir_re2 = LiteralCaseBlindSearch( os.path.realpath( self.workdir ) )
                self.replacement_list.append(
                     (workdir_re1,        '<workdir>') )
                self.replacement_list.append(
                     (workdir_re2,        '<workdir>') )

        if self.python:
                python_re = LiteralCaseBlindSearch( self.python )
                self.replacement_list.append(
                     (python_re,        '<PYTHON>') )

        if self.username:
                username_spaces_re = LiteralSearch( self.username_spaces )
                self.replacement_list.append(
                        (username_spaces_re,        '<username>') )
                username_re = LiteralSearch( self.username )
                self.replacement_list.append(
                        (username_re,        '<username>') )

    def find( self, keyword ):
        for line in self.lines_list:
            parts = string.split( line, ':' )
            if parts[0] == keyword:
                value = string.strip( string.join( parts[1:], ':' ) )
                if _debug: print 'find(',keyword,') ->',value
                return value
        return ''

    def execute(self):
            return map(self.replace, self.lines_list)

    def replace(self,line):
        if _debug: print 'Processing: ',line
        for re_expr, replacement_text in self.replacement_list:
            while 1:
                if _debug: print '...trying:',replacement_text
                match = re_expr.search( line )
                if match == None:
                    break
                line = line[0:match.start()] + replacement_text + line[match.end():]
        return line


def stripDirty(filename):

    f = open(filename, 'r')
    contents = f.read()
    f.close()

    lines = string.split( contents.replace( '\r\n', '\n' ).replace( '\r', '\n' ), '\n' )
    replace = ReplaceDirtInString( lines )
    stripped_lines = replace.execute()

    return stripped_lines


# ------------------------------------------------------------------------
# main
 
def main(argv):
 
    try:

        BenchmarkFile = argv[1]
        ResultsFile = argv[2]

        print 'Info: Comparing', BenchmarkFile
        benchmark = stripDirty(BenchmarkFile)

        print 'Info: Against  ', ResultsFile
        results = stripDirty(ResultsFile)
        if _debug:
            print 'Debug: results after we called stripDirty'
            pprint.pprint(results)


        f = open(ResultsFile + '.clean','w')
        for line in results:
            f.write( line + '\n' )
        f.close()

        f = open(BenchmarkFile + '.clean','w')
        for line in benchmark:
            f.write( line + '\n' )
        f.close()



        if results != benchmark:
            print 'Error: Test failed - %s' % ResultsFile

            sm = difflib.SequenceMatcher()
            sm.set_seq1( benchmark )
            sm.set_seq2( results )
            opcodes = sm.get_opcodes()

            for tag, i1, i2, j1, j2 in opcodes:
                if tag in ['delete','insert','replace']:
                    print 'Error: --------------------------------------------------------------------------------'
                if tag in ['delete','replace']:
                    for line_index in range(i1,i2):
                        prefix = 'Benchmark(%d) %7s' % (line_index+1, tag)
                        print 'Error: %26s %s' % (prefix, benchmark[line_index])
                if tag in ['insert','replace']:
                    for line_index in range(j1,j2):
                        prefix = 'Result(%d) %7s' % (line_index+1, tag)
                        print 'Error: %26s %s' % (prefix, results[line_index])

            print 'Error: --------------------------------------------------------------------------------'
            return 1
        else:
            print 'Info: Test succeeded'
            return 0

#    except KeyboardInterrupt:
#        print 'Interrupted by Ctrl-C'
    except IOError, detail:
        print 'Error:', detail

    return 2

# ------------------------------------------------------------------------
 
if __name__ == "__main__":
    sys.exit(main( sys.argv ))

