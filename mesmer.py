#!/usr/bin/python
"""
MESMER -- MEmoryze String MappER

#WARNING -- I did not write Memoryze.  Right now this capability is theory and
does not guarentee accuracy.

This script is used to search the av.db file generated by Memoryze by Mandiant.
#ProTip: Ensure you enumerate strings in memory when you run Memoryze for best results.

This script requires two arguments:
    The path to the av.db file.
    The string you are searching for (the search is NOT case sensitive).

usage example:
    python mesmer.py -f C:\audit\av.db -s "evil string"
"""

from optparse import OptionParser
import sqlite3
import sys
import os

def searchDB(filepath, searchstring):
  con = None

  try:
    con = sqlite3.connect(filepath)

    #find all the 'strings' tables.
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'strings_%'")

    #put the table names into a list
    tables = []
    tables = cur.fetchall()

    # loop through each table search for that string.
    for table in tables:
      cur.execute("SELECT pid, string FROM " + table[0] + " WHERE string LIKE '%" + searchstring + "%'")
      rows = cur.fetchall()
      
      #display the pid and the whole string it found
      for row in rows:
        print str(row[0]) + " -- " + row[1]
    
  except sqlite3.Error, e:
    print "Error %s" % e.args[0]
    sys.exit(1)

  finally:
    if con:
      con.close()


def main():
  parser = OptionParser(usage="usage: %prog [options]",
                        version="%prog 1.0")
  parser.add_option("-f",
                    action="store",
                    dest="filepath",
                    default=False,
                    help="This is the path to av.db file that Memoryze creates.")
  parser.add_option("-s",
                    action="store",
                    dest="searchstring",
                    default=False,
                    help="The string you want to search the file for, use double quotes \" \".",)
  (options, args) = parser.parse_args()

  # check to make sure all arguments are present
  mandatory = ['filepath', 'searchstring']
  for m in mandatory:
    if not options.__dict__[m]:
      print "Mandatory argument is missing.\n"
      parser.print_help()
      sys.exit(1)

  # run the search
  searchDB(options.filepath, options.searchstring)


if __name__ == '__main__':
    main()