#!/usr/bin/env python
if __name__ == "__main__":
  from ownSyncUtils import *
  import argparse
  import sys
  import getpass
  from argparse import RawTextHelpFormatter
  if len(sys.argv) <= 1:
    sys.argv.append("--help")
  else:
    sys.argv.pop(0)

  t = """type of sync to do. (Default: both) The options are:
\tto - Local is seen as the master repo, everything remote is replaced, updated or deleted from.
\tfrom - Remote is seen as the master repo, everything local will be replaces, updated or deleted till it looks exactly like whats on the server.
\tboth - Local and Remote paths are compared and merged. The newest file will be used in both places."""
  parser = argparse.ArgumentParser(description="Command line tool used to sync your ownCloud files to and from local directory",
    formatter_class=RawTextHelpFormatter)
  parser.add_argument('--url', help="url to use to connect to ownCloud (IE https://myCloud.com/owncloud/)",
            required=True)
  parser.add_argument('--user', help="Username to use to connect (Password will be prompted)", required=True)
  parser.add_argument('--local', help="local path to sync into", required=True)
  parser.add_argument('--rpath', help="remote path to sync into (Default: /)", required=False, default="/")
  parser.add_argument('--passcmd', help="Use this command to get password instead of asking via prompt.",
            required=False)
  parser.add_argument('--type', help=t, required=False)
  parser.add_argument('--exclude', help="Comma-separated list of paths to exclude from sync, this is relative to --rpath value",
            required=False, default="")
  Args = vars(parser.parse_args(sys.argv))

  print("Checking URL...  ")
  Args['url'] = getOwn(Args['url'])
  if Args['url'] is None:
    print("Problem with URL!!!")
    sys.exit(1)
  else:
    print("GOOD: {}".format(Args['url']))


  if Args['passcmd'] is None:
    pw = getpass.getpass()
  else:
    import subprocess
    pw = subprocess.check_output(Args['passcmd'].split()).strip()

  logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
  log = logging.getLogger("root")
  log.setLevel(logging.DEBUG)


  def merge_paths(path, root):
    return ("/".join([root.strip("/"), path.strip("/")])).strip("/")

  if len(Args['exclude']):
    exclude = [merge_paths(x, Args['rpath']) for x in Args['exclude'].split(",")]
  else:
    exclude = []

  X = ownClient(Args['url'], exclude)
  X.set_auth(Args['user'], pw)

  if Args['type'] is None or Args['type'].lower() == "both":
    X.syncBOTH(Args['local'], base=Args['rpath'])
  elif Args['type'].lower() == "to":
    X.syncTO(Args['local'], base=Args['rpath'])
  elif Args['type'].lower() == "from":
    X.syncFROM(Args['local'], base=Args['rpath'])
