import json
import urllib2
import re

# Config
from config import *
INC_CLOSED = False
disclaimer_files = ["disclaimer.txt"]

def get_all_boards():
  # Get all orgs
  orgs_dict = {}
  org_data = json.loads(get_url("https://api.trello.com/1/members/me/organizations?key=%s&token=%s" % (TRELLO_API_KEY,TRELLO_API_APP_TOKEN)))
  for org in org_data:
    orgs_dict[org["id"]] = org["displayName"]

  # Add a None in the orgs list for non-org associated boards
  orgs_dict[None] = "No Org"

  # Get all boards
  boards_list = []
  for org_id in orgs_dict.keys():
    if org_id:
      board_data = json.loads(get_url("https://api.trello.com/1/organizations/%s/boards?key=%s&token=%s" % (org_id,TRELLO_API_KEY,TRELLO_API_APP_TOKEN)))
    else:
      board_data = json.loads(get_url("https://api.trello.com/1/members/me/boards?key=%s&token=%s" % (TRELLO_API_KEY,TRELLO_API_APP_TOKEN)))
    for board in board_data:
      # If board is closed and config says not to include closed then skip
      if board["closed"] and not INC_CLOSED:
        pass
      else:
        boards_list.append({"id":board["id"],"name":board["name"],"org_id":board["idOrganization"]})
  
  return boards_list
  
def get_url(url):
  """fetch a URL, return as a string"""
  try:
    response = urllib2.urlopen(url)
  except urllib2.URLError: 
    print "Problem getting URL - %s" % (url)
  return response.read()

disclaimers = []
for disclaimer_file in disclaimer_files:
  f = open(disclaimer_file,"r")
  disclaimers.append(f.read())
  f.close()
  
boards = get_all_boards()
card_targets = {}
for board in boards:
  board_data = json.loads(get_url("https://api.trello.com/1/boards/%s?actions=all&actions_limit=1000&cards=all&lists=all&members=all&member_fields=all&checklists=all&fields=all&key=%s&token=%s" % (board["id"],TRELLO_API_KEY,TRELLO_API_APP_TOKEN)))
  for card in board_data["cards"]:
    for disclaimer in disclaimers:
      # Match on disclaimers by removing replacing all white space with a single space.
      if "\n".join(disclaimer.splitlines()) in "\n".join(card["desc"].splitlines()):
#      if re.sub("\s+", " ", disclaimer) in re.sub("\s+", " ", card["desc"]):
        card_targets[card["id"]] = disclaimer

for card_target in card_targets:
  pass

