import inspect
import re
import time
import sys
import argparse


def parse_solutions(lines, fmt="^(?P<num>\d+)\.\s+(?P<solution>\S+)$"):
    refmt = re.compile(fmt)
    for line in lines:
        match = refmt.match(line.rstrip())
        if match:
            num, solution = int(match.group('num')), match.group('solution')
            yield num, (int(solution) if re.match('[\d-]+$', solution) else solution)

def run():
    import problems

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--solutions', metavar='SOLUTIONS_FILE', default='solutions.txt')
    parser.add_argument('-v', '--show_solutions', default=False, action='store_true')
    parser.add_argument('problems', nargs='*')

    args = parser.parse_args()

    ignored = map(int, (p[1:] for p in args.problems if p.startswith('-')))
    selected = map(int, (p for p in args.problems if not p.startswith('-')))

    # map problem numbers to their solution functions
    problems = dict((int(re.match('problem(\d+)$', s).group(1)), fun)
                    for (s, fun) in inspect.getmembers(problems) if s.startswith('problem'))

    # you can grab the solution file from "http://projecteuler-solutions.googlecode.com/svn/trunk/Solutions.txt"
    with open(args.solutions) as fp:
        solutions = dict(parse_solutions(fp))

    tstart = time.time()

    ok, ran = 0, 0
    for num, problem in sorted(problems.iteritems(), key=lambda x: x[0]):
        if selected and not num in selected or ignored and num in ignored:
            continue
        print 'problem', num, '...',
        sys.stdout.flush()
        start = time.time()
        solution = solutions.get(num)
        if solution is not None:
            try:
                result = problem()
            except Exception, e:
                print 'ERROR: %s' % e
            else:
                took = time.time() - start
                ran += 1
                _pass = result == solution
                if _pass:
                    ok += 1

                print '%s (%0.3fs)' % ('OK' if _pass else 'FAIL', took,),
                print '[%s]' % (result,) if args.show_solutions or not _pass else ''
        else:
            print "we don't know the solution"

    print
    print '='*75
    print 'ran', ran, 'problems (%d fail) in %0.3f seconds' % (ran - ok, time.time() - tstart)


if __name__ == '__main__':
    run()
