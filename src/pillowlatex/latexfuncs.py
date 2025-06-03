from .latex import (
    RegisterLaTexFunc, LaTexImage, LaTexImageDraw, GetFontSize, MixFont, GetLaTexTextObj
)
import math
from typing import Optional, Union

@RegisterLaTexFunc("frac", needFont = True, needColor = True)
def lt_frac(a: LaTexImage, b: LaTexImage, font: MixFont, color) -> LaTexImage:
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
    img = LaTexImage.new((width, height), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)
    draw.line((0, a.height + k // 2, width, a.height + k // 2), fill=color, width=ls)
    img.alpha_composite(a, ((width-a.width)//2, 0))
    img.alpha_composite(b, ((width-b.width)//2, a.height + 10))
    return img

@RegisterLaTexFunc("tfrac", needFont = True, needColor = True)
def lt_tfrac(a: LaTexImage, b: LaTexImage, font: MixFont, color) -> LaTexImage:
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
    img = LaTexImage.new((width, height), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)
    draw.line((0, a.height + k // 2, width, a.height + k // 2), fill=color, width=ls)
    img.alpha_composite(a, ((width-a.width)//2, 0))
    img.alpha_composite(b, ((width-b.width)//2, a.height + 10))
    return img.resize((int(width*0.5), int(height*0.5)))

RegisterLaTexFunc("cfrac", needFont = True, needColor = True)(lt_frac.func)

@RegisterLaTexFunc("mathrm")
def lt_mathrm(a: LaTexImage) -> LaTexImage:
    """
    渲染数学常规文本
    :param a: 文本图像
    :return: 渲染后的文本图像
    """
    return a

@RegisterLaTexFunc("operatorname")
def lt_operatorname(a: LaTexImage) -> LaTexImage:
    """
    渲染数学运算符名称
    :param a: 运算符名称图像
    :return: 渲染后的运算符名称图像
    """
    return a

@RegisterLaTexFunc("sqrt", nonenum = 1, needFont = True, needColor = True)
def lt_sqrt(a: Optional[LaTexImage], b: LaTexImage, font: MixFont, color) -> LaTexImage:
    
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
    
    img = LaTexImage.new((x, y), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    draw.line((xb + 10, yb + 5, xb + b.width + 10, yb + 5), fill=color, width=ls)
    draw.line((xb + 10, yb + 5, xb + 5, img.height), fill=color, width=ls)
    draw.line((xb + 5, img.height, xb + 3, img.height - (b.height // 2)), fill=color, width=ls)
    draw.line((xb + 3, img.height - (b.height // 2), 0, img.height - (b.height // 2)), fill=color, width=ls)

    if a:
        img.alpha_composite(a, (max(0, xb + 5 - a.width), img.height - b.height // 2 - a.height))
        # draw.rectangle((5, 0, 5+a.width, a.height), fill=(255, 255, 255, 100))

    img.alpha_composite(b, (xb + 10, yb + 10))
    return img

@RegisterLaTexFunc("dot", nosmaller=True, needFont = True, needColor = True)
def lt_dot(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染一阶导数
    :param a: 点图像
    :return: 渲染后的点图像
    """
    size = math.ceil(font.size / 10)
    ex = math.ceil(size / 4)

    img = LaTexImage.new((a.width, a.height + size + ex * 2), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    xmid = img.width // 2
    ymid = ex + size // 2
    half_size = size // 2

    img.alpha_composite(a, (0, ex * 2 + size))

    draw.ellipse((xmid - half_size, ymid - half_size, xmid + half_size, ymid + half_size), fill=color)

    return img

@RegisterLaTexFunc("ddot", nosmaller=True, needFont = True, needColor = True)
def lt_ddot(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染二阶导数
    :param a: 点图像
    :return: 渲染后的点图像
    """
    size = math.ceil(font.size / 10)
    ex = math.ceil(size / 4)

    img = LaTexImage.new((a.width, a.height + size + ex * 2), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    xmid = img.width // 2
    ymid = ex + size // 2
    half_size = size // 2

    img.alpha_composite(a, (0, ex * 2 + size))

    draw.ellipse((xmid - half_size - size - ex, ymid - half_size, xmid + half_size - size - ex, ymid + half_size), fill=color)
    draw.ellipse((xmid - half_size + size + ex, ymid - half_size, xmid + half_size + size + ex, ymid + half_size), fill=color)

    return img

@RegisterLaTexFunc("pmod", needDeep=True, nosmaller=True, needFont = True, needColor = True)
def lt_pmod(a: LaTexImage, deep: int, font: MixFont, color) -> LaTexImage:
    """
    渲染模运算
    :param a: 模数图像
    :return: 渲染后的模运算图像
    """
    xe1, ye1 = GetFontSize(font, "(mod ")
    xe2, ye2 = GetFontSize(font, ")")

    img1 = LaTexImage.new((xe1, ye1), (255, 255, 255, 0))
    draw1 = LaTexImageDraw.Draw(img1)
    draw1.text((0, 0), "(mod ", font=font, fill=color)
    img2 = LaTexImage.new((xe2, ye2), (255, 255, 255, 0))
    draw2 = LaTexImageDraw.Draw(img2)
    draw2.text((0, 0), ")", font=font, fill=color)

    img1 = img1.resize_with_deep(deep)
    img2 = img2.resize_with_deep(deep)

    xe1, ye1 = img1.size
    xe2, ye2 = img2.size

    new = LaTexImage.new((a.width + xe1 + xe2, max(a.height, ye1, ye2)), (255, 255, 255, 0))

    new.alpha_composite(a, (xe1, (new.height - a.height) // 2))
    new.alpha_composite(img1, (0, (new.height - ye1) // 2))
    new.alpha_composite(img2, (xe1 + a.width, (new.height - ye2) // 2))


    return new

@RegisterLaTexFunc("sideset", nosmaller=True)
def lt_sideset(a: LaTexImage, b: LaTexImage, c: LaTexImage) -> LaTexImage:
    """
    渲染带有侧标的数学表达式
    :return: 渲染后的带侧标的表达式图像
    """
    new = LaTexImage.new((a.width + b.width + c.width, max(a.height, b.height, c.height)), (255, 255, 255, 0))
    new.alpha_composite(a, (0, (new.height - a.height) // 2))
    new.alpha_composite(b, (a.width + c.width, (new.height - b.height) // 2))
    new.alpha_composite(c, (a.width, (new.height - c.height) // 2))
    return new

@RegisterLaTexFunc("hat", nosmaller=True, needFont = True, needColor = True)
def lt_hat(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "ˆ"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTexImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTexFunc("check", nosmaller=True, needFont = True, needColor = True)
def lt_check(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "ˇ"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTexImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTexFunc("grave", nosmaller=True, needFont = True, needColor = True)
def lt_grave(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "`"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTexImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTexFunc("acute", nosmaller=True, needFont = True, needColor = True)
def lt_acute(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "´"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTexImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTexFunc("tilde", nosmaller=True, needFont = True, needColor = True)
def lt_tilde(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "~"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 3)

    img = LaTexImage.new((max(fsize[0], a.width), fsize[1] // 2 * 2  + a.height + space * 2), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, fsize[1] // 2 + space + 3))

    return img

@RegisterLaTexFunc("breve", nosmaller=True, needFont = True, needColor = True)
def lt_breve(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "˘"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTexImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTexFunc("bar", nosmaller=True, needFont = True, needColor = True)
def lt_bar(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "¯"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    img = LaTexImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, space))

    return img

@RegisterLaTexFunc("vec", nosmaller=True, needFont = True, needColor = True)
def lt_vec(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "→"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 3)

    img = LaTexImage.new((max(fsize[0], a.width), fsize[1] // 2 * 2  + a.height + space * 2), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    draw.text(((img.width - fsize[0]) // 2, 0), text, font=font, fill=color)
    img.alpha_composite(a, ((img.width - a.width) // 2, fsize[1] // 2 + space + 3))

    return img

@RegisterLaTexFunc("not", nosmaller=True, needDeep=True, needFont = True, needColor = True)
def lt_not(a: LaTexImage, deep: int, font: MixFont, color) -> LaTexImage:
    """
    渲染not符号
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "⧸"
    fsize = GetFontSize(font, text)
    f = LaTexImage.new((fsize[0], int(font.size)), (255, 255, 255, 0))
    f = f.resize_with_deep(deep)

    img = LaTexImage.new((max(f.width, a.width), max(f.height, a.height)), (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)

    img.alpha_composite(a, ((img.width - a.width) // 2, (img.height - a.height) // 2))
    draw.text(((img.width - f.width) // 2, (img.height - f.height) // 2), text, font=font, fill=color)

    return img

@RegisterLaTexFunc("widetilde", nosmaller=True, needFont = True, needColor = True)
def lt_widetilde(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "~"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 3)

    f = LaTexImage.new((fsize[0], int(font.size)), (255, 255, 255, 0))
    img = LaTexImage.new((max(fsize[0], a.width), fsize[1] // 2 * 2  + a.height + space * 2), (255, 255, 255, 0))
    drawf = LaTexImageDraw.Draw(f)

    drawf.text((0, 0), text, font=font, fill=color)
    f = f.resize((min(fsize[0]*4, max(fsize[0], img.width)), f.height))

    img.alpha_composite(a, ((img.width - a.width) // 2, fsize[1] // 2 + space + 3))
    img.alpha_composite(f, ((img.width - f.width) // 2, 0))

    return img

@RegisterLaTexFunc("widehat", nosmaller=True, needFont = True, needColor = True)
def lt_widehat(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "ˆ"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 8) + 2

    f = LaTexImage.new((fsize[0], int(font.size)), (255, 255, 255, 0))
    img = LaTexImage.new((max(fsize[0], a.width), a.height + space), (255, 255, 255, 0))
    drawf = LaTexImageDraw.Draw(f)

    drawf.text((0, 0), text, font=font, fill=color)
    f = f.resize((min(fsize[0]*4, max(fsize[0], img.width)), f.height))

    img.alpha_composite(a, ((img.width - a.width) // 2, space))
    img.alpha_composite(f, ((img.width - f.width) // 2, 0))

    return img

@RegisterLaTexFunc("overleftarrow", nosmaller=True, needFont = True, needColor = True)
def lt_overleftarrow(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "⟵"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 3)

    f = LaTexImage.new((fsize[0], int(font.size)), (255, 255, 255, 0))
    img = LaTexImage.new((max(fsize[0], a.width), fsize[1] // 2 * 2  + a.height + space * 2), (255, 255, 255, 0))
    drawf = LaTexImageDraw.Draw(f)

    drawf.text((0, 0), text, font=font, fill=color)
    f = f.resize((max(fsize[0], img.width), f.height))

    img.alpha_composite(a, ((img.width - a.width) // 2, fsize[1] // 2 + space + 3))
    img.alpha_composite(f, ((img.width - f.width) // 2, 0))

    return img

@RegisterLaTexFunc("overrightarrow", nosmaller=True, needFont = True, needColor = True)
def lt_overrightarrow(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    text = "⟶"
    fsize = GetFontSize(font, text)
    space = math.ceil(font.size / 3)

    f = LaTexImage.new((fsize[0], int(font.size)), (255, 255, 255, 0))
    img = LaTexImage.new((max(fsize[0], a.width), fsize[1] // 2 * 2  + a.height + space * 2), (255, 255, 255, 0))
    drawf = LaTexImageDraw.Draw(f)

    drawf.text((0, 0), text, font=font, fill=color)
    f = f.resize((max(fsize[0], img.width), f.height))

    img.alpha_composite(a, ((img.width - a.width) // 2, fsize[1] // 2 + space + 3))
    img.alpha_composite(f, ((img.width - f.width) // 2, 0))

    return img

@RegisterLaTexFunc("overline", nosmaller=True, needFont = True, needColor = True)
def lt_overline(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    k = math.ceil(font.size / 10)
    ls = math.ceil(font.size / 20)

    new = LaTexImage.new((a.width + k, a.height + k*4), (255, 255, 255, 0))
    new.alpha_composite(a, (0, k*2))
    draw = LaTexImageDraw.Draw(new)

    draw.line((0, k, a.width, k), fill=color, width=ls)

    return new

@RegisterLaTexFunc("underline", nosmaller=True, needFont = True, needColor = True)
def lt_underline(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    k = math.ceil(font.size / 20)
    ls = math.ceil(font.size / 20)

    new = LaTexImage.new((a.width + k, a.height + k*4), (255, 255, 255, 0))
    new.alpha_composite(a, (0, k*2))
    draw = LaTexImageDraw.Draw(new)

    draw.line((0, k*3+a.height, a.width, k*3+a.height), fill=color, width=ls)

    return new

@RegisterLaTexFunc("overbrace", nosmaller=True, needFont = True, needColor = True)
def lt_overbrace(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    k = math.ceil(font.size / 5)
    l = math.ceil(GetFontSize(font, "⏞")[0] // 4)
    ls = math.ceil(font.size / 20)

    new = LaTexImage.new((a.width, a.height + k*2), (255, 255, 255, 0))
    new.alpha_composite(a, (0, k))
    draw = LaTexImageDraw.Draw(new)

    mid = a.width // 2

    for line in [
        (0, k, l, k//2), (l, k//2, mid - l, k//2), (mid - l, k//2, mid, 0),
        (mid, 0, mid + l, k // 2), (mid + l, k // 2, a.width - l, k // 2), (a.width - l, k // 2, a.width, k)
    ]:
        draw.line(line, fill=color, width=ls)

    return new

@RegisterLaTexFunc("underbrace", nosmaller=True, needFont = True, needColor = True)
def lt_underbrace(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    k = math.ceil(font.size / 5)
    l = math.ceil(GetFontSize(font, "⏞")[0] // 4)
    ls = math.ceil(font.size / 20)

    new = LaTexImage.new((a.width, a.height + k*2), (255, 255, 255, 0))
    new.alpha_composite(a, (0, k))
    draw = LaTexImageDraw.Draw(new)

    mid = a.width // 2

    for line in [
        (0, k, l, k//2), (l, k//2, mid - l, k//2), (mid - l, k//2, mid, 0),
        (mid, 0, mid + l, k // 2), (mid + l, k // 2, a.width - l, k // 2), (a.width - l, k // 2, a.width, k)
    ]:
        draw.line([line[0], new.height - line[1], line[2], new.height - line[3]], fill=color, width=ls)

    return new

@RegisterLaTexFunc("overset", nosmaller=True)
def lt_overset(a: LaTexImage, b: LaTexImage) -> LaTexImage:
    """
    渲染上标的数学表达式
    :param a: 上标图像
    :param b: 表达式图像
    """

    new = LaTexImage.new((max(a.width, b.width), a.height * 2 + b.height), (255, 255, 255, 0))
    new.alpha_composite(a, ((new.width - a.width) // 2, 0))
    new.alpha_composite(b, ((new.width - b.width) // 2, a.height))

    return new

@RegisterLaTexFunc("underset", nosmaller=True)
def lt_underset(a: LaTexImage, b: LaTexImage) -> LaTexImage:
    """
    渲染下标的数学表达式
    :param a: 下标图像
    :param b: 表达式图像
    """

    new = LaTexImage.new((max(a.width, b.width), a.height * 2 + b.height), (255, 255, 255, 0))
    new.alpha_composite(a, ((new.width - a.width) // 2, b.height + a.height))
    new.alpha_composite(b, ((new.width - b.width) // 2, 0))

    return new

@RegisterLaTexFunc("stackrel", nosmaller=True)
def lt_stackrel(a: LaTexImage, b: LaTexImage) -> LaTexImage:
    """
    渲染堆叠的数学表达式
    :param a: 上标图像
    :param b: 下标图像
    """

    new = LaTexImage.new((max(a.width, b.width), a.height * 2 + b.height), (255, 255, 255, 0))
    new.alpha_composite(a, ((new.width - a.width) // 2, 0))
    new.alpha_composite(b, ((new.width - b.width) // 2, a.height))

    return new

@RegisterLaTexFunc("overleftrightarrow", nosmaller=True, needFont = True, needColor = True)
def lt_overleftrightarrow(a: LaTexImage, font: MixFont, color) -> LaTexImage:
    """
    渲染带帽的数学表达式
    :param a: 表达式图像
    :return: 渲染后的带帽的表达式图像
    """
    k = math.ceil(font.size / 5)
    l = math.ceil(GetFontSize(font, "⏞")[0] // 2)
    ls = math.ceil(font.size / 20)

    new = LaTexImage.new((a.width, a.height + k*2), (255, 255, 255, 0))
    new.alpha_composite(a, (0, k))
    draw = LaTexImageDraw.Draw(new)

    for line in [
        (0, k//2, l, 0), (0, k//2, l, k),
        (0, k//2, new.width, k // 2),
        (new.width, k // 2, new.width - l, k), (new.width, k // 2, new.width - l, 0),
    ]:
        draw.line(line, fill=color, width=ls)

    return new

@RegisterLaTexFunc("xleftarrow", nonenum = 1, needFont = True, needColor = True)
def lt_xleftarrow(a: Optional[LaTexImage], b: LaTexImage, font: MixFont, color) -> LaTexImage:
    k = GetFontSize(font, "a")[0]
    height = int(font.size)

    if not a:
        a = LaTexImage.new((1, 1), (255, 255, 255, 0))

    new = LaTexImage.new((max(a.width, b.width) + k*2, max(a.height, b.height) * 2 + height), (255, 255, 255, 0))

    new.alpha_composite(a, ((new.width - a.width) // 2, int(new.height // 2 - height // 2 - a.height)))
    new.alpha_composite(b, ((new.width - b.width) // 2, int(new.height // 2 + height // 2)))

    mid = new.height // 2
    ak = math.ceil(font.size / 5)
    l = math.ceil(GetFontSize(font, "⏞")[0] // 2)
    draw = LaTexImageDraw.Draw(new)
    ls = math.ceil(font.size / 20)

    for line in [
        (0, mid, ak, mid + l), (0, mid, ak, mid - l),
        (0, mid, new.width, mid)
    ]:
        draw.line(line, fill=color, width=ls)

    return new

@RegisterLaTexFunc("xrightarrow", nonenum = 1, needFont = True, needColor = True)
def lt_xrightarrow(a: Optional[LaTexImage], b: LaTexImage, font: MixFont, color) -> LaTexImage:
    k = GetFontSize(font, "a")[0]
    height = int(font.size)

    if not a:
        a = LaTexImage.new((1, 1), (255, 255, 255, 0))

    new = LaTexImage.new((max(a.width, b.width) + k*2, max(a.height, b.height) * 2 + height), (255, 255, 255, 0))

    new.alpha_composite(a, ((new.width - a.width) // 2, int(new.height // 2 - height // 2 - a.height)))
    new.alpha_composite(b, ((new.width - b.width) // 2, int(new.height // 2 + height // 2)))

    mid = new.height // 2
    ak = math.ceil(font.size / 5)
    l = math.ceil(GetFontSize(font, "⏞")[0] // 2)
    draw = LaTexImageDraw.Draw(new)
    ls = math.ceil(font.size / 20)

    for line in [
        (0, mid, new.width, mid),
        (new.width, mid, new.width - ak, mid + l), (new.width, mid, new.width - ak, mid - l)
    ]:
        draw.line(line, fill=color, width=ls)

    return new

@RegisterLaTexFunc("textstyle", nosmaller=True)
def lt_textstyle(a: LaTexImage) -> LaTexImage:
    """
    渲染文本样式的数学表达式
    :param a: 表达式图像
    :return: 渲染后的文本样式的表达式图像
    """
    a.img_type = "text"
    return a

@RegisterLaTexFunc("binom", nosmaller=True, needDeep=True, needFont = True, needColor = True)
def lt_binom(a: LaTexImage, b: LaTexImage, deep: int, font: MixFont, color) -> LaTexImage:
    """
    渲染二项式系数
    :param a: 上标图像
    :param b: 下标图像
    :return: 渲染后的二项式系数图像
    """
    x1,y1 = GetFontSize(font, "(")
    x2,y2 = GetFontSize(font, ")")
    img1 = LaTexImage.new((x1, y1), (255, 255, 255, 0))
    img2 = LaTexImage.new((x2, y2), (255, 255, 255, 0))
    draw1 = LaTexImageDraw.Draw(img1)
    draw2 = LaTexImageDraw.Draw(img2)

    draw1.text((0, 0), "(", font=font, fill=color)
    draw2.text((0, 0), ")", font=font, fill=color)

    img1 = img1.resize_with_deep(deep)
    img2 = img2.resize_with_deep(deep)

    k = math.ceil(img1.height / 5)

    new = LaTexImage.new((max(a.width, b.width) + img1.width + img2.width, max(a.height + b.height + k, img1.height, img2.height)), (255, 255, 255, 0))

    img1 = img1.resize((img1.width, new.height))
    img2 = img2.resize((img2.width, new.height))

    new.alpha_composite(img1, (0, (new.height - img1.height) // 2))
    new.alpha_composite(a, (img1.width + (new.width - img2.width - img1.width) // 2 - a.width // 2, 0))
    new.alpha_composite(b, (img1.width + (new.width - img2.width - img1.width) // 2 - b.width // 2, new.height - b.height))
    new.alpha_composite(img2, (new.width - img2.width, (new.height - img2.height) // 2))

    return new

@RegisterLaTexFunc("text")
def lt_text(a: LaTexImage) -> LaTexImage:
    """
    渲染文本样式的数学表达式
    :param a: 表达式图像
    :return: 渲染后的文本样式的表达式图像
    """
    a.img_type = "text"
    return a

@RegisterLaTexFunc("unicode", nosmaller = True, needDeep = True, needFont = True, needColor = True, autoRender = False)
def lt_unicode(a: Union[str, list], deep: int, font: MixFont, color) -> LaTexImage:
    """
    渲染Unicode样式的数学表达式
    :param a: 表达式图像
    :return: 渲染后的Unicode样式的表达式图像
    """
    text = GetLaTexTextObj(a) or ""

    try:
        char = chr(int(text))
    except:
        char = ""

    size = GetFontSize(font, char)
    img = LaTexImage.new(size, (255, 255, 255, 0))
    draw = LaTexImageDraw.Draw(img)
    draw.text((0, 0), char, font=font, fill=color)
    img = img.resize_with_deep(deep)

    return img