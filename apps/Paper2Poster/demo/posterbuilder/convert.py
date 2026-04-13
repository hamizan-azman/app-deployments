# build_poster.py  /  convert.py
# -*- coding: utf-8 -*-
import json, re, pathlib, shutil, os, math

# ===================== 自动定位项目根 =====================
IMAGES_DIR_NAME = "<gpt-5_gpt-5>_images_and_tables"  # 蓝色文件夹名

def find_project_root(start: pathlib.Path) -> pathlib.Path:
    cur = start.resolve()
    for p in [cur] + list(cur.parents):
        if (p / "Paper2Poster").exists() or (p / "Paper2Video").exists():
            return p
        if (p / IMAGES_DIR_NAME).exists():
            return p
        if (p / "posterbuilder" / "cambridge_template.tex").exists():
            return p
    return cur

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR   = find_project_root(SCRIPT_DIR)
TEST_DIR   = ROOT_DIR / "posterbuilder"

# ===================== 路径（全部相对 ROOT_DIR） =====================
JSON_PATH        = TEST_DIR / "contents" / "poster_content.json"
TEMPLATE_PATH    = TEST_DIR / "cambridge_template.tex"
ARRANGEMENT_PATH = TEST_DIR / "contents" / "arrangement.json"
CAPTION_PATH     = TEST_DIR / "contents" / "figure_caption.json"

OUTPUT_DIR       = TEST_DIR / "latex_proj"
OUTPUT_PATH      = OUTPUT_DIR / "poster_output.tex"

# 图片父目录（关键修正）：默认 Paper2Poster/，找不到再退回 ROOT_DIR/
IMAGES_PARENTS   = [ROOT_DIR / "Paper2Poster", ROOT_DIR]

# ============ 放大与排版参数 ============
BEAMER_SCALE_TARGET   = 1.0      # 模板 \usepackage{beamerposter}[... scale=...] 的新值
# 标题字号策略：单行、两行、3+ 行
TITLE_SIZE_SINGLE     = r"\Huge"
TITLE_SIZE_WRAP1      = r"\huge"
TITLE_SIZE_WRAP2PLUS  = r"\LARGE"

AUTHOR_SIZE_CMD       = r"\Large"
INSTITUTE_SIZE_CMD    = r"\large"
BLOCK_TITLE_SIZE_CMD  = r"\Large"
BLOCK_BODY_SIZE_CMD   = r"\large"
CAPTION_SIZE_CMD      = r"\small"

# 图像放大基础参数（初值）
FIG_ENLARGE_FACTOR    = 1.18
FIG_MIN_FRAC          = 0.80
FIG_MAX_FRAC          = 0.90

# 预算控制：每个 section 内，图像累计“高度占 panel 高度”的允许上限（会根据字数自适应）
BASE_FIG_RATIO_LIMIT  = 0.58  # 基准阈值
TEXT_CHAR_PER_LINE    = 95    # 估算一行容纳的字符数（粗略）
LINE_HEIGHT_WEIGHT    = 0.015 # 转换“正文行数”为“面板高度比例”的权重（经验系数）

# 右上角 logo
RIGHT_LOGO_FILENAME   = "logo.png"  # 位于 latex_proj/ 下
RIGHT_LOGO_HEIGHT_CM  = 6.0
RIGHT_LOGO_INNERSEP_CM= 2.0
RIGHT_LOGO_XSHIFT_CM  = -2.0
RIGHT_LOGO_YSHIFT_CM  = 0.0

# NEW: 规范器——把 \textit{...} 中“数学样式”的内容自动切到数学模式
MATH_BLOCK_RE = re.compile(
    r"\${1,2}.*?\${1,2}"           # $...$ 或 $$...$$
    r"|\\\(.+?\\\)"                # \( ... \)
    r"|\\\[(?:.|\n)+?\\\]",        # \[ ... \] （跨行）
    re.S
)

