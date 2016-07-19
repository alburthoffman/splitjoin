import sublime, sublime_plugin
import re

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

class UniqLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        curpos = self.view.sel()[0]
        curreg = self.view.line(curpos)
        linetxt = self.view.substr(curreg)
        lines = linetxt.split("\n")
        keymap = {}
        for line in lines:
            keymap[line] = 1
        self.view.replace(edit, curreg, "\n".join(keymap.keys()))

class SortLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        curpos = self.view.sel()[0]
        curreg = self.view.line(curpos)
        linetxt = self.view.substr(curreg)
        lines = linetxt.split()
        lines.sort()
        self.view.replace(edit, curreg, "\n".join(lines))

class BlockSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, pattern = r"\s"):
        curpos = self.view.sel()[0]
        allregs = self.view.find_all(pattern)
        b = None
        e = None
        for idx in range(len(allregs) - 1):
            b = allregs[idx]
            e = allregs[idx + 1]
            if b.end() <= curpos.begin() and e.begin() >= curpos.end():
                break
        if b == None or e == None:
            return
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(b.end(), e.begin()))

class BlockPairSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, pattern1 = r"\s", pattern2 = r"\s"):
        #import spdb ; spdb.start();spdb.setbreak()
        curpos = self.view.sel()[0]
        patternRegs = self.view.find_all(pattern1 + "|" + pattern2)
        b = e = None
        # get the closest one
        for idx in range(len(patternRegs) - 1):
            nIdx = idx + 1
            if patternRegs[idx].end() <= curpos.begin() and patternRegs[nIdx].begin() >= curpos.end():
                b = idx
                e = nIdx
                break

        if b == None or e == None:
            sublime.error_message("No closest marthes.")
            return

        # find the unclosed one in the front
        count = 0
        firstPat = pattern2
        secondPat = pattern1
        delta = -1
        firstpos = b
        endpos = -1
        while firstpos != endpos:
            strAtPlace = self.view.substr(patternRegs[firstpos])
            if re.match(firstPat, strAtPlace):
                count = count + 1
            elif re.match(secondPat, strAtPlace):
                if count == 0:
                    b = firstpos
                    break
                count = count - 1
            firstpos = firstpos + delta 
        else:
            sublime.error_message("no matched begining pattern")
            return 

        # find the unclosed one in the end
        count = 0
        firstPat = pattern1
        secondPat = pattern2
        delta = 1
        firstpos = e
        endpos = len(patternRegs)
        while firstpos != endpos:
            strAtPlace = self.view.substr(patternRegs[firstpos])
            if re.match(firstPat, strAtPlace):
                count = count + 1
            elif re.match(secondPat, strAtPlace):
                if count == 0:
                    e = firstpos
                    break
                count = count - 1
            firstpos = firstpos + delta 
        else:
            sublime.error_message("no matched endding pattern")
            return           

        b = patternRegs[b]
        e = patternRegs[e]

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(b.end(), e.begin()))

class LinesColumnSelCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        curpos = self.view.sel()[0]
        curreg = self.view.line(curpos)
        linetxt = self.view.substr(curreg)
