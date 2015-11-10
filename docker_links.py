#! /usr/bin/env python3

"""
    DockerLinks a kiss class which help to get links info in a docker
    container.
"""

import json
import os
import re


class DockerLinks(object):

    "DockerLinks a kiss class which help to get links info in a docker \
        container."

    def __init__(self):
        self._get_links()

    def __enter__(self):
        return self

    def __exit__(self):
        pass

    def _get_links(self):

        "List all links and return dictionnay with link name, ip address, \
            ports and protocols."

        self.all_links = {}
        # nb_args = len(args)
        # Read hosts file
        with open('/etc/hosts') as hosts:
            for line in hosts:
                split = line.split()
                if len(split) < 3:
                    continue
                # Check if entry is a link
                link_ip = split[0]
                link_name_env = split[1].upper().replace('-', '_')
                link_name = split[1]
                env_var = "{link_name}_NAME".format(link_name=link_name_env)
                # if nb_args and link_name not in args:
                #     continue
                # Check if ip is already in dict
                if self._is_duplicated(link_ip):
                    self._add_name(ip=link_ip, names=split[1:])
                    continue
                if env_var in os.environ:
                    self.all_links[link_name] = {
                        "ip": link_ip,
                        "ports": _find_ports(link_name_env),
                        "environment": _find_env(link_name_env),
                        "other_names": split[2:]
                    }

    def _is_duplicated(self, ip):
        for _, item in self.all_links.items():
            if ip == item["ip"]:
                return True
        return False

    def _add_name(self, ip, names):
        for name in self.all_links:
            if self.all_links[name]["ip"] == ip:
                lst = self.all_links[name]["other_names"]
                self.all_links[name]["other_names"] = list(set(lst + names))
                self.all_links[name]["other_names"].sort()
                if name in self.all_links[name]["other_names"]:
                    self.all_links[name]["other_names"].remove(name)

    def links(self, *args):
        nb_args = len(args)
        if not nb_args:
            return self.all_links
        return {link: item for link, item in self.all_links.items()
                if link in args or
                len(set(item["other_names"]).intersection(args))}

    def to_json(self, *args):
        print(json.dumps(self.links(*args),
                         sort_keys=True,
                         indent=4,
                         separators=(',', ': ')
                         ))


def _find_ports(link_name):
    rtn = {}
    p = re.compile('^{link}_PORT_(\d*)_(UDP|TCP)$'.format(link=link_name))
    for key in os.environ:
        m = p.match(key)
        if m:
            rtn[m.group(1)] = {
                "protocol": m.group(2).lower(),
            }
    return rtn


def _find_env(link_name):
    rtn = {}
    p = re.compile('^{link}_ENV_(.*)$'.format(link=link_name))
    for key, value in os.environ.items():
        m = p.match(key)
        if m:
            rtn[m.group(1)] = value
    return rtn


if __name__ == '__main__':
    links = DockerLinks()
    print(links.to_json())
