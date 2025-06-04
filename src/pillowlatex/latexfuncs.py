from .latex import (
    RegisterLaTeXFunc, LaTeXImage, LaTeXImageDraw, GetFontSize, MixFont, GetLaTeXTextObj
)
import math
from typing import Optional, Union

@RegisterLaTeXFunc("frac", needFont = True, needColor = True)
def lt_frac(a: LaTeXImage, b: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染分数
    :param a: 分子图像
    :param b: 分母图像
    :return: 渲染后的分数图像
    """

    # a = a.resize((int(a.width * 0.8), int(a.height * 0.8)))
    # b = b.resize((int(b.width * 0.8), int(b.height * 0.8)))

    k = math.ceil(font.size / 5)
    ls = math.ceil(font.size / 20)
    width = max(a.width, b.width) + k
    height = a.height + b.height + k
    img = LaTeXImage.new((width, height), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)
    draw.line((0, a.height + k // 2, width, a.height + k // 2), fill=color, width=ls)
    img.alpha_composite(a, ((width-a.width)//2, 0))
    img.alpha_composite(b, ((width-b.width)//2, a.height + 10))
    return img

@RegisterLaTeXFunc("tfrac", needFont = True, needColor = True)
def lt_tfrac(a: LaTeXImage, b: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染小分数
    :param a: 分子图像
    :param b: 分母图像
    :return: 渲染后的分数图像
    """

    # a = a.resize((int(a.width * 0.8), int(a.height * 0.8)))
    # b = b.resize((int(b.width * 0.8), int(b.height * 0.8)))

    k = math.ceil(font.size / 5)
    ls = math.ceil(font.size / 20)
    width = max(a.width, b.width) + k
    height = a.height + b.height + k
    img = LaTeXImage.new((width, height), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)
    draw.line((0, a.height + k // 2, width, a.height + k // 2), fill=color, width=ls)
    img.alpha_composite(a, ((width-a.width)//2, 0))
    img.alpha_composite(b, ((width-b.width)//2, a.height + 10))
    return img.resize((int(width*0.5), int(height*0.5)))

RegisterLaTeXFunc("cfrac", needFont = True, needColor = True)(lt_frac.func)

@RegisterLaTeXFunc("mathrm")
def lt_mathrm(a: LaTeXImage) -> LaTeXImage:
    """
    渲染数学常规文本
    :param a: 文本图像
    :return: 渲染后的文本图像
    """
    return a

@RegisterLaTeXFunc("operatorname")
def lt_operatorname(a: LaTeXImage) -> LaTeXImage:
    """
    渲染数学运算符名称
    :param a: 运算符名称图像
    :return: 渲染后的运算符名称图像
    """
    return a

@RegisterLaTeXFunc("sqrt", nonenum = 1, needFont = True, needColor = True)
def lt_sqrt(a: Optional[LaTeXImage], b: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    
    x = b.width + 10
    y = b.height + 10
    xb = 0
    yb = 0
    ls = math.ceil(font.size / 20)

    if a:
        a = a.resize((a.width * 2 // 3, a.height * 2 // 3))
        xb = max(0, a.width - 5)
        x += xb
        yb = max(0, a.height - b.height // 2)
        y += yb
    
    img = LaTeXImage.new((x, y), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    draw.line((xb + 10, yb + 5, xb + b.width + 10, yb + 5), fill=color, width=ls)
    draw.line((xb + 10, yb + 5, xb + 5, img.height), fill=color, width=ls)
    draw.line((xb + 5, img.height, xb + 3, img.height - (b.height // 2)), fill=color, width=ls)
    draw.line((xb + 3, img.height - (b.height // 2), 0, img.height - (b.height // 2)), fill=color, width=ls)

    if a:
        img.alpha_composite(a, (max(0, xb + 5 - a.width), img.height - b.height // 2 - a.height))
        # draw.rectangle((5, 0, 5+a.width, a.height), fill=(255, 255, 255, 100))

    img.alpha_composite(b, (xb + 10, yb + 10))
    return img

@RegisterLaTeXFunc("dot", nosmaller=True, needFont = True, needColor = True)
def lt_dot(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染一阶导数
    :param a: 点图像
    :return: 渲染后的点图像
    """
    size = math.ceil(font.size / 10)
    ex = math.ceil(size / 4)

    img = LaTeXImage.new((a.width, a.height + size + ex * 2), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    xmid = img.width // 2
    ymid = ex + size // 2
    half_size = size // 2

    img.alpha_composite(a, (0, ex * 2 + size))

    draw.ellipse((xmid - half_size, ymid - half_size, xmid + half_size, ymid + half_size), fill=color)

    return img

@RegisterLaTeXFunc("ddot", nosmaller=True, needFont = True, needColor = True)
def lt_ddot(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染二阶导数
    :param a: 点图像
    :return: 渲染后的点图像
    """
    size = math.ceil(font.size / 10)
    ex = math.ceil(size / 4)

    img = LaTeXImage.new((a.width, a.height + size + ex * 2), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    xmid = img.width // 2
    ymid = ex + size // 2
    half_size = size // 2

    img.alpha_composite(a, (0, ex * 2 + size))

    draw.ellipse((xmid - half_size - size - ex, ymid - half_size, xmid + half_size - size - ex, ymid + half_size), fill=color)
    draw.ellipse((xmid - half_size + size + ex, ymid - half_size, xmid + half_size + size + ex, ymid + half_size), fill=color)

    return img

@RegisterLaTeXFunc("pmod", needDeep=True, nosmaller=True, needFont = True, needColor = True)
def lt_pmod(a: LaTeXImage, deep: int, font: MixFont, color) -> LaTeXImage:
    """
    渲染模运算
    :param a: 模数图像
    :return: 渲染后的模运算图像
    """
    xe1, ye1 = GetFontSize(font, "(mod ")
    xe2, ye2 = GetFontSize(font, ")")

    img1 = LaTeXImage.new((xe1, ye1), (255, 255, 255, 0))
    draw1 = LaTeXImageDraw.Draw(img1)
    draw1.text((0, 0), "(mod ", font=font, fill=color)
    img2 = LaTeXImage.new((xe2, ye2), (255, 255, 255, 0))
    draw2 = LaTeXImageDraw.Draw(img2)
    draw2.text((0, 0), ")", font=font, fill=color)

    img1 = img1.resize_with_deep(deep)
    img2 = img2.resize_with_deep(deep)

    xe1, ye1 = img1.size
    xe2, ye2 = img2.size

    new = LaTeXImage.new((a.width + xe1 + xe2, max(a.height, ye1, ye2)), (255, 255, 255, 0))

    new.alpha_composite(a, (xe1, (new.height - a.height) // 2))
    new.alpha_composite(img1, (0, (new.height - ye1) // 2))
    new.alpha_composite(img2, (xe1 + a.width, (new.height - ye2) // 2))


    return new

@RegisterLaTeXFunc("sideset", nosmaller=True)
def lt_sideset(a: LaTeXImage, b: LaTeXImage, c: LaTeXImage) -> LaTeXImage:
    """
    渲染带有侧标的数学表达式
    :return: 渲染后的带侧标的表达式图像
    """
    new = LaTeXImage.new((a.width + b.width + c.width, max(a.height, b.height, c.height)), (255, 255, 255, 0))
    new.alpha_composite(a, (0, (new.height - a.height) // 2))
    new.alpha_composite(b, (a.width + c.width, (new.height - b.height) // 2))
    new.alpha_composite(c, (a.width, (new.height - c.height) // 2))
    return new

@RegisterLaTeXFunc("hat", nosmaller=True, needFont = True, needColor = True)
def lt_hat(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "ˆ"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTeXImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTeXFunc("check", nosmaller=True, needFont = True, needColor = True)
def lt_check(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "ˇ"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTeXImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTeXFunc("grave", nosmaller=True, needFont = True, needColor = True)
def lt_grave(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "`"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTeXImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTeXFunc("acute", nosmaller=True, needFont = True, needColor = True)
def lt_acute(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "´"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTeXImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTeXFunc("tilde", nosmaller=True, needFont = True, needColor = True)
def lt_tilde(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "~"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 3)

    img = LaTeXImage.new((max(fsize[0], a.width), fsize[1] // 2 * 2  + a.height + space * 2), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, fsize[1] // 2 + space + 3))

    return img

@RegisterLaTeXFunc("breve", nosmaller=True, needFont = True, needColor = True)
def lt_breve(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "˘"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTeXImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTeXFunc("bar", nosmaller=True, needFont = True, needColor = True)
def lt_bar(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "¯"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTeXImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTeXFunc("vec", nosmaller=True, needFont = True, needColor = True)
def lt_vec(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "→"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 3)

    img = LaTeXImage.new((max(fsize[0], a.width), fsize[1] // 2 * 2  + a.height + space * 2), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, fsize[1] // 2 + space + 3))

    return img

@RegisterLaTeXFunc("not", nosmaller=True, needDeep=True, needFont = True, needColor = True)
def lt_not(a: LaTeXImage, deep: int, font: MixFont, color) -> LaTeXImage:
    """
    渲染not符号
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "⧸"
    fsize = GetFontSize(font, text)
    f = LaTeXImage.new((fsize[0], int(font.size)), (255, 255, 255, 0))
    f = f.resize_with_deep(deep)

    img = LaTeXImage.new((max(f.width, a.width), max(f.height, a.height)), (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)

    img.alpha_composite(a, ((img.width - a.width) // 2, (img.height - a.height) // 2))
    draw.text(((img.width - f.width) // 2, (img.height - f.height) // 2), text, font=font, fill=color)

    return img

@RegisterLaTeXFunc("widetilde", nosmaller=True, needFont = True, needColor = True)
def lt_widetilde(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "~"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 3)

    f = LaTeXImage.new((fsize[0], int(font.size)), (255, 255, 255, 0))
    img = LaTeXImage.new((max(fsize[0], a.width), fsize[1] // 2 * 2  + a.height + space * 2), (255, 255, 255, 0))
    drawf = LaTeXImageDraw.Draw(f)

    drawf.text((0, 0), text, font=font, fill=color)
    f = f.resize((min(fsize[0]*4, max(fsize[0], img.width)), f.height))

    img.alpha_composite(a, ((img.width - a.width) // 2, fsize[1] // 2 + space + 3))
    img.alpha_composite(f, ((img.width - f.width) // 2, 0))

    return img

@RegisterLaTeXFunc("widehat", nosmaller=True, needFont = True, needColor = True)
def lt_widehat(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "ˆ"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    f = LaTeXImage.new((fsize[0], int(font.size)), (255, 255, 255, 0))
    img = LaTeXImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    drawf = LaTeXImageDraw.Draw(f)

    drawf.text((0, 0), text, font=font, fill=color)
    f = f.resize((min(fsize[0]*4, max(fsize[0], img.width)), f.height))

    img.alpha_composite(a, ((img.width - a.width) // 2, space))
    img.alpha_composite(f, ((img.width - f.width) // 2, 0))

    return img

@RegisterLaTeXFunc("overleftarrow", nosmaller=True, needFont = True, needColor = True)
def lt_overleftarrow(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "⟵"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 3)

    f = LaTeXImage.new((fsize[0], int(font.size)), (255, 255, 255, 0))
    img = LaTeXImage.new((max(fsize[0], a.width), fsize[1] // 2 * 2  + a.height + space * 2), (255, 255, 255, 0))
    drawf = LaTeXImageDraw.Draw(f)

    drawf.text((0, 0), text, font=font, fill=color)
    f = f.resize((max(fsize[0], img.width), f.height))

    img.alpha_composite(a, ((img.width - a.width) // 2, fsize[1] // 2 + space + 3))
    img.alpha_composite(f, ((img.width - f.width) // 2, 0))

    return img

@RegisterLaTeXFunc("overrightarrow", nosmaller=True, needFont = True, needColor = True)
def lt_overrightarrow(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "⟶"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 3)

    f = LaTeXImage.new((fsize[0], int(font.size)), (255, 255, 255, 0))
    img = LaTeXImage.new((max(fsize[0], a.width), fsize[1] // 2 * 2  + a.height + space * 2), (255, 255, 255, 0))
    drawf = LaTeXImageDraw.Draw(f)

    drawf.text((0, 0), text, font=font, fill=color)
    f = f.resize((max(fsize[0], img.width), f.height))

    img.alpha_composite(a, ((img.width - a.width) // 2, fsize[1] // 2 + space + 3))
    img.alpha_composite(f, ((img.width - f.width) // 2, 0))

    return img

@RegisterLaTeXFunc("overline", nosmaller=True, needFont = True, needColor = True)
def lt_overline(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    k = math.ceil(font.size / 10)
    ls = math.ceil(font.size / 20)

    new = LaTeXImage.new((a.width + k, a.height + k*4), (255, 255, 255, 0))
    new.alpha_composite(a, (0, k*2))
    draw = LaTeXImageDraw.Draw(new)

    draw.line((0, k, a.width, k), fill=color, width=ls)

    return new

@RegisterLaTeXFunc("underline", nosmaller=True, needFont = True, needColor = True)
def lt_underline(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    k = math.ceil(font.size / 20)
    ls = math.ceil(font.size / 20)

    new = LaTeXImage.new((a.width + k, a.height + k*4), (255, 255, 255, 0))
    new.alpha_composite(a, (0, k*2))
    draw = LaTeXImageDraw.Draw(new)

    draw.line((0, k*3+a.height, a.width, k*3+a.height), fill=color, width=ls)

    return new

@RegisterLaTeXFunc("overbrace", nosmaller=True, needFont = True, needColor = True)
def lt_overbrace(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    k = math.ceil(font.size / 5)
    l = math.ceil(GetFontSize(font, "⏞")[0] // 4)
    ls = math.ceil(font.size / 20)

    new = LaTeXImage.new((a.width, a.height + k*2), (255, 255, 255, 0))
    new.alpha_composite(a, (0, k))
    draw = LaTeXImageDraw.Draw(new)

    mid = a.width // 2

    for line in [
        (0, k, l, k//2), (l, k//2, mid - l, k//2), (mid - l, k//2, mid, 0),
        (mid, 0, mid + l, k // 2), (mid + l, k // 2, a.width - l, k // 2), (a.width - l, k // 2, a.width, k)
    ]:
        draw.line(line, fill=color, width=ls)

    return new

@RegisterLaTeXFunc("underbrace", nosmaller=True, needFont = True, needColor = True)
def lt_underbrace(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    k = math.ceil(font.size / 5)
    l = math.ceil(GetFontSize(font, "⏞")[0] // 4)
    ls = math.ceil(font.size / 20)

    new = LaTeXImage.new((a.width, a.height + k*2), (255, 255, 255, 0))
    new.alpha_composite(a, (0, k))
    draw = LaTeXImageDraw.Draw(new)

    mid = a.width // 2

    for line in [
        (0, k, l, k//2), (l, k//2, mid - l, k//2), (mid - l, k//2, mid, 0),
        (mid, 0, mid + l, k // 2), (mid + l, k // 2, a.width - l, k // 2), (a.width - l, k // 2, a.width, k)
    ]:
        draw.line([line[0], new.height - line[1], line[2], new.height - line[3]], fill=color, width=ls)

    return new

@RegisterLaTeXFunc("overset", nosmaller=True)
def lt_overset(a: LaTeXImage, b: LaTeXImage) -> LaTeXImage:
    """
    渲染上标的数学表达式
    :param a: 上标图像
    :param b: 表达式图像
    """

    new = LaTeXImage.new((max(a.width, b.width), a.height * 2 + b.height), (255, 255, 255, 0))
    new.alpha_composite(a, ((new.width - a.width) // 2, 0))
    new.alpha_composite(b, ((new.width - b.width) // 2, a.height))

    return new

@RegisterLaTeXFunc("underset", nosmaller=True)
def lt_underset(a: LaTeXImage, b: LaTeXImage) -> LaTeXImage:
    """
    渲染下标的数学表达式
    :param a: 下标图像
    :param b: 表达式图像
    """

    new = LaTeXImage.new((max(a.width, b.width), a.height * 2 + b.height), (255, 255, 255, 0))
    new.alpha_composite(a, ((new.width - a.width) // 2, b.height + a.height))
    new.alpha_composite(b, ((new.width - b.width) // 2, 0))

    return new

@RegisterLaTeXFunc("stackrel", nosmaller=True)
def lt_stackrel(a: LaTeXImage, b: LaTeXImage) -> LaTeXImage:
    """
    渲染堆叠的数学表达式
    :param a: 上标图像
    :param b: 下标图像
    """

    new = LaTeXImage.new((max(a.width, b.width), a.height * 2 + b.height), (255, 255, 255, 0))
    new.alpha_composite(a, ((new.width - a.width) // 2, 0))
    new.alpha_composite(b, ((new.width - b.width) // 2, a.height))

    return new

@RegisterLaTeXFunc("overleftrightarrow", nosmaller=True, needFont = True, needColor = True)
def lt_overleftrightarrow(a: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    k = math.ceil(font.size / 5)
    l = math.ceil(GetFontSize(font, "⏞")[0] // 2)
    ls = math.ceil(font.size / 20)

    new = LaTeXImage.new((a.width, a.height + k*2), (255, 255, 255, 0))
    new.alpha_composite(a, (0, k))
    draw = LaTeXImageDraw.Draw(new)

    for line in [
        (0, k//2, l, 0), (0, k//2, l, k),
        (0, k//2, new.width, k // 2),
        (new.width, k // 2, new.width - l, k), (new.width, k // 2, new.width - l, 0),
    ]:
        draw.line(line, fill=color, width=ls)

    return new

@RegisterLaTeXFunc("xleftarrow", nonenum = 1, needFont = True, needColor = True)
def lt_xleftarrow(a: Optional[LaTeXImage], b: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    k = GetFontSize(font, "a")[0]
    height = int(font.size)

    if not a:
        a = LaTeXImage.new((1, 1), (255, 255, 255, 0))

    new = LaTeXImage.new((max(a.width, b.width) + k*2, max(a.height, b.height) * 2 + height), (255, 255, 255, 0))

    new.alpha_composite(a, ((new.width - a.width) // 2, int(new.height // 2 - height // 2 - a.height)))
    new.alpha_composite(b, ((new.width - b.width) // 2, int(new.height // 2 + height // 2)))

    mid = new.height // 2
    ak = math.ceil(font.size / 5)
    l = math.ceil(GetFontSize(font, "⏞")[0] // 2)
    draw = LaTeXImageDraw.Draw(new)
    ls = math.ceil(font.size / 20)

    for line in [
        (0, mid, ak, mid + l), (0, mid, ak, mid - l),
        (0, mid, new.width, mid)
    ]:
        draw.line(line, fill=color, width=ls)

    return new

@RegisterLaTeXFunc("xrightarrow", nonenum = 1, needFont = True, needColor = True)
def lt_xrightarrow(a: Optional[LaTeXImage], b: LaTeXImage, font: MixFont, color) -> LaTeXImage:
    k = GetFontSize(font, "a")[0]
    height = int(font.size)

    if not a:
        a = LaTeXImage.new((1, 1), (255, 255, 255, 0))

    new = LaTeXImage.new((max(a.width, b.width) + k*2, max(a.height, b.height) * 2 + height), (255, 255, 255, 0))

    new.alpha_composite(a, ((new.width - a.width) // 2, int(new.height // 2 - height // 2 - a.height)))
    new.alpha_composite(b, ((new.width - b.width) // 2, int(new.height // 2 + height // 2)))

    mid = new.height // 2
    ak = math.ceil(font.size / 5)
    l = math.ceil(GetFontSize(font, "⏞")[0] // 2)
    draw = LaTeXImageDraw.Draw(new)
    ls = math.ceil(font.size / 20)

    for line in [
        (0, mid, new.width, mid),
        (new.width, mid, new.width - ak, mid + l), (new.width, mid, new.width - ak, mid - l)
    ]:
        draw.line(line, fill=color, width=ls)

    return new

@RegisterLaTeXFunc("textstyle", nosmaller=True)
def lt_textstyle(a: LaTeXImage) -> LaTeXImage:
    """
    渲染文本样式的数学表达式
    :param a: 表达式图像
    :return: 渲染后的文本样式的表达式图像
    """
    a.img_type = "text"
    return a

@RegisterLaTeXFunc("binom", nosmaller=True, needDeep=True, needFont = True, needColor = True)
def lt_binom(a: LaTeXImage, b: LaTeXImage, deep: int, font: MixFont, color) -> LaTeXImage:
    """
    渲染二项式系数
    :param a: 上标图像
    :param b: 下标图像
    :return: 渲染后的二项式系数图像
    """
    x1,y1 = GetFontSize(font, "(")
    x2,y2 = GetFontSize(font, ")")
    img1 = LaTeXImage.new((x1, y1), (255, 255, 255, 0))
    img2 = LaTeXImage.new((x2, y2), (255, 255, 255, 0))
    draw1 = LaTeXImageDraw.Draw(img1)
    draw2 = LaTeXImageDraw.Draw(img2)

    draw1.text((0, 0), "(", font=font, fill=color)
    draw2.text((0, 0), ")", font=font, fill=color)

    img1 = img1.resize_with_deep(deep)
    img2 = img2.resize_with_deep(deep)

    k = math.ceil(img1.height / 5)

    new = LaTeXImage.new((max(a.width, b.width) + img1.width + img2.width, max(a.height + b.height + k, img1.height, img2.height)), (255, 255, 255, 0))

    img1 = img1.resize((img1.width, new.height))
    img2 = img2.resize((img2.width, new.height))

    new.alpha_composite(img1, (0, (new.height - img1.height) // 2))
    new.alpha_composite(a, (img1.width + (new.width - img2.width - img1.width) // 2 - a.width // 2, 0))
    new.alpha_composite(b, (img1.width + (new.width - img2.width - img1.width) // 2 - b.width // 2, new.height - b.height))
    new.alpha_composite(img2, (new.width - img2.width, (new.height - img2.height) // 2))

    return new

@RegisterLaTeXFunc("text")
def lt_text(a: LaTeXImage) -> LaTeXImage:
    """
    渲染文本样式的数学表达式
    :param a: 表达式图像
    :return: 渲染后的文本样式的表达式图像
    """
    a.img_type = "text"
    return a

@RegisterLaTeXFunc("unicode", nosmaller = True, needDeep = True, needFont = True, needColor = True, autoRender = False)
def lt_unicode(a: Union[str, list], deep: int, font: MixFont, color) -> LaTeXImage:
    """
    渲染Unicode样式的数学表达式
    :param a: 表达式图像
    :return: 渲染后的Unicode样式的表达式图像
    """
    text = GetLaTeXTextObj(a) or ""

    try:
        char = chr(int(text))
    except:
        char = ""

    size = GetFontSize(font, char)
    img = LaTeXImage.new(size, (255, 255, 255, 0))
    draw = LaTeXImageDraw.Draw(img)
    draw.text((0, 0), char, font=font, fill=color)
    img = img.resize_with_deep(deep)

    return img