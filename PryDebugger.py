import sublime, sublime_plugin
import os
import subprocess
from tempfile import SpooledTemporaryFile as tempfile

class ToggleBreakpointCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for selection in self.view.sel():
			(row,col) = self.view.rowcol(selection.begin())
			point = self.view.text_point(row, 0)
			self.view.insert(edit, point, "biding.remote_pry\n")

class PanelOutput:
	def __init__(self, panel):
		self.panel = panel
		self.tempfile = tempfile()
		self.fileno = self.tempfile.fileno
	def write(self, string):
		edit = self.panel.begin_edit()
		self.panel.insert(edit, self.panel.size(), string)
		self.panel.end_edit(edit)
		self.panel.show(self.panel.size())

class OpenDebuggerCommand(sublime_plugin.WindowCommand):
	def run(self):
		panel = self.window.get_output_panel('debugger')
		panel.settings().set('word_wrap', False)
		panel.set_name('Pry Debugger')
		self.output = PanelOutput(panel)
		self.output.write('bosta')
		self.window.run_command('show_panel', {'panel': 'output.debugger'})
		process = subprocess.Popen(['rbenv', 'exec', 'pry-remote'], stdin=subprocess.PIPE,
													stdout=self.output)
		self.output.write("return: %s pid: %s\n" % (process.returncode, process.pid))
		output, err = process.communicate()
		self.output.write("return: %s pid: %s\n" % (process.returncode, process.pid))