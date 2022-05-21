import argparse
from dotenv import load_dotenv

from .util import Logger
from .ldap import fetch_groups as ldap_fetch_groups
from .gitlab import fetch_groups as gitlab_fetch_groups, add_members as gitlab_add_members, remove_members as gitlab_remove_members

def sync(verbosity, dry_run):
    logger = Logger(verbosity)

    logger.log("Fetching LDAP and GitLab members ...")
    logger.verbose("Fetching LDAP groups and their members") 
    ldap_groups = ldap_fetch_groups(logger)
    logger.debug("LDAP returned: {}".format(ldap_groups))

    logger.verbose("Fetching GitLab groups and their members")
    gitlab_groups = gitlab_fetch_groups(logger)
    logger.debug("GitLab returned: {}".format(gitlab_groups))

    logger.log("Creating diff ...")
    for group in ldap_groups:
        if group not in gitlab_groups:
            logger.warning("Skipping creating diff for {}. GitLab group doesn't exist!".format(group))
            continue

        logger.log("Diff for {}:".format(group))
        removals = list(set(gitlab_groups[group]) - set(ldap_groups[group]))
        logger.log("- {}".format(removals))
        additions = list(set(ldap_groups[group]) - set(gitlab_groups[group]))
        logger.log("+ {}".format(additions))

        if not dry_run:
            logger.log("Applying diff to GitLab ...")
            if len(removals) > 0:
                gitlab_remove_members(logger, group, removals)
            if len(additions) > 0:
                gitlab_add_members(logger, group, additions)
        else:
            logger.warning("Dry run! Not applying diff.")



def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Syncs LDAP group members to GitLab groups")
    parser.add_argument("--dry-run", action="store_true", help="only show changes. don't change anything.")

    echo_group = parser.add_mutually_exclusive_group()
    echo_group.add_argument("-q", "--quiet", action="store_true", help="don't output anything", dest="quiet")
    echo_group.add_argument("-w", "--warning", action="store_true", help="outputs only warnings and errors", dest="warning")
    echo_group.add_argument("-v", "--verbose", action="store_true", help="outputs more", dest="verbose")
    echo_group.add_argument("-d", "--debug", action="store_true", help="outputs most", dest="debug")
    args = parser.parse_args()

    verbosity = ((-2) * args.quiet) + ((-1) * args.warning) + (1 * args.verbose) + (2 * args.debug)

    sync(verbosity=verbosity, dry_run=args.dry_run)
