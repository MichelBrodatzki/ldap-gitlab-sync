import os
import ldap

def fetch_groups(logger):
    # TODO: Raise exception if env vars aren't set!
    ldap_conn = ldap.initialize("ldap://{}:{}".format(os.getenv("LDAP_HOST"), os.getenv("LDAP_PORT")))
    ldap_conn.simple_bind_s(os.getenv("LDAP_BIND_DN"), os.getenv("LDAP_BIND_PASSWORD"))

    # Search for all groups in LDAP_GROUPS_BASE with relevant objectClass
    logger.debug("Searching in {} for objectClass={}".format(os.getenv("LDAP_GROUPS_BASE"), os.getenv("SYNC_LDAP_GROUP_OBJECTCLASS")))
    group_search = ldap_conn.search_s(os.getenv("LDAP_GROUPS_BASE"), ldap.SCOPE_SUBTREE, "(objectClass={})".format(os.getenv("SYNC_LDAP_GROUP_OBJECTCLASS")))

    groups = {}

    base_group = os.getenv("GITLAB_BASE_GROUP")
    admin_group = os.getenv("SYNC_LDAP_ADMIN_GROUP")

    guest_level = int(os.getenv("SYNC_GUEST_LEVEL"))
    group_level = int(os.getenv("SYNC_GROUP_LEVEL"))
    admin_level = int(os.getenv("SYNC_ADMIN_LEVEL"))

    groups[base_group] = []

    for group_dn, group_object in group_search:
        current_group_name = (group_object["cn"][0].decode("utf-8"))

        # Check if group has users
        if not "memberUid" in group_object:
            logger.verbose("Skipping {}. No members!".format(current_group_name))
            continue

        if not os.getenv("SYNC_LDAP_GITLAB_GROUP_ATTRIBUTE") in group_object:
            logger.warning("Skipping {}. No GitLab path!".format(current_group_name))
            continue

        current_group = (group_object[os.getenv("SYNC_LDAP_GITLAB_GROUP_ATTRIBUTE")][0].decode("utf-8"))
        current_users = ["(uid={})".format(user.decode("utf-8")) for user in group_object["memberUid"]]

        logger.debug("Searching for {} in {}".format("(&(|{})(objectClass={}))".format("".join(current_users), os.getenv("SYNC_LDAP_USER_OBJECTCLASS")), os.getenv("LDAP_USERS_BASE")))

        users_search = ldap_conn.search_s(os.getenv("LDAP_USERS_BASE"), ldap.SCOPE_SUBTREE, "(&(|{})(objectClass={}))".format("".join(current_users), os.getenv("SYNC_LDAP_USER_OBJECTCLASS")))

        groups[current_group] = []

        for user_dn, user_object in users_search:
            current_user = (user_object["uid"][0].decode("utf-8"))

            if not os.getenv("SYNC_LDAP_GITLAB_USER_ATTRIBUTE") in user_object:
                logger.warning("Skipping {} for {}. No GitLab user!".format(current_user, current_group))
                continue

            if current_group_name == admin_group:
                # Add user to base_group if current_group is admin_group
                groups[base_group].extend([(account.decode("utf-8"), admin_level) for account in user_object[os.getenv("SYNC_LDAP_GITLAB_USER_ATTRIBUTE")]])
            else:
                # Add user to current_group with group_level
                groups[current_group].extend([(account.decode("utf-8"), group_level) for account in user_object[os.getenv("SYNC_LDAP_GITLAB_USER_ATTRIBUTE")]])

    admins = []

    # Add every user at guest_level to base_group, if not already in there
    # Remove all admins from higher groups
    for group in groups:
        if group == base_group:
            admins = [user[0] for user in groups[group]]
            logger.debug("Current admins are: {}".format(admins))
        else:
            groups[group] = list(filter(lambda user: user[0] not in admins, groups[group]))
            for user in groups[group]:
                if user[0] not in [base_user[0] for base_user in groups[base_group]]:
                    groups[base_group].append((user[0], guest_level))

    return groups
