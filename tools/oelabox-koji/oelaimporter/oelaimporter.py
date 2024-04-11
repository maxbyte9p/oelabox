import argparse
import sys
import os
import re
from typing import Union, Iterable
import json

from github import Github, Auth
from github.Organization import Organization
from github.PaginatedList import PaginatedList
from github.Branch import Branch
from github.Repository import Repository
import github

import koji

# Create Github session.
# String containing OAuth token optional.
def create_github_session(token: str) -> Github:
    return Github(auth=Auth.Token(token)) if token else Github()

def get_organization(session: Github, org: str) -> Organization:
    return session.get_organization(org)

def get_raw_repos(org: Organization, visibility: str = 'public') -> PaginatedList:
    return org.get_repos(visibility)

# I wanted to avoid using a try except statement, but it's the best way to handle this.
# I didn't want to deal with the exception because if it fails it won't cause any real harm.
# Returning None always makes more sense since it can be easily processed. Idk I'm weird I guess
def get_raw_repo(org: Organization, reponame: str) -> Union[Repository, None]:
    try:
        return org.get_repo(reponame)
    except:
        return None

# I don't like how dirty this is. Could be made way easier and neater.
def create_koji_session(config_name: str) -> koji.ClientSession:
    koji_config = koji.read_config(config_name)
    koji_session_opts = koji.grab_session_options(koji_config)
    koji_session = koji.ClientSession(koji_config['server'], koji_session_opts)
    koji_session.gssapi_login()
    koji_session.exclusiveSession(force=True) # Without this Koji doesn't want to be nice if we ctrl-c

    return koji_session

def koji_import(session: koji.ClientSession, r: Repository, b: Branch, d: str, u: str) -> int:
    session.packageListAdd(d, r.name, u)
    return session.build('git+{}#{}'.format(r.clone_url,b.commit.sha),d)

# Match branch name against wanted branch name.
# Can toggle regex mode on or off.
# This is a one-liner if statement that looks weird.
# If regex mode is enabled the return value of re.match is converted into a boolean with "is not None" then returned.
# This is easy to do because the way re.match returns can be thought of as a boolean
# If regex mode is disabled return the boolean result of "b.name == pb"
def branch_match(b: Branch, pb: str, regmod: bool) -> bool:
    return re.match(pb, b.name) is not None if regmod else b.name == pb

# Check if repository has desired branch or if regex mode is enabled has matching branches.
# Return tuple of matches or return None if no matches are found.
# This oneliner takes advantage of how the filter function works.
# Since branch_match always returns a bool we can generate a tuple of matching branches based on that.
# Any branches which make the curried branch_match return True has their data included in the tuple.
# If the tuple ends up empty because there are no matches then just return None instead because it's easier to work with.
def has_branch(r: Repository, pb: str, regmod: bool) -> Union[tuple[Branch], None]:
    return tuple(filter(lambda x: branch_match(x, pb, regmod), r.get_branches())) or None

# Create import target
# returns (Repository, (Branch, ...)) or (Repository, None)
def create_import_target(r: Repository, pb: str, regmod: bool) -> tuple[Repository, Union[tuple[Branch], None]]:
    return (r, has_branch(r, pb, regmod))

def has_branch_matches(imptar: tuple[Repository, Union[tuple[Branch], None]]) -> bool:
    return imptar[1] is not None

# Import package into Koji and return tuple containing import data.
# At first glance this one-liner looks a little hard to read, but in reality once understood is pretty easy to grasp.
# Essentially we are building up a nested tuple structure which is really easy to manipulate.
# We start out with the first layer which is (Repository, tuple).
# Then we go into the second layer where we have a lambda that constructs the second layer. (Repository, (tuple))
# After that we go to the third layer which constructs one or more tuples of a Branch and its import ID returned by koji_import. (Repository, ((Branch, Import_ID), ...))
def import_pkg(session: koji.ClientSession, r: Repository, b: tuple[Branch], d: str, u: str) -> tuple[Repository, tuple[tuple[Branch, int]]]:
    return (r, (lambda : tuple((i,koji_import(session, r, i, d, u)) for i in b))())

# Create a pretty banner for string using character.
# This one-liner is used to create the pretty banners in human readable mode.
# It's pretty clever for it's mathy stuff.
# First our char is printed 3 times and constructs a string "==="
# Then "===" is concatenated with "Oela Importer". "===Oela Importer"
# After that a new string using char is constructed using a lambda which fetches the width of our terminal then substracts it by the length of our initial string "===Oela Importer".
# Then both "===Oela Importer" and "======..." are concatenated then returned.
def make_banner(s: str, c: str) -> str:
    return c*3 + s + c*(lambda : os.get_terminal_size().columns - len(c*3 + s))()

