# PillowLaTeX

用于快速渲染大模型返回的latex表达式，支持`40`余种函数表达式及`10`余种环境以及`300`余种关键词替换

## 特点

轻量、易上手、快速、可自定义、纯python实现、支持切割渲染（既可以将表达式渲染成多个Image，供开发者手动拼接，以实现特定环境下的latex换行）

## 快速上手

使用pip：
```
pip install pillowmd
```

然后在代码中使用
```python
import pillowlatex as plax
# 导入

latex = r"表达式示例：sin^2(x\times\pi)"
# 表达式

# font = MixFont( # 混合字体
#     settings.FONT_PATH.parent / "STIXTwoMath-Regular.ttf", # 主字体
#     second_fonts = [ # 备用字体
#         settings.FONT_PATH.parent / "yahei.ttf",
#     ],
#     size = 50, # 字体大小
#     font_y_correct = {
#         "yahei.ttf": +15 # 偏移修正
#     }
# )

# 字体定义（可选）

img = plax.RenderLaTeX(
    GetLaTeXObjs(latex), # 对latex进行解析
    color = (255, 0, 0),
    # font = font
)

# 返回LaTeXImage对象

img.show()
```

说明：
`LaTeXImage`转化为`PIL.Image`的方式为
```python
img: LaTeXImage = ...
pilimage = img.img
```
需要注意的是，`img`的`size`，长和宽都比`pilimage`少`2*img.space`

## 已支持函数及大概效果

