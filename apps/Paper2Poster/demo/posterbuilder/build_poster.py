# build_poster.py  /  convert.py
# -*- coding: utf-8 -*-
import json, re, pathlib, shutil, os

# ===================== 自动定位项目根 =====================
IMAGES_DIR_NAME = "<gpt-5_gpt-5>_images_and_tables"  # 蓝色文件夹名

def find_project_root(start: pathlib.Path) -> pathlib.Path:
    cur = start.resolve()
    for p in [cur] + list(cur.parents):
        if (p / "Paper2Poster").exists() or (p / "Paper2Video").exists():
            return p
        if (p / IMAGES_DIR_NAME).exists():
            return p
        if (p / "test" / "cambridge_template.tex").exists():
            return p
    return cur

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR   = find_project_root(SCRIPT_DIR)
TEST_DIR   = ROOT_DIR / "test"

# ===================== 路径（全部相对 ROOT_DIR） =====================
JSON_PATH        = TEST_DIR / "poster_content.json"
TEMPLATE_PATH    = TEST_DIR / "cambridge_template.tex"
ARRANGEMENT_PATH = TEST_DIR / "arrangement.json"
CAPTION_PATH     = TEST_DIR / "figure_caption.json"

OUTPUT_DIR       = TEST_DIR / "latex_proj"
OUTPUT_PATH      = OUTPUT_DIR / "poster_output_fix.tex"  # tex 与 figures 都在 OUTPUT_DIR

# 图片父目录（优先 Paper2Poster/，找不到再退回 ROOT_DIR/）
IMAGES_PARENTS   = [ROOT_DIR / "Paper2Poster", ROOT_DIR]

# ============ 放大参数（可以按需微调） ============
BEAMER_SCALE_TARGET   = 1.1      # 模板 \usepackage{beamerposter}[... scale=...] 的新值
TITLE_SIZE_CMD        = r"\Huge"  # 标题字号
AUTHOR_SIZE_CMD       = r"\Large"
INSTITUTE_SIZE_CMD    = r"\large"
BLOCK_TITLE_SIZE_CMD  = r"\Large"
BLOCK_BODY_SIZE_CMD   = r"\large"
CAPTION_SIZE_CMD      = r"\small"

FIG_ENLARGE_FACTOR    = 1.1      # 图片放大系数（在不超过 0.92\linewidth 的前提下）
FIG_MIN_FRAC          = 0.60      # 最小宽度占比
FIG_MAX_FRAC          = 0.92      # 最大宽度占比

RIGHT_LOGO_FILENAME   = "logo.png"  # 位于 latex_proj/ 下
RIGHT_LOGO_HEIGHT_CM  = 6.0         # 右上角 logo 高度（cm）
RIGHT_LOGO_INNERSEP_CM= 2.0         # 右上角内边距（cm）
RIGHT_LOGO_XSHIFT_CM  = -2.0        # 右上角水平偏移（cm）
RIGHT_LOGO_YSHIFT_CM  = 0.0         # 右上角垂直偏移（cm）

# ===================== 基础工具 =====================
def escape_text(s: str) -> str:
    if not s: return ""
    rep = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
           "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    for k, v in rep.items(): s = s.replace(k, v)
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
    if not content: return ""
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    if lines and all(ln.startswith(("-", "•")) for ln in lines):
        items = [escape_text(ln.lstrip("-• ").strip()) for ln in lines]
        return "\n".join(["\\begin{itemize}"] + [f"\\item {it}" for it in items] + ["\\end{itemize}"])
    return escape_text(" ".join(lines))

def make_block(title: str, content: str, figures_tex: str = "") -> str:
    body = format_content_to_latex(content or "")
    if figures_tex: body = (body + "\n\n" if body else "") + figures_tex
    return f"\\begin{{block}}{{{escape_text(title or '')}}}\n{body}\n\\end{{block}}\n"

def build_header_from_meta(meta: dict):
    raw_title = meta.get('poster_title','') or ''
    wrapped_title = soft_wrap_title_for_logo(raw_title)
    t = f"\\title{{{escape_text(wrapped_title)}}}"
    a = f"\\author{{{escape_text(meta.get('authors',''))}}}"
    inst = f"\\institute[shortinst]{{{escape_text(meta.get('affiliations',''))}}}"
    return t, a, inst

