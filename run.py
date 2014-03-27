import inspect
import re
import time
import sys
import argparse


def parse_solutions(lines, fmt=r"^(?P<num>\d+)\.\s+(?P<solution>\S+)$"):
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
    parser.add_argument('-t', '--show-traceback', default=False, action='store_true')
    parser.add_argument('problems', nargs='*')

    args = parser.parse_args()

    ignored = list(map(int, (p[1:] for p in args.problems if p.startswith('-'))))
    selected = list(map(int, (p for p in args.problems if not p.startswith('-'))))

    # map problem numbers to their solution functions
    problems = dict((int(re.match(r'^problem(\d+)$', s).group(1)), fun)
                    for (s, fun) in inspect.getmembers(problems) if s.startswith('problem'))

    # you can grab the solution file from "http://projecteuler-solutions.googlecode.com/svn/trunk/Solutions.txt"
    with open(args.solutions) as fp:
        solutions = dict(parse_solutions(fp))

    tstart = time.time()

    ok, ran = 0, 0
    for num, problem in sorted(problems.items(), key=lambda x: x[0]):
        if selected and not num in selected or ignored and num in ignored:
            continue
        print('problem', num, '...', end='', flush=True)
        start = time.time()
        solution = solutions.get(num)
        if solution is not None:
            ran += 1
            try:
                result = problem()
            except Exception as e:
                if args.show_traceback:
                    raise
                print('ERROR:', e)
            else:
                took = time.time() - start
                pass_ = result == solution
                if pass_:
                    ok += 1

                print('{0} ({1:0.3f}s)'.format('OK' if pass_ else 'FAIL', took))
                if args.show_solutions or not pass_:
                    print('[{0}]'.format(result))
        else:
            print("we don't know the solution")

    print()
    print('=' * 75)

    fail_count = ran - ok
    time_taken = time.time() - tstart
    print('ran', ran, 'problems ({0} failed) in {1:0.3f} seconds'.format(fail_count, time_taken))


if __name__ == '__main__':
    run()
