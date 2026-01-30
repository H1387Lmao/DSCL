from enum import Enum
import sys
import re

COLORS = {
    "bold": 1,
    "dark": 2,
    "italic": 3,
    "underline":4,
    "semibold": 5, #looks like the same idk what this is
    "reset": 0,
    "reverse":7,
    "strikethrough":8,
    "black":30,
    "red":31,
    "green":32,
    "yellow":33,
    "gold": 93,
    "blue": 34,
    "purple":35,
    "violet":35,
    "pink": 95,
    "cyan":36,
    "gray":38,
    "grey":38,
    "white":39,
}

def Python(msg):
    tokens = []
    KEYWORDS=["None", "False", "True", "async", "def", "in", "for", "elif", "if", "while", "else", "await", "from", "import"]
    ct = ""
    cty = None
    capture_all=False
    for c in msg:
        if c == "\n":
            if ct in KEYWORDS:
                cty="keyword"
            tokens.append((ct,cty))
            ct=""
            cty=None
            capture_all=False
        if c in "(){}[]+-/*\\%&^=|: \n\t,.@#" and not capture_all:
            if ct:
                if ct in KEYWORDS:
                    tokens.append((ct, "keyword"))
                else:
                    tokens.append((ct,cty))
                cty=None
                ct=""
            if c in "@#":
                capture_all="#"
                cty="comment"
                ct+=c
            elif c in "+-/%*^=&|":
                tokens.append((c, "symbol"))
            else:
                tokens.append((c, "ignored"))
        elif c in "'\"" and capture_all!="#":
            ct+=c
            if cty is None:
                cty="string"
                capture_all="'"
            elif cty=="string":
                tokens.append((ct,cty))
                cty=None
                ct=""
                capture_all=False
        elif c.isdigit() and not capture_all:
            ct+=c
            if cty is None:
                cty="number"
        else:
            ct+=c
            if not capture_all:
                if ct in KEYWORDS:
                    cty="keyword"
                if c.isupper() and cty != "identifier":
                    cty="identifier.class"
                elif cty is None:
                    cty="identifier"

    if ct:
        if ct in KEYWORDS:
            tokens.append((ct, "keyword"))
        else:
            tokens.append((ct, cty))
    return tokens
class LogLevel(Enum):
    ERROR = "[[red]ERROR[reset]] "
    WARNING = "[[dark gold]WARNING[reset]] "
    LOG = "[[cyan]LOG[reset]] "

class Logger:
    def __init__(self, name="UnknownLogger"):
        self.last_color=None    
        self.enter_stage(name)

        self.no_colors=False
    def enter_stage(self, name):
        self.name=name
        self.errors = 0
    def colorize(self, text):
        return re.sub(r"\[([^\]\[]+)\]", self._tag, text)
    def exit_stage(self):
        if self.errors > 0:
            self.print(f"[red]Failed at stage: '{self.name}'[?]")
            sys.exit(-1)
    def log(self, loglevel, msg):
        if loglevel.name=="ERROR":
            self.errors+=1
        print(self.colorize(loglevel.value+msg))
    def error(self, msg):
        self.log(LogLevel.ERROR, msg)
    def print(self, msg):
        print(self.colorize(msg))

    def print_code(self, msg, tokenizer=Python):
        res=""
        for token in tokenizer(msg):
            match(token[1]):
                case "string":
                    res+="[green]"+token[0]+"[?]"
                case "symbol":
                    res+="[bold light cyan]"+token[0]+"[?]"
                case "number":
                    res+="[cyan]"+token[0]+"[?]"
                case "identifier.class":
                    res+="[yellow]"+token[0]+"[?]"
                case "keyword":
                    res+="[purple]"+token[0]+"[?]"
                case "comment":
                    res+="[dark gray]"+token[0]+"[?]"
                case _:
                    res+=token[0]
        self.print(res)
    def _tag(self, m):
        res = []
        self.light=0
        tag=m.group(0)[1:-1]
        styles = tag.split(" ")
        for style in styles:
            style=style.lower()
            if style == "?":
                style="reset"
            if style == "light":
                self.light+=60
            if style == "bg":
                self.light+=10
            if style not in "bglight":
                color = COLORS.get(style)
                if color is None:
                    return m.group(0)
                color+=self.light
                self.light=0
                res.append(color)
        else:
            if self.no_colors:
                return ""
            self.last_color = "\033["+";".join(map(str,res))+"m"
            return self.last_color

if __name__=="__main__":
    test=Logger("Test Logger")
    test.log(LogLevel.ERROR, "hi")

    test.exit_stage()