# ===================== LaTeX 环境/模板增强 =====================
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

def inject_font_tweaks(tex: str) -> str:
    """在 \begin{document} 前注入字号设置"""
    tweaks = (
        "\n% --- injected font tweaks ---\n"
        f"\\setbeamerfont{{title}}{{size={TITLE_SIZE_CMD}}}\n"
        f"\\setbeamerfont{{author}}{{size={AUTHOR_SIZE_CMD}}}\n"
        f"\\setbeamerfont{{institute}}{{size={INSTITUTE_SIZE_CMD}}}\n"
        f"\\setbeamerfont{{block title}}{{size={BLOCK_TITLE_SIZE_CMD}}}\n"
        f"\\setbeamerfont{{block body}}{{size={BLOCK_BODY_SIZE_CMD}}}\n"
        f"\\setbeamerfont{{caption}}{{size={CAPTION_SIZE_CMD}}}\n"
        "\\setlength{\\abovecaptionskip}{8pt}\n"
        "\\setlength{\\belowcaptionskip}{8pt}\n"
    )
    pos_doc = tex.find(r"\begin{document}")
    return tex[:pos_doc] + tweaks + tex[pos_doc:] if pos_doc != -1 else tex + tweaks

def inject_right_logo(tex: str) -> str:
    """
    在现有 \addtobeamertemplate{headline} 的 tikzpicture 内追加右上角 logo；
    若已存在（检测 'logo.png'）则不重复；若找不到该块则新增一个。
    """
    if "logo.png" in tex:
        return tex  # 已经加过

    # 尝试在已有 headline 的 tikzpicture 里插入
    pos_head = tex.find(r"\addtobeamertemplate{headline}")
    node = (
        f"\n      \\node[anchor=north east, inner sep={RIGHT_LOGO_INNERSEP_CM}cm]"
        f" at ([xshift={RIGHT_LOGO_XSHIFT_CM}cm,yshift={RIGHT_LOGO_YSHIFT_CM}cm]current page.north east)\n"
        f"      {{\\includegraphics[height={RIGHT_LOGO_HEIGHT_CM}cm]{{{RIGHT_LOGO_FILENAME}}}}};\n"
    )
    if pos_head != -1:
        # 找 tikzpicture 环境范围
        begin_tikz = tex.find(r"\begin{tikzpicture}", pos_head)
        if begin_tikz != -1:
            b, e = find_env_bounds(tex, "tikzpicture", begin_tikz)
            if b is not None:
                region = tex[b:e]
                pos_end = region.rfind(r"\end{tikzpicture}")
                if pos_end != -1:
                    insert_at = b + pos_end
                    return tex[:insert_at] + node + tex[insert_at:]

    # fallback：追加一个新的 headline（不影响原有）
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

# ===================== 图片布置（相对 PaperShow/） =====================
def load_arrangement_and_captions():
    arr = json.loads(ARRANGEMENT_PATH.read_text(encoding="utf-8"))
    panels = arr.get("panel_arrangement", [])
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
    # 优先 Paper2Poster/
    for parent in IMAGES_PARENTS:
        for sp in sample_fig_paths[:10]:
            if sp:
                p = parent / sp
                if p.exists():
                    return parent
    return IMAGES_PARENTS[0]

def copy_and_get_relpath(figure_path: str, out_tex_path: pathlib.Path, images_parent: pathlib.Path) -> str:
    """
    规则：
      - 绝对路径：直接用；
      - 相对路径：
         * 若以 IMAGES_DIR_NAME 开头：src = images_parent / figure_path
         * 否则：src = images_parent / IMAGES_DIR_NAME / figure_path
    复制到 test/latex_proj/figures/<basename>；TeX 用 'figures/<basename>'
    """
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