# 常见希腊字母/数学宏，用于识别 \textit{\tau} 这类情况
GREEK_OR_MATH_MACROS = (
    r"alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|iota|kappa|lambda|"
    r"mu|nu|xi|pi|varpi|rho|varrho|sigma|varsigma|tau|upsilon|phi|varphi|chi|psi|omega|"
    r"Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Upsilon|Phi|Psi|Omega"
)

MATH_INLINE_MACROS = (
    GREEK_OR_MATH_MACROS  
    + r"|partial|nabla|infty|cdot|times|pm|leq|geq|ldots|dots"
)

_MACRO_OUTSIDE_MATH_RE = re.compile(
    rf"(\\(?:{MATH_INLINE_MACROS}))"          # \delta / \tau / \cdot / ...
    rf"(?:\s*[A-Za-z])?",                     # 允许后面紧跟一个字母变量（如 \delta c）
)

_BULLET_RE = re.compile(r"•")

# ===================== 基础工具 =====================
# 覆盖的数学块（全局已有 MATH_BLOCK_RE，可以复用）
def wrap_math_macros_outside_math(s: str) -> str:
    """
    目的：在“非数学环境”里遇到数学宏时，自动加上 $...$。
    例如：\delta c  ->  $\delta c$
          \tau      ->  $\tau$
    已有的 $...$ / \[...\] / \(...\) 不会被二次处理（先暂存）。
    """
    if not s:
        return s

    # 1) 暂存已有数学块
    stash = []
    def _hide(m):
        stash.append(m.group(0))
        return f"\x00M{len(stash)-1}\x00"
    s_hidden = MATH_BLOCK_RE.sub(_hide, s)

    # 2) 把裸奔宏包进 $...$
    def _wrap(m):
        return f"${m.group(0)}$"
    s_hidden = _MACRO_OUTSIDE_MATH_RE.sub(_wrap, s_hidden)

    # 3) 还原数学块
    for i, blk in enumerate(stash):
        s_hidden = s_hidden.replace(f"\x00M{i}\x00", blk)

    return s_hidden


def wrap_math_macros_outside_math(s: str) -> str:
    """
    目的：在“非数学环境”里遇到数学宏时，自动加上 $...$。
    例如：\delta c  ->  $\delta c$
          \tau      ->  $\tau$
    已有的 $...$ / \[...\] / \(...\) 不会被二次处理（先暂存）。
    """
    if not s:
        return s

    # 1) 暂存已有数学块
    stash = []
    def _hide(m):
        stash.append(m.group(0))
        return f"\x00M{len(stash)-1}\x00"
    s_hidden = MATH_BLOCK_RE.sub(_hide, s)

    # 2) 把裸奔宏包进 $...$
    def _wrap(m):
        return f"${m.group(0)}$"
    s_hidden = _MACRO_OUTSIDE_MATH_RE.sub(_wrap, s_hidden)

    # 3) 还原数学块
    for i, blk in enumerate(stash):
        s_hidden = s_hidden.replace(f"\x00M{i}\x00", blk)

    return s_hidden


_BULLET_RE = re.compile(r"•")

def normalize_inline_bullets(s: str) -> str:
    """
    把 Unicode 的 • 统一替换为 LaTeX 的 \\textbullet{}，并确保两侧留空格。
    """
    if not s:
        return s
    s = _BULLET_RE.sub(r"\\textbullet{}", s)
    # 若两侧无空格，补空格（避免“黏连”）
    s = re.sub(r"(?<=\S)\\textbullet\{\}(?=\S)", r" \\textbullet{} ", s)
    s = re.sub(r"\\textbullet\{\}(?=\S)", r"\\textbullet{} ", s)
    s = re.sub(r"(?<=\S)\\textbullet\{\}", r" \\textbullet{}", s)
    return s

