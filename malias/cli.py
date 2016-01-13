'''System Aliases Modifier

List or modifies the contents of a system aliases file

Usage: malias [options] [--] [NAME [VALUE]...]

Options:
  -a --add             Add new values to name
  -d --delete          Delete values from name
  -r --replace         Replace name with the new values
  -s --sort            Sort names. Retains order by default.
  -S --sort-values     Sort values by key.
  -w NUM --wrap=NUM    Wrap lines to NUM characters. [default: 0]
  -f FILE --file=FILE  Target aliases file. [default: /etc/aliases]
  -o FILE --out=FILE   Output file. [default: -]
  -i --save            Save in place. Overrides --out.
  -h --help            Show this.
  --version            Show version.


'''

from __future__ import unicode_literals, print_function

import sys
import docopt
from collections import OrderedDict
from .core import load, dump
from . import __version__

def run(opts):
	# PRE
	dt = dict if opts['--sort'] else OrderedDict
	# IN
	with (opts['--file']=='-' and sys.stdin or open(opts['--file'])) as fp:
		aliases = dt(load(fp))
	if opts['NAME']:
		if opts['VALUE']:
			# Modify Name
			assert opts['--add'] or opts['--del'] or opts['--replace']
			if opts['--add']:
				for v in opts['VALUE']:
					if aliases[opts['NAME']].find(v)==-1:
						aliases[opts['NAME']].append(v)
			elif opts['--sync']:
				aliases[opts['NAME']][:] = opts['VALUE']
			elif opts['--del']:
				for v in opts['VALUE']:
					i = aliases[opts['NAME']].find(v)
					if i > -1:
						aliases[opts['NAME']].pop(i)
		else:
			# Query Name
			print('\n'.join(aliases[opts['NAME']]))
			return
	# Tweak
	if opts['--sort-values']:
		for v in aliases.values():
			v.sort()
	# Output
	fn = opts['--file'] if opts['--save'] else opts['--out']
	with (sys.stdout if fn=='-' else open(fn, 'w')) as fp:
		dump((iter,sorted)[opts['--sort']](aliases.items()), fp, int(opts['--wrap']))

def main():
	try:
		run(docopt.docopt(__doc__, version=__version__))
	except KeyError, e:
		print(str(e))

if __name__ == '__main__':
	main()
