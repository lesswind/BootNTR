#!/usr/bin/env python2

import sys
import os.path
import re

# Data at offsets of dbgKernelCacheInterface addresses for o3ds
dbgKernelCacheInterfaceDataOld3DS = (
	"\xF8\x43\x2D\xE9\x1A\x0B\x51\xE3\x01\x70\x80\xE0\x1F\x80\x87\xE2",
	"\xF8\x40\x2D\xE9\x01\x20\x80\xE0\x1F\x20\x82\xE2\x01\x09\x51\xE3\x00\x60\xA0\xE3\x1F\x50\xC2\xE3\x1F\x40\xC0\xE3\x0E\x00\x00\x2A\x05\x30\xA0\xE1\x04\x20\xA0\xE1\x01",
	"\xF8\x40\x2D\xE9\x01\x20\x80\xE0\x1F\x20\x82\xE2\x01\x09\x51\xE3\x00\x60\xA0\xE3\x1F\x50\xC2\xE3\x1F\x40\xC0\xE3\x0E\x00\x00\x2A\x05\x30\xA0\xE1\x04\x20\xA0\xE1\x02",
	"\xF8\x40\x2D\xE9\x01\x20\x80\xE0\x1F\x20\x82\xE2\x1A\x0B\x51"
)

# Data at offsets of dbgKernelCacheInterface for n3dss
dbgKernelCacheInterfaceDataNew3DS = (
	"\xF8\x4F\x2D\xE9\x00\x40\xA0\xE1\x01\x90\xA0\xE1\x0C\x11\x9F",
	"\xF8\x40\x2D\xE9\x01\x20\x80\xE0\x1F\x20\x82\xE2\x01\x09\x51",
	"\xF8\x43\x2D\xE9\x01\x90\xA0\xE1\x10\x11\x9F\xE5\x09\x20\x80",
	"\xF8\x40\x2D\xE9\x01\x20\x80\xE0\x1F\x20\x82\xE2\x1A\x0B\x51"
)


# Empty array where cache interface offsets will go
dbgKernelCacheInterfaceOffsets = ["","","",""]

# If not all arguments are provided, print out a "helpful" message
if len(sys.argv) < 3:
	print "Usage: finder.py <dump path> <console type>\n"
	print "Example: finder.py axiwramp.dmp o3ds"
	sys.exit()

# set file_path equal to the first argument and console_type to the second. Lowercase console_type in case some people use N3DS or similar over n3ds
file_path = sys.argv[1]
console_type = sys.argv[2].lower()

# Check if dump exists; if it does, use it, otherwise say file not found
if os.path.isfile(file_path):
	f = open(file_path, "rb")
	data = f.read()
	f.close()

	if console_type == "o3ds":
		for index, searchString in enumerate(dbgKernelCacheInterfaceDataOld3DS):
			dbgKernelCacheInterfaceOffsets[index] = data.find(searchString)
	elif console_type == "n3ds":
		for index, searchString in enumerate(dbgKernelCacheInterfaceDataNew3DS):
			dbgKernelCacheInterfaceOffsets[index] = data.find(searchString)
	else:
		print "Invalid console tpye! Valid console types: o3ds, n3ds"
		sys.exit()

	for index, offset in enumerate(dbgKernelCacheInterfaceOffsets):
		print "DEBUG:", offset 
		if offset > 385024: # If offset is greater than 385024 (0x5E000 in decimal), then it's in a different memory mapping - adjust accordingly.
			dbgKernelCacheInterfaceOffsets[index] = hex(offset + 4293668864) # offset plus 0xFFEC3000 in decimal
		else:
			dbgKernelCacheInterfaceOffsets[index] = hex(offset + 4293918720) # offset plus 0xFFF20000 in decimal 

	if console_type == "o3ds":
		print "dbgKernelCacheInterface cacheInterface_OldVER = {"
		print "\t//for old 3ds VER"
	else:
		print "dbgKernelCacheInterface cacheInterface_NEWVER = {"
		print "\t//for new 3ds VER"

	for index, offset in enumerate(dbgKernelCacheInterfaceOffsets):
		if index != 3:
			print "\t(void*)" + offset.upper() + ","
		else:
			print "\t(void*)" + offset.upper()
	print "}"
else:
	print "File not found!"