from .latex import(
    RegisterLaTeXEnvFunc, LaTeXImage, LaTeXImageDraw, GetFontSize, MixFont, GetLaTeXTextObj
)
from typing import Union

@RegisterLaTeXEnvFunc("matrix", needFont = True)
def lt_matrix(objs: list[list[LaTeXImage]], font: MixFont) -> LaTeXImage:
    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
    
    return new

@RegisterLaTeXEnvFunc("align*", needFont = True)
def lt_aligns(objs: list[list[LaTeXImage]], font: MixFont) -> LaTeXImage:
    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
    
    return new

@RegisterLaTeXEnvFunc("align", needFont = True)
def lt_align(objs: list[list[LaTeXImage]], font: MixFont) -> LaTeXImage:
    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
    
    return new

@RegisterLaTeXEnvFunc("array", needFont = True)
def lt_array(mode: Union[str, list], objs: list[list[LaTeXImage]], font: MixFont) -> LaTeXImage:

    m = GetLaTeXTextObj(mode)

    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            if m == "l":
                new.alpha_composite(img, (int(sum(widths[:j]) + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
            elif m == "r":
                new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
            else:
                new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
    
    return new

@RegisterLaTeXEnvFunc("eqnarray", needFont = True)
def lt_eqnarray(objs: list[list[LaTeXImage]], font: MixFont) -> LaTeXImage:
    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
    
    return new

@RegisterLaTeXEnvFunc("bmatrix", needFont = True, needColor = True)
def lt_bmatrix(objs: list[list[LaTeXImage]], font: MixFont, color) -> LaTeXImage:
    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1 = GetFontSize(font, "[")[0]
    s2 = GetFontSize(font, "]")[0]

    k = int(font.size // 10)
    ls = int(font.size // 20)
    
    new2 = LaTeXImage.new((new.width + s1 + s2, new.height + k *2), (255, 255, 255, 0))
    new2.alpha_composite(new, (s1, k))
    draw = LaTeXImageDraw.Draw(new2)

    for line in [
        (0, 0, s1, 0), (0, 0, 0, new2.height), (0, new2.height, s1, new2.height),
        (new2.width, 0, new2.width - s2, 0), (new2.width, 0, new2.width, new2.height), (new2.width, new2.height, new2.width - s2, new2.height)
    ]:
        draw.line(line, fill=color, width=ls)

    return new2

@RegisterLaTeXEnvFunc("pmatrix", needFont = True, needColor = True)
def lt_pmatrix(objs: list[list[LaTeXImage]], font: MixFont, color) -> LaTeXImage:
    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1,y1 = GetFontSize(font, "(")
    s2,y2 = GetFontSize(font, ")")
    img1 = LaTeXImage.new((s1, y1), (255, 255, 255, 0))
    img2 = LaTeXImage.new((s2, y2), (255, 255, 255, 0))
    draw1 = LaTeXImageDraw.Draw(img1)
    draw2 = LaTeXImageDraw.Draw(img2)
    draw1.text((0, 0), "(", font=font, fill=color)
    draw2.text((0, 0), ")", font=font, fill=color)

    new2 = LaTeXImage.new((new.width + s1 + s2, max(y1,y2,new.height)), (255, 255, 255, 0))

    img1 = img1.resize((img1.width, new2.height))
    img2 = img2.resize((img2.width, new2.height))

    new2.alpha_composite(img1, (0, (new2.height - img1.height) // 2))
    new2.alpha_composite(new, (img1.width, 0))
    new2.alpha_composite(img2, (new2.width - img2.width, (new2.height - img2.height) // 2))

    return new2

@RegisterLaTeXEnvFunc("vmatrix", needFont = True, needColor = True)
def lt_vmatrix(objs: list[list[LaTeXImage]], font: MixFont, color) -> LaTeXImage:
    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1 = GetFontSize(font, "[")[0]
    s2 = GetFontSize(font, "]")[0]

    k = int(font.size // 10)
    ls = int(font.size // 20)
    
    new2 = LaTeXImage.new((new.width + s1 + s2, new.height + k *2), (255, 255, 255, 0))
    new2.alpha_composite(new, (s1, k))
    draw = LaTeXImageDraw.Draw(new2)

    for line in [
        (0, 0, 0, new2.height), (new2.width, 0, new2.width, new2.height)
    ]:
        draw.line(line, fill=color, width=ls)

    return new2

@RegisterLaTeXEnvFunc("Vmatrix", needFont = True, needColor = True)
def lt_Vmatrix(objs: list[list[LaTeXImage]], font: MixFont, color) -> LaTeXImage:
    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1 = GetFontSize(font, "[")[0]
    s2 = GetFontSize(font, "]")[0]

    k = int(font.size // 10)
    ls = int(font.size // 20)
    
    new2 = LaTeXImage.new((new.width + s1 + s2, new.height + k *2), (255, 255, 255, 0))
    new2.alpha_composite(new, (s1, k))
    draw = LaTeXImageDraw.Draw(new2)

    for line in [
        (0, 0, 0, new2.height), (new2.width, 0, new2.width, new2.height),
        (s1//2, 0, s1//2, new2.height), (new2.width-s2//2, 0, new2.width-s2//2, new2.height)
    ]:
        draw.line(line, fill=color, width=ls)

    return new2

@RegisterLaTeXEnvFunc("Bmatrix", needFont = True, needColor = True)
def lt_Bmatrix(objs: list[list[LaTeXImage]], font: MixFont, color) -> LaTeXImage:
    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1 = GetFontSize(font, "{")[0]
    s2 = GetFontSize(font, "}")[0]

    k = int(font.size // 4)
    e = s1 // 2
    ls = int(font.size // 20)
    
    new2 = LaTeXImage.new((new.width + s1 + s2, new.height + k *2), (255, 255, 255, 0))
    new2.alpha_composite(new, (s1, k))
    draw = LaTeXImageDraw.Draw(new2)

    mid = new2.height // 2

    for line in [
        (e*2, 0, e, k), (e, k, e, mid - k), (e, mid - k, 0, mid), (0, mid, e, mid + k), (e, mid + k, e, new2.height - k), (e, new2.height - k, e*2, new2.height),
        (new2.width - e*2, 0, new2.width - e, k), (new2.width - e, k, new2.width - e, mid - k), (new2.width - e, mid - k, new2.width, mid), (new2.width, mid, new2.width - e, mid + k),  (new2.width - e, mid + k, new2.width - e, new2.height - k), (new2.width - e, new2.height - k, new2.width - e*2, new2.height),
    ]:
        draw.line(line, fill=color, width=ls)

    return new2

@RegisterLaTeXEnvFunc("cases", needFont = True, needColor = True)
def lt_cases(objs: list[list[LaTeXImage]], font: MixFont, color) -> LaTeXImage:
    k1 = font.size
    k2 = font.size // 2

    heights = [max([i.height for i in row]) for row in objs]
    widths = []

    for i in range(max([len(row) for row in objs])):
        max_width = 0
        for row in objs:
            if i < len(row):
                max_width = max(max_width, row[i].width)
        widths.append(max_width)
    
    new = LaTeXImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1 = GetFontSize(font, "{")[0]

    k = int(font.size // 4)
    e = s1 // 2
    ls = int(font.size // 20)
    
    new2 = LaTeXImage.new((new.width + s1, new.height + k *2), (255, 255, 255, 0))
    new2.alpha_composite(new, (s1, k))
    draw = LaTeXImageDraw.Draw(new2)

    mid = new2.height // 2

    for line in [
        (e*2, 0, e, k), (e, k, e, mid - k), (e, mid - k, 0, mid), (0, mid, e, mid + k), (e, mid + k, e, new2.height - k), (e, new2.height - k, e*2, new2.height)
    ]:
        draw.line(line, fill=color, width=ls)

    return new2