|函数|效果|
|-|-|
|frac|分数渲染|
|tfrac|更小的分数|
|cfrac|同frac|
|sqrt|根号渲染（可选开根数）|
|dot|一阶导数渲染|
|ddot|二阶导数渲染|
|pmode|模运算|
|sideset|侧标|
|hat|带帽`ˆ`|
|check|带帽`ˇ`|
|grave|带帽`|
|acute|带帽`´`|
|tilde|带帽`~`|
|breve|带帽`˘`|
|bar|带帽`¯`|
|vec|带帽`→`|
|not|叠加`⧸`|
|widetilde|`~`覆盖|
|widehat|`ˆ`覆盖|
|overleftarrow|`⟵`覆盖|
|overrightarrow|`⟶`覆盖|
|overline|上划线覆盖|
|underline|下划线覆盖|
|overbrace|上花括号覆盖|
|underbrace|下花括号覆盖|
|overset|上标渲染|
|underset|下标渲染|
|stackrel|堆叠渲染|
|overleftrightarrow|左右箭头覆盖|
|xleftarrow|左箭头覆盖|
|xrightarrow|右箭头覆盖|
|text|修改下一个元素类型为`text`|
|binom|二项式渲染|
|textstyle|修改下一个元素类型为`text`|
|unicode|渲染unicode文本|

## 已支持替换及大概效果

|元素|替换|
|-|-|
|\||替换为字符∥|
|(|替换为字符(|
|)|替换为字符)|
|[|替换为字符[|
|]|替换为字符]|
|{|替换为字符{|
|}|替换为字符}|
|lt|替换为字符<|
|gt|替换为字符>|
|leq|替换为字符≤|
|geq|替换为字符≥|
|neq|替换为字符≠|
|bmod|替换为字符mod|
|gcd|替换为字符gcd|
|lim|替换为字符lim|
|max|替换为字符max|
|min|替换为字符min|
|log|替换为字符log|
|ln|替换为字符ln|
|lg|替换为字符lg|
|exp|替换为字符exp|
|sup|替换为字符sup|
|inf|替换为字符inf|
|limsup|替换为字符lim sup|
|liminf|替换为字符lim inf|
|dim|替换为字符dim|
|ker|替换为字符ker|
|int|替换为字符∫|
|iint|替换为字符∬|
|iiint|替换为字符∭|
|oint|替换为字符∮|
|sum|替换为字符∑|
|prod|替换为字符∏|
|coprod|替换为字符∐|
|bigcap|替换为字符⋂|
|bigcup|替换为字符⋃|
|bigvee|替换为字符⋁|
|bigwedge|替换为字符⋀|
|lfloor|替换为字符⌊|
|rfloor|替换为字符⌋|
|lceil|替换为字符⌈|
|rceil|替换为字符⌉|
|langle|替换为字符⟨|
|rangle|替换为字符⟩|
|to|替换为字符→|
|sin|替换为字符sin|
|cos|替换为字符cos|
|tan|替换为字符tan|
|cot|替换为字符cot|
|sec|替换为字符sec|
|csc|替换为字符csc|
|arcsin|替换为字符arcsin|
|arccos|替换为字符arccos|
|arctan|替换为字符arctan|
|arccot|替换为字符arccot|
|arcsec|替换为字符arcsec|
|arccsc|替换为字符arccsc|
|sinh|替换为字符sinh|
|cosh|替换为字符cosh|
|tanh|替换为字符tanh|
|coth|替换为字符coth|
|sech|替换为字符sech|
|csch|替换为字符csch|
|times|替换为字符×|
|div|替换为字符÷|
|pm|替换为字符±|
|mp|替换为字符∓|
|triangleleft|替换为字符◁|
|triangleright|替换为字符▷|
|cdot|替换为字符⋅|
|setminus|替换为字符∖|
|star|替换为字符★|
|ast|替换为字符∗|
|cup|替换为字符∪|
|cap|替换为字符∩|
|sqcup|替换为字符⊔|
|sqcap|替换为字符⊓|
|vee|替换为字符∨|
|wedge|替换为字符∧|
|circ|替换为字符○|
|bullet|替换为字符•|
|oplus|替换为字符⊕|
|omuinus|替换为字符⊖|
|odot|替换为字符⊙|
|oslash|替换为字符⊘|
|otimes|替换为字符⊗|
|bigcirc|替换为字符◯|
|diamond|替换为字符◇|
|uplus|替换为字符⊎|
|bigtriangleup|替换为字符△|
|bigtriangledown|替换为字符▽|
|lhd|替换为字符⊲|
|rhd|替换为字符⊳|
|unlhd|替换为字符⊴|
|unrhd|替换为字符⊵|
|amalg|替换为字符⨿|
|wr|替换为字符≀|
|dagger|替换为字符†|
|ddagger|替换为字符‡|
|le|替换为字符≤|
|ge|替换为字符≥|
|equiv|替换为字符≡|
|ll|替换为字符≪|
|gg|替换为字符≫|
|doteq|替换为字符≐|
|prec|替换为字符≺|
|succ|替换为字符≻|
|sim|替换为字符∼|
|preceq|替换为字符≼|
|succeq|替换为字符≽|
|simeq|替换为字符≃|
|approx|替换为字符≈|
|subset|替换为字符⊂|
|supset|替换为字符⊃|
|subseteq|替换为字符⊆|
|supseteq|替换为字符⊇|
|sqsubset|替换为字符⊏|
|sqsupset|替换为字符⊐|
|sqsubseteq|替换为字符⊑|
|sqsupseteq|替换为字符⊒|
|cong|替换为字符≅|
|join|替换为字符⋈|
|bowtie|替换为字符⋈|
|propto|替换为字符∝|
|in|替换为字符∈|
|ni|替换为字符∋|
|vdash|替换为字符⊢|
|dashv|替换为字符⊣|
|models|替换为字符⊨|
|mid|替换为字符∣|
|parallel|替换为字符∥|
|perp|替换为字符⊥|
|smile|替换为字符⌣|
|frown|替换为字符⌢|
|asymp|替换为字符≍|
|notin|替换为字符∉|
|ne|替换为字符≠|
|gets|替换为字符←|
|longleftarrow|替换为字符⟵|
|longrightarrow|替换为字符⟶|
|uparrow|替换为字符↑|
|downarrow|替换为字符↓|
|updownarrow|替换为字符↕|
|leftrightarrow|替换为字符↔|
|Uparrow|替换为字符⇑|
|Downarrow|替换为字符⇓|
|Updownarrow|替换为字符⇕|
|longleftrightarrow|替换为字符⟷|
|Leftarrow|替换为字符⇐|
|Longleftarrow|替换为字符⟸|
|Rightarrow|替换为字符⇒|
|Longrightarrow|替换为字符⟹|
|Leftrightarrow|替换为字符⇔|
|Longleftrightarrow|替换为字符⟺|
|mapsto|替换为字符↦|
|longmapsto|替换为字符⟼|
|nearrow|替换为字符↗|
|searrow|替换为字符↘|
|swarrow|替换为字符↙|
|nwarrow|替换为字符↖|
|hookleftarrow|替换为字符↩|
|hookrightarrow|替换为字符↪|
|rightleftharpoons|替换为字符⇌|
|iff|替换为字符⇔|
|leftharpoonup|替换为字符↼|
|leftharpoondown|替换为字符↽|
|rightharpoonup|替换为字符⇀|
|rightharpoondown|替换为字符⇁|
|because|替换为字符∵|
|therefore|替换为字符∴|
|dots|替换为字符…|
|cdots|替换为字符⋯|
|vdots|替换为字符⋮|
|ddots|替换为字符⋱|
|forall|替换为字符∀|
|exists|替换为字符∃|
|nexists|替换为字符∄|
|Finv|替换为字符Ⅎ|
|neg|替换为字符¬|
|prime|替换为字符′|
|emptyset|替换为字符∅|
|infty|替换为字符∞|
|nabla|替换为字符∇|
|triangle|替换为字符△|
|Box|替换为字符□|
|Diamond|替换为字符◇|
|bot|替换为字符⊥|
|top|替换为字符⊤|
|angle|替换为字符∠|
|measuredangle|替换为字符∡|
|sphericalangle|替换为字符∢|
|surd|替换为字符√|
|diamondsuit|替换为字符♢|
|heartsuit|替换为字符♡|
|clubsuit|替换为字符♣|
|spadesuit|替换为字符♠|
|flat|替换为字符♭|
|natural|替换为字符♮|
|sharp|替换为字符♯|
|alpha|替换为字符α|
|beta|替换为字符β|
|gamma|替换为字符γ|
|delta|替换为字符ℸ|
|epsilon|替换为字符ε|
|varepsilon|替换为字符ϵ|
|zeta|替换为字符ζ|
|eta|替换为字符η|
|theta|替换为字符θ|
|vartheta|替换为字符ϑ|
|iota|替换为字符ι|
|kappa|替换为字符κ|
|lambda|替换为字符λ|
|mu|替换为字符μ|
|nu|替换为字符ν|
|xi|替换为字符ξ|
|pi|替换为字符π|
|varpi|替换为字符ϖ|
|rho|替换为字符ρ|
|varrho|替换为字符ϱ|
|sigma|替换为字符σ|
|varsigma|替换为字符ς|
|tau|替换为字符τ|
|upsilon|替换为字符υ|
|phi|替换为字符φ|
|varphi|替换为字符ϕ|
|chi|替换为字符χ|
|psi|替换为字符ψ|
|omega|替换为字符ω|
|Gamma|替换为字符Γ|
|Delta|替换为字符Δ|
|Theta|替换为字符Θ|
|Lambda|替换为字符Λ|
|Xi|替换为字符Ξ|
|Pi|替换为字符Π|
|Sigma|替换为字符Σ|
|Upsilon|替换为字符Υ|
|Phi|替换为字符Φ|
|Psi|替换为字符Ψ|
|Omega|替换为字符Ω|
|hbar|替换为字符ℏ|
|imath|替换为字符ı|
|jmath|替换为字符ȷ|
|ell|替换为字符ℓ|
|Re|替换为字符ℜ|
|Im|替换为字符ℑ|
|aleph|替换为字符ℵ|
|beth|替换为字符ℶ|
|gimel|替换为字符ℷ|
|wp|替换为字符℘|
|mho|替换为字符℧|
|backepsilon|替换为字符϶|
|partial|替换为字符∂|
|eth|替换为字符ð|
|Bbbk|替换为字符𝕜|
|complement|替换为字符∁|
|circledS|替换为字符Ⓢ|
|S|替换为字符§|

## 已支持环境

|环境|
|-|
|matrix|
|align*|
|align|
|array|
|eqnarray|
|bmatrix|
|pmatrix|
|vmatrix|
|Vmatrix|
|Bmatrix|
|cases|

## 会被直接屏蔽|返回原图的函数

|函数|效果|
|-|-|
|mathrm|返回原图|
|operatorname|返回原图|

## 暂不支持的内容（屏蔽）

|内容|
|-|
|mathbf|
|mathbb|
|tiny|
|scriptsize|
|footnotesize|
|small|
|normalsize|
|large|
|Large|
|LARGE|
|huge|
|Huge|
|nolimits|
|mathop|
|ce|

## 其他支持

|内容|是否支持|
|-|-|
|环境嵌套|支持|
|left与right|支持|
|上标下标位置修改|支持|