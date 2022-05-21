from os import getenv
import gitlab

def get_groups():
    gl_url = getenv("GITLAB_URL")
    gl_token = getenv("GITLAB_GROUP_TOKEN")
    gl_base_group = getenv("GITLAB_BASE_GROUP")

    if gl_url is None or gl_token is None or gl_base_group is None: 
        raise ValueError("GitLab config variables not found. Is .env correctly configured?")

    gl = gitlab.Gitlab(url=gl_url, private_token=gl_token)
    eligible_base_groups = [group for group in gl.groups.list() if group.path == gl_base_group]

    if len(eligible_base_groups) == 0:
        raise RuntimeError("Configured base group wasn't found.")

    if len(eligible_base_groups) > 1:
        raise RuntimeError("Configured base group isn't unique. This is a bug in this script!")

    base_group = eligible_base_groups[0]

    print (base_group)