def normalize_textit_math(s: str) -> str:
    """
    目的：
      - \textit{\tau}   -> $\tau$
      - \textit{c}(\tau) -> $c(\tau)$
      - \textit{c}       -> $c$
    规则：
      - 先屏蔽已有数学块，避免误处理
      - 仅把“单字母变量”或“以反斜杠开头的数学命令”从 \textit{...} 切换到数学模式
      - 不碰 \textit{SST} 这类普通词
    """
    if not s:
        return s

    # 1) 屏蔽现有数学块
    stash = []
    def _hide(m):
        stash.append(m.group(0))
        return f"\x00M{len(stash)-1}\x00"
    s = MATH_BLOCK_RE.sub(_hide, s)

    # 2a) \textit{\tau}、\textit{\zeta} ... -> $\tau$、$\zeta$
    s = re.sub(
        rf"\\textit\{{\s*(\\(?:{GREEK_OR_MATH_MACROS})\b[^\}}]*)\s*\}}",
        r"$\1$",
        s
    )

    # 2b) \textit{c}(\tau) 这种：单字母 + 直接跟括号表达式 -> $c(\tau)$
    s = re.sub(
        r"\\textit\{\s*([A-Za-z])\s*\}\s*\(\s*([^()$]+?)\s*\)",
        r"$\1(\2)$",
        s
    )

    # 2c) \textit{c}_0 或 \textit{q}^T 这种：把后续下/上标一并包进数学
    s = re.sub(
        r"\\textit\{\s*([A-Za-z])\s*\}\s*([_^]\s*(?:\{[^{}]*\}|[A-Za-z0-9]))",
        r"$\1\2$",
        s
    )

    # 2d) 单字母变量：\textit{c} / \textit{q} / \textit{X} -> $c$/$q$/$X$
    s = re.sub(
        r"\\textit\{\s*([A-Za-z])\s*\}",
        r"$\1$",
        s
    )

    # 3) 还原数学块
    for i, blk in enumerate(stash):
        s = s.replace(f"\x00M{i}\x00", blk)

    return s

def fix_latex_escaped_commands(s: str) -> str:
    """
    修复由于 \t 被错误解析而导致的 LaTeX 命令丢失反斜杠问题，
    例如将 "extbf{" -> "\textbf{"，并修正 "\}" -> "}"。
    """
    if not s:
        return s
    # 修复常见命令
    s = re.sub(r'(?<!\\)extbf\{', r'\\textbf{', s)
    s = re.sub(r'(?<!\\)extit\{', r'\\textit{', s)
    s = re.sub(r'(?<!\\)extcolor\{', r'\\textcolor{', s)
    s = re.sub(r'(?<!\\)exttt\{', r'\\texttt{', s)
    s = re.sub(r'(?<!\\)extsc\{', r'\\textsc{', s)
    s = re.sub(r'(?<!\\)extsuperscript\{', r'\\textsuperscript{', s)
    s = re.sub(r'(?<!\\)extsubscript\{', r'\\textsubscript{', s)
    # 修复 \} 被错误转义
    s = s.replace("\\}", "}")
    return s


def escape_text(s: str) -> str:
    if not s:
        return ""

    # --- 1) 捕获所有数学块（沿用全局 MATH_BLOCK_RE）----
    math_blocks = []
    def store_math(m):
        math_blocks.append(m.group(0))
        return f"\0{len(math_blocks)-1}\0"

    s = MATH_BLOCK_RE.sub(store_math, s)

    # --- 2) 转义文本字符（不碰 math） ----
    rep = {
        "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
        "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"~{}", "^": r"\^{}",
    }
    for k, v in rep.items():
        s = s.replace(k, v)

    # --- 3) 恢复 math ----
    for i, block in enumerate(math_blocks):
        s = s.replace(f"\0{i}\0", block)

    return s




