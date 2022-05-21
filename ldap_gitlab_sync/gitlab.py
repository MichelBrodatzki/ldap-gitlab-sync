from os import getenv
import gitlab

def fetch_groups(logger):
    gl_url = getenv("GITLAB_URL")
    gl_token = getenv("GITLAB_GROUP_TOKEN")
    gl_base_group = getenv("GITLAB_BASE_GROUP")

    groups = {}

    logger.verbose("Connecting to GitLab ...")
    gl = gitlab.Gitlab(url=gl_url, private_token=gl_token)
    
    logger.verbose("Searching for base group ...")
    eligible_base_groups = [group for group in gl.groups.list() if group.path == gl_base_group]
    logger.debug("Eligible base groups: {}".format([group.path for group in eligible_base_groups]))

    if len(eligible_base_groups) == 0:
        raise RuntimeError("Configured base group wasn't found.")

    if len(eligible_base_groups) > 1:
        raise RuntimeError("Configured base group isn't unique. This is a bug in this script!")

    
    base_group = eligible_base_groups[0]

    groups[base_group.path] = [(member.username, member.access_level) for member in base_group.members.list() if not gl.users.get(member.id).bot]

    subgroups = base_group.subgroups.list()
    for subgroup in subgroups:
        groups[subgroup.full_path] = [(member.username, member.access_level) for member in gl.groups.get(subgroup.id).members.list() if not gl.users.get(member.id).bot]

    return groups

def add_members(logger, group_path, user_list):
    logger.verbose("Adding users in {}".format(group_path))
    gl_url = getenv("GITLAB_URL")
    gl_token = getenv("GITLAB_GROUP_TOKEN")

    # Users cache
    users = {}

    gl = gitlab.Gitlab(url=gl_url, private_token=gl_token)
    
    for group in gl.groups.list():
        if group.full_path == group_path:
            for user in user_list:
                if user[0] not in users:
                    fetch_user = gl.users.list(username=user[0])
                    if len(fetch_user) == 0:
                        users[user[0]] = None
                        logger.warning("User {} not registered in GitLab".format(user[0]))
                    elif len(fetch_user) == 1:
                        users[user[0]] = fetch_user[0]
                    else:
                        users[user[0]] = None
                        logger.warning("Multiple matches in GitLab for user {}".format(user[0]))
                if users[user[0]] is not None:
                    try:
                        logger.debug("Adding {} to {}".format(user[0], group_path))
                        group.members.create({'user_id': users[user[0]].id,
                                          'access_level': user[1]})
                    except gitlab.GitlabCreateError:
                        logger.warning("{} already in group {}".format(user[0], group_path))




def remove_members(logger, group_path, user_list):
    logger.verbose("Removing users from {}".format(group_path))
    gl_url = getenv("GITLAB_URL")
    gl_token = getenv("GITLAB_GROUP_TOKEN")

    gl = gitlab.Gitlab(url=gl_url, private_token=gl_token)
    
    for group in gl.groups.list():
        if group.full_path == group_path:
            for user in user_list:
                for member in group.members.list():
                    if member.username == user[0]:
                        logger.debug("Removing {} from {}".format(user[0], group_path))
                        member.delete()
