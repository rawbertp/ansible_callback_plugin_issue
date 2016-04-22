from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
from ansible.plugins.callback import CallbackBase
from ansible import constants as C
from pprint import pprint
import os
import epdb
import logging, sys


class CallbackModule(CallbackBase):
    def __init__(self):
        super(CallbackModule, self).__init__()
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        logging.debug("+++++ v2_runner_on_failed")

        inventory = os.path.basename(os.path.realpath(self.play.get_variable_manager()._inventory.host_list))
        logging.debug("Inventory: " + inventory)

        play_name = self.play.name
        task_name = result._task.name
        host_name = result._host.name

        #logging.debug("Play: " + str(play_name) + " / Task: " + str(task_name) + " / Host: " + str(host_name))

        logging.debug("host.get_groups(): ->")
        logging.debug(result._host.get_groups())

        #epdb.st()

        # Haven't managed it yet to get the actual effective group vars...
        # The problem is that result._host.get_groups() returns an empty list!
        # (Epdb) result._host
        # localhost
        # (Epdb) result._host.get_groups()
        # [] <---

        x = self.play._variable_manager.get_vars(self.loader, play=self.play, task=result._task, host=result._host, use_cache=False)

        logging.debug("Var from 'all' group_vars: " + x.get("foo"))


    def v2_playbook_on_start(self, playbook):
        logging.debug("+++++ v2_playbook_on_start")
        self.playbook = playbook


    def v2_playbook_on_play_start(self, *args, **kwargs):
        logging.debug("v2_playbook_on_play_start(self, *args, **kwargs)")
        self.play = args[0]  # Workaround for https://github.com/ansible/ansible/issues/13948
        self.loader = args[0]._loader

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.task = task
