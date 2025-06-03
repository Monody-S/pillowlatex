from PIL import Image, ImageFont, ImageDraw
from typing import Callable, Union, Sequence, Optional, Any
from PIL.ImageFont import FreeTypeFont
import math

from .import settings

df_font = ImageFont.truetype(settings.FONT_PATH, 50)
SPACE = settings.SPACE

class LaTexReplace:
    def __init__(self, key: str, after: str):
        self.key: str = key
        self.after: str = after

class LaTexFunc:
    def __init__(
        self, 
        key: str, 
        nonenum: int, 
        nosmaller: bool, 
        needDeep: bool, 
        needFont: bool, 
        needColor: bool,
        autoRender: bool,
        func: Callable[..., "LaTexImage"]
    ):
        self.key: str = key
        self.func = func
        self.nonenum: int = nonenum
        self.nosmaller: bool = nosmaller
        self.needDeep: bool = needDeep
        self.needFont: bool = needFont
        self.needColor: bool = needColor

        self.autoRender: bool = autoRender

        self.argsTypes: list[type] = []

        for arg in func.__code__.co_varnames[:func.__code__.co_argcount]:
            if arg == "self":
                continue
            self.argsTypes.append(type(arg))

    def Render(self, *args, **kwargs) -> "LaTexImage":
        return self.func(*args, **kwargs)

class LaTexEnvFunc:
    def __init__(
        self, 
        key: str, 
        needFont: bool, 
        needColor: bool,
        func: Callable[..., "LaTexImage"]
    ):
        self.key: str = key
        self.func = func
        self.needFont: bool = needFont
        self.needColor: bool = needColor

        self.argsTypes: list[type] = []

        for arg in func.__code__.co_varnames[:func.__code__.co_argcount]:
            if arg == "self":
                continue
            self.argsTypes.append(type(arg))

    def Render(self, *args, **kwargs) -> "LaTexImage":
        return self.func(*args, **kwargs)

def DeepToK(deep: int) -> float:
    return max(0.5, 1-deep *0.2)

class LaTexImage:
    def __init__(self, img: Image.Image, space: int = SPACE, raw_size: Optional[tuple[int, int]] = None):
        out = Image.new("RGBA", (img.width+space*2, img.height+space*2), (255, 255, 255, 0))

        out.alpha_composite(img, (space, space))

        self.img = out
        self.space = space
        self.box = out.size
        self.size = img.size

        self.width: int = img.size[0]
        self.height: int = img.size[1]

        self.raw_size: tuple[int, int] = raw_size if raw_size else (img.width, img.height)
        self.min_size: float = 0.5

        self.kmove: int = 0
        self.img_type: str = "normal"

    def resize_with_deep(self, deep: int) -> "LaTexImage":
        k = DeepToK(deep)
        return self.resize((int(self.width * k), int(self.height * k)))
    
    def resize_with_k(self, k: float) -> "LaTexImage":
        """
        根据缩放因子调整图像大小
        :param k: 缩放因子
        :return: 调整后的 LaTexImage 对象
        """
        x = int(k * self.width)
        y = int(k * self.height)
        return self.resize((x, y))

    def resize(self, size: tuple[int, int]) -> "LaTexImage":
        """
        调整图像大小
        :param size: 新的大小 (width, height)
        :return: 调整后的 LaTexImage 对象
        """
        raw = self.img.crop((self.space, self.space, self.width + self.space, self.height + self.space))
        x = int(max(1, max(self.min_size * self.raw_size[0], size[0])))
        y = int(max(1, max(self.min_size * self.raw_size[1], size[1])))
        resized_img = raw.resize((x, y))
        return LaTexImage(resized_img, self.space, self.raw_size)

    def alpha_composite(self, other: "LaTexImage", position: tuple[int, int]) -> None:
        """
        将另一个 LaTexImage 对象合成到当前图像上
        :param other: 另一个 LaTexImage 对象
        :param position: 合成位置 (x, y)
        """
        self.img.alpha_composite(other.img, position)

        # draw = LaTexImageDraw.Draw(self)
        # draw.rectangle(
        #     (position[0], position[1], position[0] + other.width, position[1] + other.height),
        #     outline = (0,0,0)
        # )

    def show(self) -> None:
        """
        显示当前图像
        """
        self.img.show()

    @classmethod
    def new(cls, size: tuple[int, int], color: Union[str, tuple[int, int, int, int], tuple[int, int, int]] = (255, 255, 255, 0), space: int = SPACE):
        return cls(Image.new("RGBA", size, color), space)