def soft_wrap_title_for_logo(title: str, first_limit=68, next_limit=72) -> str:
    if not title or len(title) <= first_limit: return title
    def break_at(s: str, limit: int):
        for sep in [": ", " - ", " — ", " – "]:
            idx = s.rfind(sep, 0, limit+1)
            if idx != -1: return s[:idx+len(sep)].rstrip(), s[idx+len(sep):].lstrip()
        idx = s.rfind(" ", 0, limit+1)
        if idx == -1: idx = limit
        return s[:idx].rstrip(), s[idx:].lstrip()
    head, rest = break_at(title, first_limit); parts = [head]
    if rest:
        if len(rest) > next_limit:
            mid, tail = break_at(rest, next_limit); parts.append(mid); 
            if tail: parts.append(tail)
        else: parts.append(rest)
    return r" \\ ".join(parts)

def replace_command_balanced(tex: str, cmd: str, new_line: str) -> str:
    m = re.search(rf"\\{cmd}\b", tex)
    if not m: return tex
    i = m.end()
    if i < len(tex) and tex[i] == '[':
        depth = 1; i += 1
        while i < len(tex) and depth:
            if tex[i] == '[': depth += 1
            elif tex[i] == ']': depth -= 1
            i += 1
        while i < len(tex) and tex[i].isspace(): i += 1
    if i >= len(tex) or tex[i] != '{': return tex
    start = m.start(); j = i; depth = 0; end = None
    while j < len(tex):
        if tex[j] == '{': depth += 1
        elif tex[j] == '}':
            depth -= 1
            if depth == 0: end = j; break
        j += 1
    if end is None: return tex
    return tex[:start] + new_line + tex[end+1:]

def format_content_to_latex(content: str) -> str:
    """格式化正文内容，自动修复 LaTeX 命令"""
    if not content:
        return ""

    # 1) 先修复 \t 造成的命令断头
    content = fix_latex_escaped_commands(content)

    # 2) 规范 \textit{...} 里的“伪数学”
    content = normalize_textit_math(content)

    # 3) **把非数学环境的数学宏包进 $...$**  ← NEW（修正 \delta c）
    content = wrap_math_macros_outside_math(content)

    # 之后再进行 itemize 的识别与转义
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    if lines and all(ln.startswith(("-", "•")) for ln in lines):
        items = [escape_text(ln.lstrip("-• ").strip()) for ln in lines]
        return "\n".join(["\\begin{itemize}"] + [f"\\item {it}" for it in items] + ["\\end{itemize}"])

    return escape_text(" ".join(lines))


def make_block(title: str, content: str, figures_tex: str = "") -> str:
    body = format_content_to_latex(content or "")
    if figures_tex: body = (body + "\n\n" if body else "") + figures_tex
    return f"\\begin{{block}}{{{escape_text(title or '')}}}\n{body}\n\\end{{block}}\n"

# ----- 标题字号挑选（新增） -----
def choose_title_size_cmd(wrapped_title: str) -> str:
    breaks = wrapped_title.count("\\\\")
    if breaks == 0:
        return TITLE_SIZE_SINGLE
    elif breaks == 1:
        return TITLE_SIZE_WRAP1
    else:
        return TITLE_SIZE_WRAP2PLUS

def build_header_from_meta(meta: dict):
    raw_title = meta.get('poster_title','') or ''
    wrapped_title = soft_wrap_title_for_logo(raw_title)
    t = f"\\title{{{escape_text(wrapped_title)}}}"
    a = f"\\author{{{escape_text(meta.get('authors',''))}}}"
    inst = f"\\institute[shortinst]{{{escape_text(meta.get('affiliations',''))}}}"
    # 返回 wrapped_title 以便后续动态字号
    return t, a, inst, wrapped_title

# ===================== LaTeX 环境处理/模板增强 =====================
def find_env_bounds(tex: str, env: str, start_pos: int):
    pat = re.compile(rf"\\(begin|end)\{{{re.escape(env)}\}}")
    depth = 0; begin_idx = None
    for m in pat.finditer(tex, start_pos):
        if m.group(1) == "begin":
            if depth == 0: begin_idx = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end_idx = m.end()
                return begin_idx, end_idx
    return None, None

