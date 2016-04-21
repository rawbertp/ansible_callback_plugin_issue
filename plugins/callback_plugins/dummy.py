from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.callback import CallbackBase
from ansible import constants as C
from pprint import pprint
import os
import epdb
import logging, sys

try:
	from __main__ import cli
except ImportError:
    cli = None


class CallbackModule(CallbackBase):

    def __init__(self):
	super(CallbackModule, self).__init__()
        if cli:
		self._options = cli.options
        else:
		self._options = None

  	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)		


    def v2_runner_on_failed(self, result, ignore_errors=False):
	self._display.display("+++++ v2_runner_on_failed")
	inventory = os.path.basename(os.path.realpath(self.play.get_variable_manager()._inventory.host_list))

	logging.debug("Inventory: " + inventory)


	#play_name = self._display.display("Play: " + self.play.name)
	#task_name = self._display.display("Task: " + result._task.name)
	#host_name = self._display.display("Host:" + result._host.name)	


	# Haven't managed it yet to get the actual effective group vars... The problem is that result._host.get_groups() returns an empty list!
	# (Epdb) result._host
	# localhost
	# (Epdb) result._host.get_groups()
	# []

	x = self.play._variable_manager.get_vars(self.loader, play=self.play, task=result._task, host=result._host, use_cache=False)
	logging.debug("Var from 'all' group_vars: " + x.get("foo"))
	
	self._display.display(x.get("foo"))



	#for item in result._task.get_vars():
	#	self._display.display(item)

	#self._display.display(type((self.play.get_variable_manager().get_vars(task=result._task,host=result._host))))

	###self._display.display("GroupVar read by Callback Plugin --> " + self.play.get_variable_manager()._inventory.get_group(inventory).get_vars().get("foo"))
	###self._display.display("InventoryName --> " + inventory) 

    def v2_playbook_on_start(self, playbook):
	self._display.display("+++++ v2_playbook_on_start")
        self.playbook = playbook
	

#    def v2_playbook_on_play_start(self, play):
#	# This method doesn't seem to work/get called... https://github.com/ansible/ansible/issues/13948
#	self._display.display("+++++ v2_playbook_on_play_start")
#	#self._display.display(pprint(vars(play)))
#        #self.play = play


    def v2_playbook_on_play_start(self, *args, **kwargs):
	self._display.display("v2_playbook_on_play_start(self, *args, **kwargs)")
	self.play = args[0] # Workaround for https://github.com/ansible/ansible/issues/13948
	self.loader = args[0]._loader

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.task = task