class LaTexImageDraw:
    def __init__(self, img: LaTexImage):
        self.draw = ImageDraw.Draw(img.img)
        self.img = img
    
    def text(self, xy: tuple[float, float], text: str, fill=None, font: ImageFont.ImageFont | FreeTypeFont | ImageFont.TransposedFont | None = None, anchor=None, spacing=4, align="left", direction=None, features=None, language=None, stroke_width=0, stroke_fill=None, embedded_color=False, *args, **kwargs) -> None:
        return self.draw.text((xy[0]+self.img.space, xy[1]+self.img.space), text, fill, font, anchor, spacing, align, direction, features, language, stroke_width, stroke_fill, embedded_color, *args, **kwargs)

    def line(self, xy: Sequence[float], fill=None, width=1, joint=None) -> None:
        xy = [xy[0] + self.img.space, xy[1] + self.img.space, xy[2] + self.img.space, xy[3] + self.img.space]
        return self.draw.line(xy, fill, width, joint)
    
    def ellipse(self, xy: Sequence[float], fill=None, outline=None, width=1) -> None:
        xy = [xy[0] + self.img.space, xy[1] + self.img.space, xy[2] + self.img.space, xy[3] + self.img.space]
        return self.draw.ellipse(xy, fill, outline, width)
    
    def rectangle(self, xy: Sequence[float], fill=None, outline=None, width=1) -> None:
        xy = [xy[0] + self.img.space, xy[1] + self.img.space, xy[2] + self.img.space, xy[3] + self.img.space]
        return self.draw.rectangle(xy, fill, outline, width)
    
    @classmethod
    def Draw(cls, img: LaTexImage) -> "LaTexImageDraw":
        return cls(img)

funcs: list[LaTexFunc] = []
    
def RegisterLaTexFunc(
    key: str, 
    nonenum: int=0, 
    nosmaller: bool=False, 
    needDeep: bool = False, 
    needFont: bool = False, 
    needColor: bool = False,
    autoRender: bool = True
) -> Callable[[Callable[..., LaTexImage]], LaTexFunc]:
    def decorator(func: Callable[..., LaTexImage]) -> LaTexFunc:
        latex_func = LaTexFunc(key, nonenum, nosmaller, needDeep, needFont, needColor, autoRender, func)
        funcs.append(latex_func)
        return latex_func
    return decorator

env_funcs: dict[str, LaTexEnvFunc] = {}

def RegisterLaTexEnvFunc(key: str, needFont: bool = False, needColor: bool = False) -> Callable[[Callable[..., LaTexImage]], LaTexEnvFunc]:
    def decorator(func: Callable[..., LaTexImage]) -> LaTexEnvFunc:
        latex_env_func = LaTexEnvFunc(key, needFont, needColor, func)
        env_funcs[key] = latex_env_func
        return latex_env_func
    return decorator

middle_lowandpows = [
    "sideset",
    "lim",
    "max",
    "min",
    "limits",
]

auto_middle_replaces = [
    "sum",
    "prod",
    "coprod",
    "bigcap",
    "bigcup",
    "bigvee",
    "bigwedge",
]

big_replaces = [
    "sum",
    "prod",
    "coprod",
    "bigcap",
    "bigcup",
    "bigvee",
    "bigwedge",
]

high_replaces = [
    "int",
    "iint",
    "iiint",
    "oint"
]

ex_replaces = [
    "|",
    "\\",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}"
]