def extract_begin_token_with_options(region: str, env: str) -> str:
    m = re.match(rf"(\\begin\{{{re.escape(env)}\}}\s*(?:\[[^\]]*\])?)", region, re.S)
    return m.group(1) if m else f"\\begin{{{env}}}"

def split_even_continuous(blocks: list[str], n_cols: int) -> list[list[str]]:
    n = len(blocks); base = n // n_cols; rem = n % n_cols
    sizes = [(base + 1 if i < rem else base) for i in range(n_cols)]
    out, idx = [], 0
    for sz in sizes:
        out.append(blocks[idx: idx+sz]); idx += sz
    return out

def rebuild_first_columns_region_to_three(tex: str, blocks_latex: list[str]) -> str:
    pos_doc = tex.find(r"\begin{document}")
    if pos_doc == -1:
        raise RuntimeError("未找到 \\begin{document}")
    begin_idx, end_idx = find_env_bounds(tex, "columns", pos_doc)
    if begin_idx is None:
        raise RuntimeError("未在文档主体找到 \\begin{columns} ... \\end{columns}")
    region = tex[begin_idx:end_idx]
    begin_token = extract_begin_token_with_options(region, "columns")
    per_col_blocks = split_even_continuous(blocks_latex, 3)
    body_lines = []
    for i in range(3):
        body_lines.append(r"\separatorcolumn")
        body_lines.append(r"\begin{column}{\colwidth}")
        if per_col_blocks[i]: body_lines.append("\n".join(per_col_blocks[i]))
        body_lines.append(r"\end{column}")
    body_lines.append(r"\separatorcolumn")
    new_region = begin_token + "\n" + "\n".join(body_lines) + "\n\\end{columns}"
    return tex[:begin_idx] + new_region + tex[end_idx:]

def bump_beamerposter_scale(tex: str, target: float) -> str:
    def repl(m):
        opts = m.group(1)
        if re.search(r"scale\s*=\s*[\d.]+", opts):
            opts2 = re.sub(r"scale\s*=\s*[\d.]+", f"scale={target}", opts)
        else:
            if opts.strip().endswith(","): opts2 = opts + f"scale={target}"
            elif opts.strip()=="": opts2 = f"scale={target}"
            else: opts2 = opts + f",scale={target}"
        return f"\\usepackage[{opts2}]{{beamerposter}}"
    return re.sub(r"\\usepackage\[(.*?)\]\{beamerposter\}", repl, tex, flags=re.S)

def inject_font_tweaks(tex: str, title_size_cmd: str) -> str:
    """在 \begin{document} 前注入字号设置（标题字号可动态传入）"""
    tweaks = (
        "\n% --- injected font tweaks ---\n"
        f"\\setbeamerfont{{title}}{{size={title_size_cmd}}}\n"
        f"\\setbeamerfont{{author}}{{size={AUTHOR_SIZE_CMD}}}\n"
        f"\\setbeamerfont{{institute}}{{size={INSTITUTE_SIZE_CMD}}}\n"
        f"\\setbeamerfont{{block title}}{{size={BLOCK_TITLE_SIZE_CMD}}}\n"
        f"\\setbeamerfont{{block body}}{{size={BLOCK_BODY_SIZE_CMD}}}\n"
        # f"\\setbeamerfont{{caption}}{{size={CAPTION_SIZE_CMD}}}\n"
        # "\\setlength{\\abovecaptionskip}{4pt}\n"
        # "\\setlength{\\belowcaptionskip}{3pt}\n"
    )
    pos_doc = tex.find(r"\begin{document}")
    return tex[:pos_doc] + tweaks + tex[pos_doc:] if pos_doc != -1 else tex + tweaks

