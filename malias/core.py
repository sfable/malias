from __future__ import unicode_literals, print_function

special_chars='#|@,"\'\r\n\t '

def split_quote_string(entry, delim=','):
	if entry[:1] in ('"',"'"):
		quote = entry[0]
		entry = entry[1:]
		i = 0
		while i != -1:
			i = entry.find(quote,i+1)
			if entry[i-1:i]!="\\":
				return (entry[:i].replace('\\'+quote,quote), entry[i+1:].split(delim, 1)[-1])
		return (entry, '')
	else:
		return entry.split(delim, 1)

def parse_entry(entry):
	name, values = split_quote_string(entry, ':')
	ret = (name.strip(), [])
	while values:
		values = split_quote_string(values)
		ret[1].append(values[0].strip())
		values = values[1:]
	return ret

def parse_aliases(data, entry=None):
	for line in data:
		if line.strip()[:1] in ('', '#'):
			pass
		elif line[:1] in ' \t':
			assert entry is not None
			entry += line
		else:
			if entry is not None:
				yield parse_entry(entry)
			entry = line

def loads(data):
	return parse_aliases(data.split('\n'))

def load(fp):
	return loads(fp.read())

def build_quote_string(s, chars=special_chars):
	for c in chars:
		if c in s:
			return '"{}"'.format(s.replace('"','\\"'))
	return s

def build_entry(entry, wrap=0, fmt=None):
	name = build_quote_string(entry[0], chars=':'+special_chars)
	values = map(build_quote_string,entry[1])
	vjoin = ', '.join
	if wrap:
		l = len(name)+2
		wrap -= l
		if wrap > 0:
			t = wrap
			newv = []
			for value in values:
				lv = len(value)
				if t and wrap < t+lv:
					t=0
					newv += [[]]
				if newv[-1]:
					t+=2
				newv[-1].append(value)
				t+=lv
		values = map(vjoin, newv)
		vjoin = (',\n'+' '*l).join
	return (fmt is None and '{0}: {1}' or fmt).format(name, vjoin(values))

def build_aliases(aliases, wrap=0, fmt=None):
	return (build_entry(entry, wrap, fmt) for entry in aliases)

def dumps(aliases, wrap=0, fmt=None):
	return '\n'.join(build_aliases(aliases, wrap, fmt))

def dump(aliases, fp, wrap=0, fmt=None):
	fp.write(dumps(aliases, wrap, fmt)+'\n')

def main(filename='/etc/aliases'):
	with open(filename) as fp:
		print(dumps(load(fp)))

if __name__ == '__main__':
	import sys
	main(*sys.argv[1:])