replaces: dict[str, str] = {

    "mathbf": "",
    "mathbb": "",

    "tiny": "",
    "scriptsize": "",
    "footnotesize": "",
    "small": "",
    "normalsize": "",
    "large": "",
    "Large": "",
    "LARGE": "",
    "huge": "",
    "Huge": "",

    "limits": "",
    "left": "",
    "right": "",
    "begin": "",
    "end": "",
    "ce": "",

    "mathop": "",
    "nolimits": "",

    "unicode": "",

    "|": "∥",
    "\\": "",
    "(": "(",
    ")": ")",
    "[": "[",
    "]": "]",
    "{": "{",
    "}": "}",

    "lt": "<",
    "gt": ">",
    "leq": "≤",
    "geq": "≥",
    "neq": "≠",

    "bmod": "mod",
    "gcd": "gcd",
    "lim": "lim",
    "max": "max",
    "min": "min",
    "log": "log",
    "ln": "ln",
    "lg": "lg",
    "exp": "exp",
    "sup": "sup",
    "inf": "inf",
    "lim": "lim",
    "limsup": "lim sup",
    "liminf": "lim inf",
    "dim": "dim",
    "ker": "ker",

    "int": "∫",
    "iint": "∬",
    "iiint": "∭",
    "oint": "∮",
    "sum": "∑",
    "prod": "∏",
    "coprod": "∐",
    "bigcap": "⋂",
    "bigcup": "⋃",
    "bigvee": "⋁",
    "bigwedge": "⋀",

    "lfloor": "⌊",
    "rfloor": "⌋",
    "lceil": "⌈",
    "rceil": "⌉",
    "langle": "⟨",
    "rangle": "⟩",

    "to": "→",

    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "cot": "cot",
    "sec": "sec",
    "csc": "csc",
    "arcsin": "arcsin",
    "arccos": "arccos",
    "arctan": "arctan",
    "arccot": "arccot",
    "arcsec": "arcsec",
    "arccsc": "arccsc",
    "sinh": "sinh",
    "cosh": "cosh",
    "tanh": "tanh",
    "coth": "coth",
    "sech": "sech",
    "csch": "csch",

    "times": "×",
    "div": "÷",
    "pm": "±",
    "mp": "∓",
    "triangleleft": "◁",
    "triangleright": "▷",
    "cdot": "⋅",
    "setminus": "∖",
    "star": "★",
    "ast": "∗",
    "cup": "∪",
    "cap": "∩",
    "sqcup": "⊔",
    "sqcap": "⊓",
    "vee": "∨",
    "wedge": "∧",
    "circ": "○",
    "bullet": "•",
    "oplus": "⊕",
    "omuinus": "⊖",
    "odot": "⊙",
    "oslash": "⊘",
    "otimes": "⊗",
    "bigcirc": "◯",
    "diamond": "◇",
    "uplus": "⊎",
    "bigtriangleup": "△",
    "bigtriangledown": "▽",
    "lhd": "⊲",
    "rhd": "⊳",
    "unlhd": "⊴",
    "unrhd": "⊵",
    "amalg": "⨿",
    "wr": "≀",
    "dagger": "†",
    "ddagger": "‡",
    "le": "≤",
    "ge": "≥",
    "equiv": "≡",
    "ll": "≪",
    "gg": "≫",
    "doteq": "≐",
    "prec": "≺",
    "succ": "≻",
    "sim": "∼",
    "preceq": "≼",
    "succeq": "≽",
    "simeq": "≃",
    "approx": "≈",
    "subset": "⊂",
    "supset": "⊃",
    "subseteq": "⊆",
    "supseteq": "⊇",
    "sqsubset": "⊏",
    "sqsupset": "⊐",
    "sqsubseteq": "⊑",
    "sqsupseteq": "⊒",
    "cong": "≅",
    "join": "⋈",
    "bowtie": "⋈",
    "propto": "∝",
    "in": "∈",
    "ni": "∋",
    "vdash": "⊢",
    "dashv": "⊣",
    "models": "⊨",
    "mid": "∣",
    "parallel": "∥",
    "perp": "⊥",
    "smile": "⌣",
    "frown": "⌢",
    "asymp": "≍",
    "notin": "∉",
    "ne": "≠",

    "gets": "←",
    "to": "→",
    "longleftarrow": "⟵",
    "longrightarrow": "⟶",
    "uparrow": "↑",
    "downarrow": "↓",
    "updownarrow": "↕",
    "leftrightarrow": "↔",
    "Uparrow": "⇑",
    "Downarrow": "⇓",
    "Updownarrow": "⇕",
    "longleftrightarrow": "⟷",
    "Leftarrow": "⇐",
    "Longleftarrow": "⟸",
    "Rightarrow": "⇒",
    "Longrightarrow": "⟹",
    "Leftrightarrow": "⇔",
    "Longleftrightarrow": "⟺",
    "mapsto": "↦",
    "longmapsto": "⟼",
    "nearrow": "↗",
    "searrow": "↘",
    "swarrow": "↙",
    "nwarrow": "↖",
    "hookleftarrow": "↩",
    "hookrightarrow": "↪",
    "rightleftharpoons": "⇌",
    "iff": "⇔",
    "leftharpoonup": "↼",
    "leftharpoondown": "↽",
    "rightharpoonup": "⇀",
    "rightharpoondown": "⇁",

    "because": "∵",
    "therefore": "∴",
    "dots": "…",
    "cdots": "⋯",
    "vdots": "⋮",
    "ddots": "⋱",
    "forall": "∀",
    "exists": "∃",
    "nexists": "∄",
    "Finv": "Ⅎ",
    "neg": "¬",
    "prime": "′",
    "emptyset": "∅",
    "infty": "∞",
    "nabla": "∇",
    "triangle": "△",
    "Box": "□",
    "Diamond": "◇",
    "bot": "⊥",
    "top": "⊤",

    "angle": "∠",
    "measuredangle": "∡",
    "sphericalangle": "∢",
    "surd": "√",
    "diamondsuit": "♢",
    "heartsuit": "♡",
    "clubsuit": "♣",
    "spadesuit": "♠",
    "flat": "♭",
    "natural": "♮",
    "sharp": "♯",


    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "delta": "δ",
    "epsilon": "ε",
    "varepsilon": "ϵ",
    "zeta": "ζ",
    "eta": "η",
    "theta": "θ",
    "vartheta": "ϑ",
    "iota": "ι",
    "kappa": "κ",
    "lambda": "λ",
    "mu": "μ",
    "nu": "ν",
    "xi": "ξ",
    "pi": "π",
    "varpi": "ϖ",
    "rho": "ρ",
    "varrho": "ϱ",
    "sigma": "σ",
    "varsigma": "ς",
    "tau": "τ",
    "upsilon": "υ",
    "phi": "φ",
    "varphi": "ϕ",
    "chi": "χ",
    "psi": "ψ",
    "omega": "ω",

    "Gamma": "Γ",
    "Delta": "Δ",
    "Theta": "Θ",
    "Lambda": "Λ",
    "Xi": "Ξ",
    "Pi": "Π",
    "Sigma": "Σ",
    "Upsilon": "Υ",
    "Phi": "Φ",
    "Psi": "Ψ",
    "Omega": "Ω",

    "hbar": "ℏ",
    "imath": "ı",
    "jmath": "ȷ",
    "ell": "ℓ",
    "Re": "ℜ",
    "Im": "ℑ",
    "aleph": "ℵ",
    "beth": "ℶ",
    "gimel": "ℷ",
    "delta": "ℸ",
    "wp": "℘",
    "mho": "℧",
    "backepsilon": "϶",
    "partial": "∂",
    "eth": "ð",
    "Bbbk": "𝕜",
    "complement": "∁",
    "circledS": "Ⓢ",
    "S": "§",
}