def inject_right_logo(tex: str) -> str:
    if "logo.png" in tex:
        return tex
    pos_head = tex.find(r"\addtobeamertemplate{headline}")
    node = (
        f"\n      \\node[anchor=north east, inner sep={RIGHT_LOGO_INNERSEP_CM}cm]"
        f" at ([xshift={RIGHT_LOGO_XSHIFT_CM}cm,yshift={RIGHT_LOGO_YSHIFT_CM}cm]current page.north east)\n"
        f"      {{\\includegraphics[height={RIGHT_LOGO_HEIGHT_CM}cm]{{{RIGHT_LOGO_FILENAME}}}}};\n"
    )
    if pos_head != -1:
        begin_tikz = tex.find(r"\begin{tikzpicture}", pos_head)
        if begin_tikz != -1:
            b, e = find_env_bounds(tex, "tikzpicture", begin_tikz)
            if b is not None:
                region = tex[b:e]
                pos_end = region.rfind(r"\end{tikzpicture}")
                if pos_end != -1:
                    insert_at = b + pos_end
                    return tex[:insert_at] + node + tex[insert_at:]
    add_block = (
        "\n% --- injected right-top logo ---\n"
        "\\addtobeamertemplate{headline}{}\n"
        "{\n"
        "  \\begin{tikzpicture}[remember picture,overlay]\n"
        f"    \\node[anchor=north east, inner sep={RIGHT_LOGO_INNERSEP_CM}cm]"
        f" at ([xshift={RIGHT_LOGO_XSHIFT_CM}cm,yshift={RIGHT_LOGO_YSHIFT_CM}cm]current page.north east)\n"
        f"    {{\\includegraphics[height={RIGHT_LOGO_HEIGHT_CM}cm]{{{RIGHT_LOGO_FILENAME}}}}};\n"
        "  \\end{tikzpicture}\n"
        "}\n"
    )
    pos_doc = tex.find(r"\begin{document}")
    return tex[:pos_doc] + add_block + tex[pos_doc:] if pos_doc != -1 else tex + add_block

# ===================== 图片与 captions（相对 PaperShow/） =====================
def load_arrangement_and_captions():
    arr = json.loads(ARRANGEMENT_PATH.read_text(encoding="utf-8"))
    panels = arr.get("panels", [])
    figures = arr.get("figure_arrangement", [])
    panels_by_id = {p["panel_id"]: p for p in panels if "panel_id" in p}

    cap_map_full, cap_map_base = {}, {}
    if CAPTION_PATH.exists():
        caps = json.loads(CAPTION_PATH.read_text(encoding="utf-8"))
        if isinstance(caps, dict):
            for _, v in caps.items():
                imgp = v.get("image_path", ""); cap = v.get("caption", "")
                if imgp:
                    cap_map_full[imgp] = cap
                    cap_map_base[os.path.basename(imgp)] = cap
    return panels_by_id, figures, cap_map_full, cap_map_base

def resolve_images_parent_dir(sample_fig_paths) -> pathlib.Path:
    for parent in IMAGES_PARENTS:
        for sp in sample_fig_paths[:10]:
            if sp:
                p = parent / sp
                if p.exists():
                    return parent
    return IMAGES_PARENTS[0]

def copy_and_get_relpath(figure_path: str, out_tex_path: pathlib.Path, images_parent: pathlib.Path) -> str:
    fig_dir = out_tex_path.parent / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    p = pathlib.Path(figure_path)
    if p.is_absolute():
        src = p
    else:
        if p.parts and p.parts[0] == IMAGES_DIR_NAME:
            src = images_parent / p
        else:
            src = images_parent / IMAGES_DIR_NAME / p
    dst = fig_dir / src.name
    try:
        if src.exists():
            if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
                shutil.copy2(src, dst)
    except Exception:
        pass
    return str(pathlib.Path("figures") / dst.name).replace(os.sep, "/")

def norm_title(s: str) -> str:
    return " ".join((s or "").lower().replace("&", "and").split())

# ---- 新增：清洗 caption 开头的 "Figure X:" / "Fig. X." ----
CAP_PREFIX_RE = re.compile(
    r'^\s*(?:figure|fig\.?)\s*\d+(?:\s*[a-z]\)|\s*[a-z])?\s*[:：\.\-–—]\s*',
    re.IGNORECASE
)

