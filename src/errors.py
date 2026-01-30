from .hlog import Logger, LogLevel

def try_rel(l, pos):
    if not hasattr(l, "file"):
        return "Position: "+str(pos)
    stripped = l.file[:(pos+1)]

    col=0
    for c in stripped:
        if c == "\n":
            col=0
        else:
            col+=1
    return "Column: "+str(col)
    

class BaseException:
    def __init__(self, n, logger, msg, lineno=None, pos=None):
        if pos is not None:
            rel = try_rel(logger, pos)
        v = f"\n[cyan]  Located at Line: {lineno}, {rel}[?]" if lineno is not None and pos is not None else ""
        logger.log(LogLevel.ERROR, f"{n}: {msg}{v}")

class SyntaxError(BaseException):
    def __init__(self, *kwargs):
        super().__init__("Syntax Error", *kwargs)

class LexerError(BaseException):
    def __init__(self, *kwargs):
        super().__init__("Lexer Error", *kwargs)