# Print import data as human readable.
# some Python string magic is used here to substitute where our data goes.
# The first bit is self-explanatory.
# The second bit uses a lambda which converts a (Branch, Import_ID) tuple into human readable format.
# The first list comprehension makes a list of all the branch names.
# The second list comprehension makes a list of all the import IDs.
# The tuple created from that is mapped as arguments to the format function.
def human_print_import_data(impdat: tuple[Repository, tuple[tuple[Branch, int]]]) -> None:
    print(make_banner('Import', '-'))
    print('  Repo: {}\n  Branch Matches: {}\n  Import IDs: {}'.format(impdat[0].name, *(lambda : ([ i[0].name for i in impdat[1] ], [ i[1] for i in impdat[1] ]))()))

# Print import data as machine readable.
# This is pretty simple and the import data structure isn't changed much or really at all.
# The import data structure is converted into a dictionary so it can be JSON encoded.
# A list comprehension is used to build the 'imported' key.
# This is also meant to be printed for every set of import data.
# The JSON will look something like this.
# { 'repo': 'bash', 'imported': [ { 'branch_match': 'el8', 'import_id': 42 } ] }
def machine_print_import_data(impdat: tuple[Repository, tuple[tuple[Branch, int]]]) -> None:
    print(json.dumps({ 'repo': impdat[0].name, 'imported': [ { 'branch_match': i[0].name, 'import_id': i[1] } for i in impdat[1] ]}))

# Generic function which will print import data as human readable or machine readable based on whether or not machine mode is enabled.
def print_import_data(impdat: tuple[Repository, tuple[tuple[Branch, int]]], machmod: bool) -> None:
    return machine_print_import_data(impdat) if machmod else human_print_import_data(impdat)

# Parse a string containing "i" or "i:i" to slice value for chunkify.
def chunk(s: str) -> slice:
    return slice(*tuple(int(i) for i in s.split(":")[:2]))

# Slice iterable into a chunk if a slice value is provided.
# If None is provided return the unchanged Iterable.
def chunkify(i: Iterable, s: Union[slice, None]) -> Iterable:
    return i[s] if s else i

#def run_import(r: Repository, pb: str, regmod: bool, machmod: bool, user: str, pd: str, ksess: Koji.ClientSession):

    

def main():
    parser = argparse.ArgumentParser(
            prog='oelaimporter',
            description='Imports RPM sources from an SCM on Github.',
            epilog='Oela Importer is part of the Oela Box toolset.',
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50),
    )

    parser.add_argument('-k', '--kojiconfig', default="koji", help='Koji config to use')
    parser.add_argument('-t', '--ghtoken', default="", help='Authenticate with Github using OAuth token.')
    parser.add_argument('-r', '--regmod', action='store_true', help='Enable regex mode for branch matching. Off by default.')
    parser.add_argument('-m', '--machmod', action='store_true', help='Enable machine output mode for parsing by other programs.')
    parser.add_argument('-c', '--chunk', default=None, type=chunk, help='Only import a chunk of repositories. Import all by default.')
    parser.add_argument('-o', '--only', default=None, help='Only import a specific repository.')
    parser.add_argument('-u', '--user', required=True, help='Authenticated kerberos user.')
    parser.add_argument('-s', '--scm', required=True, help='SCM to pull from')
    parser.add_argument('-d', '--dist', required=True, help='Dist to import to')
    parser.add_argument('-b', '--branch', required=True, help='Branch to pull from')


    args = parser.parse_args()

    if not args.machmod: 
        print(make_banner('Oela Importer', '='))
    else:
        github.set_log_level(0) # Disable for machine mode since it can prevent us from reading the JSON strings externally.

    session = create_github_session(args.ghtoken)

    org = get_organization(session, args.scm)

    # Very bolted on code here. Basically makes it so nothing needs to be changed in order to import a specific repository.
    # If the "-o" option is used then run get_raw_repo else fallback to default of get_raw_repos
    repos = get_raw_repo(org, args.only) if args.only else get_raw_repos(org)

    # These 2 if statements are also very bolted on. Basically we exit if for example the bash repo didn't exist.
    # If a repo didn't exist nothing really failed. It just didn't exist. 
    # Processing instead of throwing an error is also in line with how branch matching is handled.
    # If a repo doesn't have the branch just filter it out! No reason to stop execution.
    if repos is None:
        sys.exit()
    
    # Because Oela Importer was initially designed for mass imports this just makes the single repository returned from get_raw_repo into an iterable.
    # Just drill a couple holes and bolt it on! That's how Oela Importer was designed to begin with. I've had the "-o" feature in mind for a long time.
    # Starting with iterable processing only made sense because of the variable length. 
    if isinstance(repos, Repository):
        repos = (repos,)

    koji_session = create_koji_session(args.kojiconfig)

    for i in map(lambda x: import_pkg(koji_session, x[0], x[1], args.dist, args.user), filter(has_branch_matches, map(lambda x: create_import_target(x, args.branch, args.regmod), chunkify(repos, args.chunk)))):
        print_import_data(i, args.machmod)

if __name__ == '__main__':
    main()
