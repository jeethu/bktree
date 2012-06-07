import cmd
import sys
import time

from .import bktree
from .import lev


class BKREPL(cmd.Cmd):
    prompt = 'BK>'

    def __init__(self, wordfile=None):
        cmd.Cmd.__init__(self)
        s = set()
        t = time.time()
        if wordfile is not None:
            with open(wordfile, 'rb') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        s.add(word)
            self.bktree = bktree.BKTree(lev.lev, s)
            msg = "Loaded %d words in %.2f seconds"
            print >> sys.stderr, msg % (len(s), time.time() - t)
        else:
            self.bktree = bktree.BKTree(lev.lev)

    def do_query(self, line):
        """
        Query the tree:
        form 1: query <word>  # Distance is assumed to be 0
        form 2: query <word> <distance>
        """
        l = line.split()
        if len(l) == 1:
            word = l[0].strip().lower()
            distance = 0
        elif len(l) == 2:
            word, distance = l[0].strip().lower(), int(l[1].strip())
        else:
            print >> sys.stderr, "Invalid query"
            return
        t = time.time()
        r = self.bktree.search(word, distance)
        s = "Found %d matches in %.2f seconds" % (len(r), time.time() - t)
        print s
        print "#" * len(s)
        for term, distance in r:
            print "%s %s" % (term, distance)

    def do_add(self, line):
        """
        Add a word to the tree:
        add <word>
        """
        self.bktree.add(line.strip().lower())

    def do_render(self, line):
        """
        Render the tree to a GraphViz file and pdf
        """
        filename = line.strip()
        if not filename:
            filename = 'output.gv'
        self.bktree.render(filename)

    def do_EOF(self, line):
        return True


def main():
    if len(sys.argv) > 1:
        repl = BKREPL(sys.argv[1])
    else:
        repl = BKREPL()
    repl.cmdloop()

if __name__ == '__main__':
    main()