def clean_caption_prefix(cap: str) -> str:
    if not cap: return ""
    return CAP_PREFIX_RE.sub("", cap).strip()

def build_figures_for_sections(sections, panels_by_id, figures, cap_full, cap_base):
    sec_name_to_idx = {norm_title(sec.get("title","")): i
                       for i, sec in enumerate(sections)
                       if norm_title(sec.get("title","")) != norm_title("Poster Title & Author")}
    panelid_to_secidx = {}
    for p in panels_by_id.values():
        pname = norm_title(p.get("section_name",""))
        if pname in sec_name_to_idx:
            panelid_to_secidx[p["panel_id"]] = sec_name_to_idx[pname]

    # 收集：每 section 的 panel 高度、以及该 panel 下图的“安排高度总和”
    sec_panel_height = {}
    sec_arranged_fig_height = {}
    for pid, pinfo in panels_by_id.items():
        if pid in panelid_to_secidx:
            sidx = panelid_to_secidx[pid]
            sec_panel_height[sidx] = float(pinfo.get("height", 0.0) or 0.0)
            sec_arranged_fig_height[sidx] = 0.0

    # 初步构建 fig 列表（宽度基于 panel 宽度推得）
    sec_figs = {i: [] for i in range(len(sections))}
    for fg in figures:
        pid = fg.get("panel_id")
        if pid not in panelid_to_secidx: continue
        sidx = panelid_to_secidx[pid]
        pinfo = panels_by_id.get(pid, {})
        p_w = float(pinfo.get("width", 1.0) or 1.0)
        f_w = float(fg.get("width", 0.0) or 0.0)
        frac = 0.0 if p_w <= 0 else (f_w / p_w) * 0.95
        width_frac = max(FIG_MIN_FRAC, min(FIG_MAX_FRAC, (frac if frac > 0 else 0.6) * FIG_ENLARGE_FACTOR))
        fpath = fg.get("figure_path", "")
        cap_raw = cap_full.get(fpath) or cap_base.get(os.path.basename(fpath)) or ""
        cap = clean_caption_prefix(cap_raw)  # <-- 这里清洗
        sec_figs[sidx].append({
            "src": fpath, "caption": cap,
            "width_frac": width_frac,
            "order_y": float(fg.get("y", 0.0) or 0.0),
            "arranged_height": float(fg.get("height", 0.0) or 0.0)
        })
        # 统计安排高度
        sec_arranged_fig_height[sidx] = sec_arranged_fig_height.get(sidx, 0.0) + float(fg.get("height", 0.0) or 0.0)

    for i in list(sec_figs.keys()):
        sec_figs[i].sort(key=lambda x: x["order_y"])

    # —— 核心：按 panel 预算收缩图像 —— #
    for sidx, figs in sec_figs.items():
        if not figs: continue
        panel_h = sec_panel_height.get(sidx, 0.0)
        arranged_h = sec_arranged_fig_height.get(sidx, 0.0)
        # 粗略估算正文“行数”→ 行高比例
        content = sections[sidx].get("content","") or ""
        n_chars = len(content.strip().replace("\n"," "))
        n_lines = math.ceil(n_chars / max(1, TEXT_CHAR_PER_LINE))
        text_ratio = n_lines * LINE_HEIGHT_WEIGHT  # 经验换算
        # 允许图像占比随字数减少而下降（字越多，留给图的比例越小）
        ratio_limit = max(0.30, BASE_FIG_RATIO_LIMIT - min(0.25, 0.12 * (n_chars/600.0)))
        # 计算当前安排下的“图占比”
        cur_ratio = 0.0 if panel_h <= 0 else arranged_h / panel_h
        # 还要为标题/内边距留点空间
        safety = 0.08
        allowed = max(0.0, ratio_limit - text_ratio - safety)
        if cur_ratio > 0 and allowed > 0 and cur_ratio > allowed:
            # 按比例统一缩小本 section 所有图的 width_frac
            scale = allowed / cur_ratio
            for it in figs:
                it["width_frac"] = max(FIG_MIN_FRAC, min(FIG_MAX_FRAC, it["width_frac"] * scale))

    return sec_figs

