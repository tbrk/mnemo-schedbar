##############################################################################
#
# schedbar.py <timbob@bigpond.com>
#
# Show the upcoming schedules in the status bar.
#
# Some options can be added to $HOME/.mnemosyne/config.py:
#   plugin_schedbar = {
#	'show_in_days' = 3	    # show schedule counts for next n days
#				    # 0 <= n
#   }
#
# 1.0.1
#   * Fix the calculation of tomorrow's scheduled cards.
#
##############################################################################

from mnemosyne.core import *
from mnemosyne.pyqt_ui.plugin import get_main_widget
from qt import *
import sys
from datetime import date
from calendar import day_abbr

class SchedBar(Plugin):
    version = "1.0.1"

    def description(self):
	return ("Show future schedule in the status bar. (v" + version + ")")

    def load(self):
	try: self.options = get_config("plugin_schedbar")
	except KeyError:
	    self.options = {}
	    set_config("plugin_schedbar", {})

	if type(self.options) != type({}):
	    self.options = {}
	
	self.show_sched = 3
	if self.options.has_key('show_in_days'):
	    self.show_sched = min(max(0, self.options['show_in_days']), 7)

	self.today = date.today().weekday()
	self.main_dlg = get_main_widget()
	status_bar = self.main_dlg.statusBar() 

	self.widgets = []

	if self.show_sched > 0:
	    self.schedbar_indays = QLabel("", status_bar)
	    self.widgets.append(self.schedbar_indays)
        
	for w in self.widgets:
	    status_bar.addWidget(w, 0, 1)

	register_function_hook("filter_q", self.set_schedbar)

    def unload(self):
	for w in self.widgets:
	    w.parent().removeChild(w)
	    del w

	unregister_function_hook("filter_q", self.set_schedbar)

    def set_schedbar(self, text, card):
	if self.show_sched == 0: return text

	totals = []
        old_cumulative = scheduled_items(0)
        for days in range(1,self.show_sched + 1):
            cumulative = scheduled_items(days)
	    totals.append(day_abbr[(self.today + days) % 7]
			  + ': ' + str(cumulative - old_cumulative))
            old_cumulative = cumulative

	self.schedbar_indays.setText(QString(' '.join(totals)))

	return text

p = SchedBar()
p.load()