def lt_pow(a: LaTexImage, b: LaTexImage) -> LaTexImage:

    height = a.height
    b = b.resize((b.width * 2 // 3, b.height * 2 // 3))

    height = max(height, b.height * 2)

    new = LaTexImage.new((b.width, height))

    new.alpha_composite(b, (0, 0))
    
    return new

def lt_low(a: LaTexImage, b: LaTexImage) -> LaTexImage:

    height = a.height
    b = b.resize((b.width * 2 // 3, b.height * 2 // 3))

    height = max(height, b.height * 2)

    new = LaTexImage.new((b.width, height))

    new.alpha_composite(b, (0, height - b.height))
    
    return new

# def lt_cexrightarrow(a: Optional[LaTexImage], b: Optional[LaTexImage], font: FreeTypeFont, color) -> LaTexImage:
#     k = GetFontSize(font, "a")[0]
#     height = int(font.size)

#     if not a:
#         a = LaTexImage.new((1, 1), (255, 255, 255, 0))
#     if not b:
#         b = LaTexImage.new((1, 1), (255, 255, 255, 0))
    
#     ms = GetFontSize(font, "⏞")[0]*3

#     new = LaTexImage.new((max(a.width, b.width, ms) + k*2, max(a.height, b.height) * 2 + height), (255, 255, 255, 0))

#     new.alpha_composite(a, ((new.width - a.width) // 2, int(new.height // 2 - height // 2 - a.height)))
#     new.alpha_composite(b, ((new.width - b.width) // 2, int(new.height // 2 + height // 2)))

#     mid = new.height // 2
#     ak = math.ceil(font.size / 5)
#     l = math.ceil(GetFontSize(font, "⏞")[0] // 2)
#     draw = LaTexImageDraw.Draw(new)
#     ls = math.ceil(font.size / 20)

#     for line in [
#         (0, mid, new.width, mid),
#         (new.width, mid, new.width - ak, mid + l), (new.width, mid, new.width - ak, mid - l)
#     ]:
#         draw.line(line, fill=color, width=ls)

#     return new

# ltf_cexrightarrow = LaTexFunc(
#     "cexrightarrow",
#     nonenum=2,
#     nosmaller=True,
#     needDeep=False,
#     needFont=True,
#     needColor=True,
#     func=lt_cexrightarrow
# )

# def lt_cexleftarrow(a: Optional[LaTexImage], b: Optional[LaTexImage], font: FreeTypeFont, color) -> LaTexImage:
#     k = GetFontSize(font, "a")[0]
#     height = int(font.size)

#     if not a:
#         a = LaTexImage.new((1, 1), (255, 255, 255, 0))
#     if not b:
#         b = LaTexImage.new((1, 1), (255, 255, 255, 0))
    
#     ms = GetFontSize(font, "⏞")[0]*3

#     new = LaTexImage.new((max(a.width, b.width, ms) + k*2, max(a.height, b.height) * 2 + height), (255, 255, 255, 0))

#     new.alpha_composite(a, ((new.width - a.width) // 2, int(new.height // 2 - height // 2 - a.height)))
#     new.alpha_composite(b, ((new.width - b.width) // 2, int(new.height // 2 + height // 2)))

#     mid = new.height // 2
#     ak = math.ceil(font.size / 5)
#     l = math.ceil(GetFontSize(font, "⏞")[0] // 2)
#     draw = LaTexImageDraw.Draw(new)
#     ls = math.ceil(font.size / 20)

#     for line in [
#         (0, mid, new.width, mid),
#         (0, mid, 0 + ak, mid + l), (0, mid, 0 + ak, mid - l)
#     ]:
#         draw.line(line, fill=color, width=ls)

#     return new

# ltf_cexleftarrow = LaTexFunc(
#     "cexleftarrow",
#     nonenum=2,
#     nosmaller=True,
#     needDeep=False,
#     needFont=True,
#     needColor=True,
#     func=lt_cexleftarrow
# )

# def lt_cexleftrightarrow(a: Optional[LaTexImage], b: Optional[LaTexImage], font: FreeTypeFont, color) -> LaTexImage:
#     k = GetFontSize(font, "a")[0]
#     height = int(font.size)

#     if not a:
#         a = LaTexImage.new((1, 1), (255, 255, 255, 0))
#     if not b:
#         b = LaTexImage.new((1, 1), (255, 255, 255, 0))
    
#     ms = GetFontSize(font, "⏞")[0]*3

#     new = LaTexImage.new((max(a.width, b.width, ms) + k*2, max(a.height, b.height) * 2 + height), (255, 255, 255, 0))

#     new.alpha_composite(a, ((new.width - a.width) // 2, int(new.height // 2 - height // 2 - a.height)))
#     new.alpha_composite(b, ((new.width - b.width) // 2, int(new.height // 2 + height // 2)))

#     mid = new.height // 2
#     ak = math.ceil(font.size / 5)
#     l = math.ceil(GetFontSize(font, "⏞")[0] // 2)
#     draw = LaTexImageDraw.Draw(new)
#     ls = math.ceil(font.size / 20)

#     for line in [
#         (0, mid, new.width, mid),
#         (0, mid, 0 + ak, mid + l), (0, mid, 0 + ak, mid - l),
#         (new.width, mid, new.width - ak, mid + l), (new.width, mid, new.width - ak, mid - l)
#     ]:
#         draw.line(line, fill=color, width=ls)

#     return new

# ltf_cexleftrightarrow = LaTexFunc(
#     "cexleftrightarrow",
#     nonenum=2,
#     nosmaller=True,
#     needDeep=False,
#     needFont=True,
#     needColor=True,
#     func=lt_cexleftrightarrow
# )

# def lt_cexdoubleleftrightarrow(a: Optional[LaTexImage], b: Optional[LaTexImage], font: FreeTypeFont, color) -> LaTexImage:
#     k = GetFontSize(font, "a")[0] * 2
#     height = int(font.size)

#     if not a:
#         a = LaTexImage.new((1, 1), (255, 255, 255, 0))
#     if not b:
#         b = LaTexImage.new((1, 1), (255, 255, 255, 0))
    
#     ms = GetFontSize(font, "⏞")[0]*3

#     new = LaTexImage.new((max(a.width, b.width, ms) + k*2, max(a.height, b.height) * 2 + height), (255, 255, 255, 0))

#     new.alpha_composite(a, ((new.width - a.width) // 2, int(new.height // 2 - height // 2 - a.height)))
#     new.alpha_composite(b, ((new.width - b.width) // 2, int(new.height // 2 + height // 2)))

#     kk = new.height // 4
#     ak = math.ceil(font.size / 5)
#     l = math.ceil(GetFontSize(font, "⏞")[0] // 2)
#     draw = LaTexImageDraw.Draw(new)
#     ls = math.ceil(font.size / 20)

#     for line in [
#         (0, kk, new.width, kk),
#         (0, kk*3, new.width, kk*3),
#         (0, kk*3, 0 + ak, kk*3 + l),
#         (new.width, kk, new.width - ak, kk + l)
#     ]:
#         draw.line(line, fill=color, width=ls)

#     return new

# ltf_cexdoubleleftrightarrow = LaTexFunc(
#     "cexdoubleleftrightarrow",
#     nonenum=2,
#     nosmaller=True,
#     needDeep=False,
#     needFont=True,
#     needColor=True,
#     func=lt_cexdoubleleftrightarrow
# )

def GetFontSize(font:FreeTypeFont,string: str) -> tuple[int, int]:
    """
    获取字符串在指定字体下的大小
    :param font: 字体对象
    :param string: 字符串
    :return: 字符串的宽度和高度
    """
    box = font.getbbox(string)
    width = box[2] - box[0]
    height = box[3] - box[1]
    print(width, height)
    return int(width), int(height)

def GetLaTexTextObj(objs: Union[str, list, Any]) -> Optional[str]:
    if isinstance(objs, str):
        return objs
    elif isinstance(objs, list):
        return "".join(objs) if all(isinstance(i, str) for i in objs) else None
    else:
        return None

def RenderLaTexObjs(
    objs: Union[str, list], 
    deep: int = 0, 
    include: bool = False,
    font: FreeTypeFont = df_font,
    color: Optional[Union[str, tuple[int, int, int, int], tuple[int, int, int]]] = None
) -> list[LaTexImage]:
    """
    渲染LaTeX对象列表
    :param objs: LaTeX对象列表
    :return: 渲染后的图像
    """

    if not color:
        color = (0, 0, 0, 255)

    if not isinstance(objs, list):
        objs = [objs]

    idx = 0
    sz = len(objs)
    imgs: list[LaTexImage] = []

    while idx < sz:
        obj = objs[idx]
        if isinstance(obj, LaTexFunc):

            fill = []

            while len(fill) < obj.nonenum and idx + 1 < sz and objs[idx+1] == "[":
                tempidx = idx + 2
                while tempidx < sz and objs[tempidx] != "]":
                    tempidx += 1
                if tempidx < sz and objs[tempidx] == "]":
                    fill.append(objs[idx + 2: tempidx])
                    idx = tempidx

            exargs = []
            if obj.needDeep:
                exargs.append(deep)
            if obj.needFont:
                exargs.append(font)
            if obj.needColor:
                exargs.append(color)

            args = objs[idx + 1:idx + 1 + len(obj.argsTypes) - obj.nonenum - len(exargs)]

            print(obj.key, args)

            if len(args) != len(obj.argsTypes) - (1 if obj.nonenum else 0) - len(exargs):
                print(len(args) , len(obj.argsTypes) - (1 if obj.nonenum else 0) - len(exargs))
                print("warning: LaTeX function argument count mismatch for", obj.key)
            else:
                try:
                    input_args = []
                    if obj.nonenum:
                        input_args.extend([None] * (obj.nonenum - len(fill)) + fill)
                    input_args.extend(args)
                    img = obj.Render(*[
                        (RenderLaTex(i, (deep if obj.nosmaller else deep + 1), include or not obj.nosmaller, font, color) if not i is None else None )
                        
                        if obj.autoRender else i
                        
                        for i in input_args
                    ]+exargs)
                    imgs.append(img)
                    idx += len(args) + 1
                    img.img_type = obj.key

                    if obj.key == "sideset":
                        img.kmove = img.width // 2

                    continue
                except Exception as e:
                    print(f"Error rendering LaTeX function '{obj.key}': {e}")
        elif isinstance(obj, LaTexReplace):
            print("replace", obj.key, obj.after)
            img = RenderLaTex(obj.after, deep, include, font, color)
            if obj.key in big_replaces:
                img = img.resize((img.width * 2, img.height * 2))
            elif obj.key in high_replaces:
                img = img.resize((img.width, img.height * 2))

            if obj.key == "limits" and imgs:
                imgs[-1].img_type = "limits"

            elif obj.key == "begin":
                k = 1
                if not idx + 1 < sz:
                    print("warning0")
                    idx += 1
                    continue

                lefta = GetLaTexTextObj(objs[idx + 1])

                if lefta not in env_funcs:
                    print("warning5")
                    idx += 1
                    continue

                temp_idx = idx + 2

                while temp_idx < sz:
                    tobj = objs[temp_idx]
                    print(tobj)
                    if isinstance(tobj, LaTexReplace) and tobj.key == "end" and temp_idx + 1 < sz and GetLaTexTextObj(objs[temp_idx + 1]) == lefta:
                        k -= 1
                        if k == 0:
                            break
                    elif isinstance(tobj, LaTexReplace) and tobj.key == "begin" and temp_idx + 1 < sz and GetLaTexTextObj(objs[temp_idx + 1]) == lefta:
                        k += 1
                    temp_idx += 1
                
                if not temp_idx < sz or k != 0:
                    print(temp_idx < sz)
                    print("warning6")
                    idx += 1
                    continue
                    
                if isinstance(objs[temp_idx], LaTexReplace) and objs[temp_idx].key == "end" and temp_idx + 1 < sz and GetLaTexTextObj(objs[temp_idx + 1]) == lefta:
                    theobjs = [[]]
                    nowobjs = []

                    exagrs = []

                    ex = 2
                    if lefta == "array":
                        if idx + 2 < sz and isinstance(objs[idx + 2], str) and objs[idx + 2] in ["c", "l", "r"]:
                            exargs.append(objs[idx + 2])
                        ex += 1

                    tidx = idx + ex
                    while tidx < temp_idx:
                        i = objs[tidx]
                        if i == "&":
                            theobjs[-1].append(RenderLaTex(nowobjs, deep, include, font, color))
                            nowobjs = []
                        elif isinstance(i, LaTexReplace) and i.key == "\\":
                            theobjs[-1].append(RenderLaTex(nowobjs, deep, include, font, color))
                            theobjs.append([])
                            nowobjs = []

                        else:
                            nowobjs.append(i)
                        
                        tidx += 1

                    if nowobjs:                    
                        theobjs[-1].append(RenderLaTex(nowobjs, deep, include, font, color))

                    exargs = []
                    if env_funcs[lefta].needFont:
                        exargs.append(font)
                    if env_funcs[lefta].needColor:
                        exargs.append(color)

                    if not theobjs[-1]:
                        del theobjs[-1]
                    
                    img = env_funcs[lefta].Render(*[theobjs]+exargs)
                    imgs.append(img)
                    img.img_type = lefta

                    idx = temp_idx + 2
                    continue


            elif obj.key == "left":
                k = 1
                if not idx + 1 < sz:
                    print("warning1")
                    idx += 1
                    continue
                lefta = objs[idx + 1]
                temp_idx = idx + 2
                print("lefta", lefta)
                while temp_idx < sz:
                    tobj = objs[temp_idx]
                    print(tobj)
                    if isinstance(tobj, LaTexReplace) and tobj.key == "right":
                        k -= 1
                        if k == 0:
                            break
                    elif isinstance(tobj, LaTexReplace) and tobj.key == "left":
                        k += 1
                    temp_idx += 1
                print(k)
                if not temp_idx < sz or k != 0:
                    print(temp_idx < sz)
                    print("warning2")
                    idx += 1
                    continue

                if isinstance(objs[temp_idx], LaTexReplace) and objs[temp_idx].key == "right":
                    if not temp_idx + 1 < sz:
                        print("warning3")
                        idx += 1
                        continue
                    righta = objs[temp_idx + 1]
                    if not (isinstance(righta, str) or isinstance(righta, LaTexReplace) and righta.key in ex_replaces) or not (isinstance(lefta, str) or isinstance(lefta, LaTexReplace) and lefta.key in ex_replaces):
                        print(lefta, righta, "rl")
                        print("warning4")
                        idx += 1
                        continue
                    
                    img1 = RenderLaTex([lefta], deep, include, font, color) if lefta != "." else LaTexImage.new((1, 1))
                    img2 = RenderLaTex([righta], deep, include, font, color) if righta != "." else LaTexImage.new((1, 1))
                    middles = RenderLaTex(objs[idx + 2:temp_idx], deep, include, font, color)
                    new = LaTexImage.new((img1.width + img2.width + middles.width, max(img1.height, img2.height, middles.height)), (255, 255, 255, 0))
                    img1 = img1.resize((img1.width, new.height))
                    img2 = img2.resize((img2.width, new.height))
                    
                    img1.img_type = "left"
                    img2.img_type = "right"

                    imgs.extend([img1, middles, img2])
                    idx = temp_idx + 2
                    continue

            elif obj.key == "unicode":
                if idx + 1 < sz:
                    code = GetLaTexTextObj(objs[idx + 1])
                    if code and code.isdigit():
                        try:
                            char = chr(int(code))
                        except:
                            print(f"Invalid Unicode code point: {code}")
                            char = ""
                        img = RenderLaTex(char, deep, include, font, color)
                        imgs.append(img)
                    idx += 2
                else:
                    print("warning7")
                    idx += 1
                continue

            else:
                imgs.append(img)
                img.img_type = obj.key

            

        elif obj == "^":
            if idx + 1 < sz:
                base = imgs[-1] if imgs else LaTexImage.new((1, int(font.size*DeepToK(deep))), (255, 255, 255, 0))
                exponent = RenderLaTex(objs[idx + 1], deep, True, font, color)

                print("base",base.size)

                if base.img_type == "low":
                    img = lt_pow(base, exponent)
                    new = LaTexImage.new((max(base.width, img.width), max(base.height, img.height)), (255, 255, 255, 0))
                    new.alpha_composite(base, (0, (new.height - base.height) // 2))
                    new.alpha_composite(img, (0, (new.height - img.height) // 2))
                    imgs[-1] = new
                elif base.img_type in middle_lowandpows or (base.img_type in auto_middle_replaces and deep == 0 and not include):
                    img = exponent.resize_with_k(2/3)
                    new = LaTexImage.new((max(base.width, img.width), base.height+img.height), (255, 255, 255, 0))
                    new.alpha_composite(img, ((new.width - img.width)//2, 0))
                    new.alpha_composite(base, ((base.width - base.width) // 2, new.height - base.height))
                    imgs[-1] = new
                    new.img_type = base.img_type
                else:
                    img = lt_pow(base, exponent)
                    imgs.append(img)
                    img.img_type = "pow"

                idx += 1
        elif obj == "_":
            if idx + 1 < sz:
                base = imgs[-1] if imgs else LaTexImage.new((1, int(font.size*DeepToK(deep))), (255, 255, 255, 0))
                exponent = RenderLaTex(objs[idx + 1], deep, True, font, color)

                print("base",base.size)

                if base.img_type == "pow":
                    img = lt_low(base, exponent)
                    new = LaTexImage.new((max(base.width, img.width), max(base.height, img.height)), (255, 255, 255, 0))
                    new.alpha_composite(base, (0, (new.height - base.height) // 2))
                    new.alpha_composite(img, (0, (new.height - img.height) // 2))
                    imgs[-1] = new
                elif base.img_type in middle_lowandpows or (base.img_type in auto_middle_replaces and deep == 0 and not include):
                    print("mv", base.img_type, deep)
                    img = exponent.resize_with_k(2/3)
                    new = LaTexImage.new((max(base.width, img.width), base.height+img.height), (255, 255, 255, 0))
                    new.alpha_composite(base, ((new.width - base.width)//2, 0))
                    new.alpha_composite(img, ((new.width - img.width) // 2, new.height - img.height))
                    imgs[-1] = new
                    new.img_type = base.img_type
                else:
                    img = lt_low(base, exponent)
                    imgs.append(img)
                    img.img_type = "low"

                idx += 1
        elif isinstance(obj, str):
            fsize = GetFontSize(font, obj)
            img = LaTexImage.new((fsize[0], int(font.size)), (0,0,0,0))
            draw = LaTexImageDraw.Draw(img)
            draw.text((0, 0), obj, font=font, fill=color)

            if deep != 0:
                k = max(0.5, 1-deep *0.2)
                print(k)
                print(img.size)
                img = img.resize_with_deep(deep)

            imgs.append(img)
        elif isinstance(obj, list):
            img = RenderLaTex(obj, deep, include, font, color)
            imgs.append(img)
        else:
            print(f"Unsupported LaTeX object type: {type(obj)}")
        idx += 1
    
    return imgs

def RenderLaTex(
    objs: Union[str, list], 
    deep: int = 0, 
    include: bool = False,
    font: FreeTypeFont = df_font,
    color: Optional[Union[str, tuple[int, int, int, int], tuple[int, int, int]]] = None
) -> LaTexImage:
    """
    渲染LaTeX对象列表并返回合成后的图像
    :param objs: LaTeX对象列表
    :return: 渲染后的图像
    """
    imgs = RenderLaTexObjs(objs, deep, include, font, color)

    width = sum(img.width for img in imgs)
    height = max(img.height for img in imgs) if imgs else 0
    result_img = LaTexImage.new((width, height), (255, 255, 255, 0))

    x_offset = 0
    for img in imgs:
        result_img.alpha_composite(img, (x_offset, int((height - img.height) / 2)))
        x_offset += img.width

    return result_img

string = ""

def GetLaTexObjs(string: str) -> list[Union[str, LaTexFunc, LaTexReplace, list]]:
    objs: list[Union[str, LaTexFunc, LaTexReplace, list]] = []
    sz = len(string)
    idx = 0
    while idx < sz:
        if string[idx] == "{":
            end_idx = idx + 1
            left = 0
            while end_idx < sz:
                if string[end_idx] == "{":
                    left += 1
                elif string[end_idx] == "}":
                    if left == 0:
                        break
                    left -= 1
                end_idx += 1
            if end_idx < sz and string[end_idx] == "}" and left == 0:
                objs.append(GetLaTexObjs(string[idx + 1:end_idx]))
                idx = end_idx + 1
                continue
        elif string[idx] == "\\":
            end_idx = idx + 1
            while end_idx < sz and (string[end_idx].isalpha() or (string[end_idx] in ex_replaces and end_idx == idx + 1)):
                end_idx += 1
                if string[end_idx-1] in ex_replaces:
                    break
            if string[end_idx-1].isalpha() or (string[end_idx-1] in ex_replaces and end_idx - idx == 2):
                name = string[idx + 1:end_idx]
                flag = False
                for func in funcs:
                    if func.key == name:
                        flag = True
                        objs.append(func)
                        break
                if flag:
                    idx = end_idx
                    continue
                elif name in replaces:
                    objs.append(LaTexReplace(name, replaces[name]))
                    idx = end_idx
                    continue
        elif string[idx] in [" ", "\n"]:
            idx += 1
            continue
        else:
            objs.append(string[idx])
        idx += 1

    def _DealLaTexObjs(objs: list[Union[str, LaTexFunc, LaTexReplace, list]]) -> list[Union[str, LaTexFunc, LaTexReplace, list]]:
        sz = len(objs)
        idx = 0
        outs = []

        while idx < sz:
            obj = objs[idx]
            if isinstance(obj, LaTexReplace) and obj.key == "begin":
                if idx + 1 < sz:
                    print(objs[idx + 1])
                    lefta = GetLaTexTextObj(objs[idx + 1])

                    if lefta in env_funcs:
                        k = 1
                        temp_idx = idx + 2
                        while temp_idx < sz:
                            tobj = objs[temp_idx]
                            if isinstance(tobj, LaTexReplace) and tobj.key == "end" and temp_idx + 1 < sz and GetLaTexTextObj(objs[temp_idx + 1]) == lefta:
                                k -= 1
                                if k == 0:
                                    break
                            elif isinstance(tobj, LaTexReplace) and tobj.key == "begin" and temp_idx + 1 < sz and GetLaTexTextObj(objs[temp_idx + 1]) == lefta:
                                k += 1
                            temp_idx += 1
                        
                        if not temp_idx < sz or k != 0:
                            outs.append(obj)
                            continue
                        
                        obj = objs[temp_idx]
                        if isinstance(obj, LaTexReplace) and obj.key == "end" and temp_idx + 1 < sz and GetLaTexTextObj(objs[temp_idx + 1]) == lefta:
                            outs.append([objs[idx], objs[idx + 1], *_DealLaTexObjs(objs[idx+2:temp_idx]), objs[temp_idx], objs[temp_idx + 1]])
                            idx = temp_idx + 2
                            print("outs", outs[-1])
                            continue

            # elif isinstance(obj, LaTexReplace) and obj.key == "ce":
            #     ceobjs = []
            #     if idx + 1 < sz and isinstance(objs[idx + 1], list):
            #         ceobjs = objs[idx + 1]
                
            #     temp_idx = 0
            #     if not isinstance(ceobjs, list):
            #         idx += 1
            #         continue

            #     ts = len(ceobjs)

            #     outobjs = []

            #     while temp_idx < ts:
            #         if ceobjs[temp_idx] == "<" and ceobjs[temp_idx: temp_idx + 2] == ["<", "-"]:
            #             outobjs.append(ltf_cexleftarrow)
            #         elif ceobjs[temp_idx] == ">" and ceobjs[temp_idx: temp_idx + 2] == [">", "-"]:
            #             outobjs.append(ltf_cexrightarrow)
            #         elif ceobjs[temp_idx] == "<" and ceobjs[temp_idx: temp_idx + 3] == ["<", "-", ">"]:
            #             outobjs.append(ltf_cexleftrightarrow)
            #         elif ceobjs[temp_idx] == "<" and ceobjs[temp_idx: temp_idx + 4] == ["<", "-", ">"]:
            #             outobjs.append(ltf_cexdoubleleftrightarrow)

            else:
                outs.append(obj)
            
            idx += 1
        
        return outs

    print("objs", objs)

    return _DealLaTexObjs(objs)

