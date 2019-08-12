#!/usr/bin/python3

import sys



def runOnDb(fn_):
	pass


def main():

	usage = "python3 " + sys.argv[0] + " <runOnDb.sql>"

	if len(sys.argv) != 2:
		sys.stderr.write("Error: incorrect number of arguments\n" + usage + '\n\n')
		sys.exit()

	runOnDb(sys.argv[1])


if __name__ == '__main__':
	main()