def figures_to_latex(fig_list, out_tex_path: pathlib.Path, images_parent: pathlib.Path) -> str:
    chunks = []
    for it in fig_list:
        rel = copy_and_get_relpath(it["src"], out_tex_path, images_parent)
        w = it["width_frac"]; cap = escape_text(it["caption"] or "")
        chunks.append(
            "\\begin{figure}\n"
            +"\\centering\n"
            +f"\\includegraphics[width={w:.2f}\\linewidth]{{{rel}}}\n"
            # + (f"\\caption{{{cap}}}\n" if cap else "")
            +"\\end{figure}\n"
        )
    return "\n".join(chunks)


def strip_stray_t(tex: str) -> str:
    _T_BEFORE_DOLLAR_RE = re.compile(r'\\t(?=\$)')   
    if not tex:
        return tex
    return _T_BEFORE_DOLLAR_RE.sub('', tex)

# ===================== 主流程 =====================
def build():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {}) or {}
    sections_all = data.get("sections", []) or []
    sections = [s for s in sections_all if norm_title(s.get("title","")) != norm_title("Poster Title & Author")]

    panels_by_id, figures, cap_full, cap_base = load_arrangement_and_captions()
    print(f"✅ Loaded arrangement and captions.")
    sample_paths = [pathlib.Path(f.get("figure_path","")) for f in figures if f.get("figure_path")]
    images_parent = resolve_images_parent_dir(sample_paths)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # 头部
    t, a, inst, wrapped_title = build_header_from_meta(meta)
    new_tex = template
    new_tex = replace_command_balanced(new_tex, "title", t)
    new_tex = replace_command_balanced(new_tex, "author", a)
    new_tex = replace_command_balanced(new_tex, "institute", inst)

    # 放大 scale + 动态标题字号 + 右上角 logo
    new_tex = bump_beamerposter_scale(new_tex, BEAMER_SCALE_TARGET)
    dyn_title_size = choose_title_size_cmd(wrapped_title)   # <-- 多行则调小
    new_tex = inject_font_tweaks(new_tex, dyn_title_size)
    new_tex = inject_right_logo(new_tex)

    # blocks（带“按预算缩放”的图 + 清洗后的 caption）
    secidx_to_figs = build_figures_for_sections(sections, panels_by_id, figures, cap_full, cap_base)
    blocks = []
    for i, sec in enumerate(sections):
        figs_tex = figures_to_latex(secidx_to_figs.get(i, []), OUTPUT_PATH, images_parent) if secidx_to_figs.get(i) else ""
        blocks.append(make_block(sec.get("title",""), sec.get("content",""), figs_tex))

    # 三列连续均匀切分
    new_tex = rebuild_first_columns_region_to_three(new_tex, blocks)
    # --- 后处理：清理多余转义 ---
    cleaned_tex = new_tex
    cleaned_tex = cleaned_tex.replace(r"\{", "{")
    cleaned_tex = cleaned_tex.replace(r"\}", "}")
    # 注意：要先处理上面的大括号再处理反斜杠，否则会提前破坏结构
    cleaned_tex = cleaned_tex.replace(r"\\\\", r"\\")  # 避免双转义干扰
    cleaned_tex = cleaned_tex.replace(r"\\", "\\")      # 最终将 \\ → \
    cleaned_tex = cleaned_tex.replace(r"\t\t", "\\t")
    cleaned_tex = strip_stray_t(cleaned_tex)

    OUTPUT_PATH.write_text(cleaned_tex, encoding="utf-8")
    print(f"✅ Wrote: {OUTPUT_PATH.relative_to(ROOT_DIR)}")
    print(f"📁 Figures copied to: {OUTPUT_DIR / 'figures'}")
    print(f"🔠 Title size chosen: {dyn_title_size}")

if __name__ == "__main__":
    build()
