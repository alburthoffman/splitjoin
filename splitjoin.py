import sublime, sublime_plugin

class SplitLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        curpos = self.view.sel()[0]
        curreg = self.view.line(curpos)
        linetxt = self.view.substr(curreg)
        self.view.replace(edit, curreg, "\n".join(linetxt.split()))

class JoinLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        curpos = self.view.sel()[0]
        curreg = self.view.line(curpos)
        linetxt = self.view.substr(curreg)
        self.view.replace(edit, curreg, " ".join(linetxt.split("\n")))