def build_figures_for_sections(sections, panels_by_id, figures, cap_full, cap_base):
    sec_name_to_idx = {norm_title(sec.get("title","")): i
                       for i, sec in enumerate(sections)
                       if norm_title(sec.get("title","")) != norm_title("Poster Title & Author")}
    panelid_to_secidx = {}
    for p in panels_by_id.values():
        pname = norm_title(p.get("panel_name",""))
        if pname in sec_name_to_idx:
            panelid_to_secidx[p["panel_id"]] = sec_name_to_idx[pname]

    sec_figs = {i: [] for i in range(len(sections))}
    for fg in figures:
        pid = fg.get("panel_id")
        if pid not in panelid_to_secidx: continue
        secidx = panelid_to_secidx[pid]
        pinfo = panels_by_id.get(pid, {})
        p_w = float(pinfo.get("width", 1.0) or 1.0)
        f_w = float(fg.get("width", 0.0) or 0.0)
        # 原始比例（基于 panel 宽度），再整体放大 FIG_ENLARGE_FACTOR
        frac = 0.0 if p_w <= 0 else (f_w / p_w) * 0.95
        width_frac = max(FIG_MIN_FRAC, min(FIG_MAX_FRAC, (frac if frac > 0 else 0.6) * FIG_ENLARGE_FACTOR))
        fpath = fg.get("figure_path", "")
        cap = cap_full.get(fpath) or cap_base.get(os.path.basename(fpath)) or ""
        sec_figs[secidx].append({
            "src": fpath, "caption": cap,
            "width_frac": width_frac, "order_y": float(fg.get("y", 0.0) or 0.0)
        })
    for i in list(sec_figs.keys()):
        sec_figs[i].sort(key=lambda x: x["order_y"])
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
            + (f"\\caption{{{cap}}}\n" if cap else "")
            +"\\end{figure}\n"
        )
    return "\n".join(chunks)

# ===================== 主流程 =====================
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {}) or {}
    sections_all = data.get("sections", []) or []
    # 跳过 “Poster Title & Author”
    sections = [s for s in sections_all if norm_title(s.get("title","")) != norm_title("Poster Title & Author")]

    panels_by_id, figures, cap_full, cap_base = load_arrangement_and_captions()
    sample_paths = [pathlib.Path(f.get("figure_path","")) for f in figures if f.get("figure_path")]
    images_parent = resolve_images_parent_dir(sample_paths)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # 1) 头部
    t, a, inst = build_header_from_meta(meta)
    new_tex = template
    new_tex = replace_command_balanced(new_tex, "title", t)
    new_tex = replace_command_balanced(new_tex, "author", a)
    new_tex = replace_command_balanced(new_tex, "institute", inst)

    # 1.1) 放大 beamerposter 的 scale，并注入字号增强
    new_tex = bump_beamerposter_scale(new_tex, BEAMER_SCALE_TARGET)
    new_tex = inject_font_tweaks(new_tex)

    # 1.2) 右上角追加 logo（latex_proj/logo.png）
    # 注意：TeX 文件与 logo.png 同目录，includegraphics 直接用文件名
    new_tex = inject_right_logo(new_tex)

    # 2) blocks（带图）
    secidx_to_figs = build_figures_for_sections(sections, panels_by_id, figures, cap_full, cap_base)
    blocks = []
    for i, sec in enumerate(sections):
        figs_tex = figures_to_latex(secidx_to_figs.get(i, []), OUTPUT_PATH, images_parent) if secidx_to_figs.get(i) else ""
        blocks.append(make_block(sec.get("title",""), sec.get("content",""), figs_tex))

    # 3) 三列连续均匀切分
    new_tex = rebuild_first_columns_region_to_three(new_tex, blocks)

    OUTPUT_PATH.write_text(new_tex, encoding="utf-8")
    print(f"✅ Wrote: {OUTPUT_PATH.relative_to(ROOT_DIR)}")
    print(f"📁 Figures copied to: {OUTPUT_DIR / 'figures'}")
    print(f"🖼  Right-top logo path (relative): {RIGHT_LOGO_FILENAME}")
    print(f"🔠 Font scale: beamerposter scale={BEAMER_SCALE_TARGET}, title={TITLE_SIZE_CMD}, block body={BLOCK_BODY_SIZE_CMD}")
    print(f"🖼  Figure enlarge: factor={FIG_ENLARGE_FACTOR}, min={FIG_MIN_FRAC}, max={FIG_MAX_FRAC}")

# if __name__ == "__main__":
#     main()
