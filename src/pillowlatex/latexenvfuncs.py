from .latex import(
    RegisterLaTexEnvFunc, LaTexImage, LaTexImageDraw, GetFontSize, MixFont, GetLaTexTextObj
)
from typing import Union

@RegisterLaTexEnvFunc("matrix", needFont = True)
def lt_matrix(objs: list[list[LaTexImage]], font: MixFont) -> LaTexImage:
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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
    
    return new

@RegisterLaTexEnvFunc("align*", needFont = True)
def lt_aligns(objs: list[list[LaTexImage]], font: MixFont) -> LaTexImage:
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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
    
    return new

@RegisterLaTexEnvFunc("align", needFont = True)
def lt_align(objs: list[list[LaTexImage]], font: MixFont) -> LaTexImage:
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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
    
    return new

@RegisterLaTexEnvFunc("array", needFont = True)
def lt_array(mode: Union[str, list], objs: list[list[LaTexImage]], font: MixFont) -> LaTexImage:

    m = GetLaTexTextObj(mode)

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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            if m == "l":
                new.alpha_composite(img, (int(sum(widths[:j]) + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
            elif m == "r":
                new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
            else:
                new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
    
    return new

@RegisterLaTexEnvFunc("eqnarray", needFont = True)
def lt_eqnarray(objs: list[list[LaTexImage]], font: MixFont) -> LaTexImage:
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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))
    
    return new

@RegisterLaTexEnvFunc("bmatrix", needFont = True, needColor = True)
def lt_bmatrix(objs: list[list[LaTexImage]], font: MixFont, color) -> LaTexImage:
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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1 = GetFontSize(font, "[")[0]
    s2 = GetFontSize(font, "]")[0]

    k = int(font.size // 10)
    ls = int(font.size // 20)
    
    new2 = LaTexImage.new((new.width + s1 + s2, new.height + k *2), (255, 255, 255, 0))
    new2.alpha_composite(new, (s1, k))
    draw = LaTexImageDraw.Draw(new2)

    for line in [
        (0, 0, s1, 0), (0, 0, 0, new2.height), (0, new2.height, s1, new2.height),
        (new2.width, 0, new2.width - s2, 0), (new2.width, 0, new2.width, new2.height), (new2.width, new2.height, new2.width - s2, new2.height)
    ]:
        draw.line(line, fill=color, width=ls)

    return new2

@RegisterLaTexEnvFunc("pmatrix", needFont = True, needColor = True)
def lt_pmatrix(objs: list[list[LaTexImage]], font: MixFont, color) -> LaTexImage:
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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1,y1 = GetFontSize(font, "(")
    s2,y2 = GetFontSize(font, ")")
    img1 = LaTexImage.new((s1, y1), (255, 255, 255, 0))
    img2 = LaTexImage.new((s2, y2), (255, 255, 255, 0))
    draw1 = LaTexImageDraw.Draw(img1)
    draw2 = LaTexImageDraw.Draw(img2)
    draw1.text((0, 0), "(", font=font, fill=color)
    draw2.text((0, 0), ")", font=font, fill=color)

    new2 = LaTexImage.new((new.width + s1 + s2, max(y1,y2,new.height)), (255, 255, 255, 0))

    img1 = img1.resize((img1.width, new2.height))
    img2 = img2.resize((img2.width, new2.height))

    new2.alpha_composite(img1, (0, (new2.height - img1.height) // 2))
    new2.alpha_composite(new, (img1.width, 0))
    new2.alpha_composite(img2, (new2.width - img2.width, (new2.height - img2.height) // 2))

    return new2

@RegisterLaTexEnvFunc("vmatrix", needFont = True, needColor = True)
def lt_vmatrix(objs: list[list[LaTexImage]], font: MixFont, color) -> LaTexImage:
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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1 = GetFontSize(font, "[")[0]
    s2 = GetFontSize(font, "]")[0]

    k = int(font.size // 10)
    ls = int(font.size // 20)
    
    new2 = LaTexImage.new((new.width + s1 + s2, new.height + k *2), (255, 255, 255, 0))
    new2.alpha_composite(new, (s1, k))
    draw = LaTexImageDraw.Draw(new2)

    for line in [
        (0, 0, 0, new2.height), (new2.width, 0, new2.width, new2.height)
    ]:
        draw.line(line, fill=color, width=ls)

    return new2

@RegisterLaTexEnvFunc("Vmatrix", needFont = True, needColor = True)
def lt_Vmatrix(objs: list[list[LaTexImage]], font: MixFont, color) -> LaTexImage:
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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1 = GetFontSize(font, "[")[0]
    s2 = GetFontSize(font, "]")[0]

    k = int(font.size // 10)
    ls = int(font.size // 20)
    
    new2 = LaTexImage.new((new.width + s1 + s2, new.height + k *2), (255, 255, 255, 0))
    new2.alpha_composite(new, (s1, k))
    draw = LaTexImageDraw.Draw(new2)

    for line in [
        (0, 0, 0, new2.height), (new2.width, 0, new2.width, new2.height),
        (s1//2, 0, s1//2, new2.height), (new2.width-s2//2, 0, new2.width-s2//2, new2.height)
    ]:
        draw.line(line, fill=color, width=ls)

    return new2

@RegisterLaTexEnvFunc("Bmatrix", needFont = True, needColor = True)
def lt_Bmatrix(objs: list[list[LaTexImage]], font: MixFont, color) -> LaTexImage:
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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1 = GetFontSize(font, "{")[0]
    s2 = GetFontSize(font, "}")[0]

    k = int(font.size // 4)
    e = s1 // 2
    ls = int(font.size // 20)
    
    new2 = LaTexImage.new((new.width + s1 + s2, new.height + k *2), (255, 255, 255, 0))
    new2.alpha_composite(new, (s1, k))
    draw = LaTexImageDraw.Draw(new2)

    mid = new2.height // 2

    for line in [
        (e*2, 0, e, k), (e, k, e, mid - k), (e, mid - k, 0, mid), (0, mid, e, mid + k), (e, mid + k, e, new2.height - k), (e, new2.height - k, e*2, new2.height),
        (new2.width - e*2, 0, new2.width - e, k), (new2.width - e, k, new2.width - e, mid - k), (new2.width - e, mid - k, new2.width, mid), (new2.width, mid, new2.width - e, mid + k),  (new2.width - e, mid + k, new2.width - e, new2.height - k), (new2.width - e, new2.height - k, new2.width - e*2, new2.height),
    ]:
        draw.line(line, fill=color, width=ls)

    return new2

@RegisterLaTexEnvFunc("cases", needFont = True, needColor = True)
def lt_cases(objs: list[list[LaTexImage]], font: MixFont, color) -> LaTexImage:
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
    
    new = LaTexImage.new((int(sum(widths) + k1 * (len(widths) - 1)), int(sum(heights) + k2 * (len(heights) - 1))), (255, 255, 255, 0))

    for i, row in enumerate(objs):
        for j, img in enumerate(row):
            new.alpha_composite(img, (int(sum(widths[:j]) + (widths[j] - img.width) // 2 + k1 * j), int(sum(heights[:i]) + (heights[i] - img.height) // 2 + k2 * i)))

    s1 = GetFontSize(font, "{")[0]

    k = int(font.size // 4)
    e = s1 // 2
    ls = int(font.size // 20)
    
    new2 = LaTexImage.new((new.width + s1, new.height + k *2), (255, 255, 255, 0))
    new2.alpha_composite(new, (s1, k))
    draw = LaTexImageDraw.Draw(new2)

    mid = new2.height // 2

    for line in [
        (e*2, 0, e, k), (e, k, e, mid - k), (e, mid - k, 0, mid), (0, mid, e, mid + k), (e, mid + k, e, new2.height - k), (e, new2.height - k, e*2, new2.height)
    ]:
        draw.line(line, fill=color, width=ls)

    return new2