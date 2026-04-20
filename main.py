import nltk
import string
import tkinter as tk
from tkinter import scrolledtext
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import threading

# Download required data (run once)
nltk.download('punkt',      quiet=True)
nltk.download('punkt_tab',  quiet=True)
nltk.download('stopwords',  quiet=True)


# ══════════════════════════════════════════════════════
#  COLOUR PALETTE  —  soft professional light theme
# ══════════════════════════════════════════════════════
BG_ROOT      = "#F0F2F7"
BG_WHITE     = "#FFFFFF"
BG_FIELD     = "#F7F8FC"

AC_BLUE      = "#3B82F6"
AC_BLUE_LT   = "#EFF6FF"
AC_GREEN     = "#16A34A"
AC_GREEN_LT  = "#F0FDF4"
AC_ORANGE    = "#EA580C"
AC_ORANGE_LT = "#FFF7ED"
AC_RED       = "#DC2626"
AC_RED_LT    = "#FEF2F2"
AC_PURPLE    = "#7C3AED"
AC_AMBER     = "#D97706"

TX_HEADING   = "#111827"
TX_BODY      = "#374151"
TX_MUTED     = "#6B7280"
TX_HINT      = "#9CA3AF"
TX_WHITE     = "#FFFFFF"

BD_DEFAULT   = "#E5E7EB"

SB_POS       = "#86EFAC"
SB_NEU       = "#FDE68A"
SB_NEG       = "#FCA5A5"


# ══════════════════════════════════════════════════════
#  NLP LOGIC
# ══════════════════════════════════════════════════════
def process_text(text):
    text = text.lower()
    words = word_tokenize(text)
    words = [w for w in words if w not in string.punctuation]
    words = [w for w in words if w.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words]
    return words


def correct_text(text):
    return str(TextBlob(text).correct())


def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return ("Positive", "😊", AC_GREEN, SB_POS, polarity)
    elif polarity < -0.2:
        return ("Negative", "😡", AC_RED,   SB_NEG, polarity)
    else:
        return ("Neutral",  "😐", AC_AMBER, SB_NEU, polarity)


def save_report(original, corrected, processed, sentiment_label):
    with open("report.txt", "a", encoding="utf-8") as f:
        f.write("\n" + "─" * 60 + "\n")
        f.write(f"Original : {original}\n")
        f.write(f"Corrected: {corrected}\n")
        f.write(f"Processed: {processed}\n")
        f.write(f"Sentiment: {sentiment_label}\n")
        words = processed.split()
        f.write(f"Words    : {len(words)}  |  Unique: {len(set(words))}\n")


# ══════════════════════════════════════════════════════
#  HELPER — darken a hex colour by pct (0-1)
# ══════════════════════════════════════════════════════
def _darken(hex_color, pct=0.12):
    h = hex_color.lstrip("#")
    r = max(0, int(int(h[0:2], 16) * (1 - pct)))
    g = max(0, int(int(h[2:4], 16) * (1 - pct)))
    b = max(0, int(int(h[4:6], 16) * (1 - pct)))
    return f"#{r:02x}{g:02x}{b:02x}"


def _blend_with_white(hex_color, factor=0.15):
    """Mix hex_color into white by factor (0=white, 1=full color)."""
    h = hex_color.lstrip("#")
    r = int(int(h[0:2], 16) * factor + 255 * (1 - factor))
    g = int(int(h[2:4], 16) * factor + 255 * (1 - factor))
    b = int(int(h[4:6], 16) * factor + 255 * (1 - factor))
    return f"#{min(r,255):02x}{min(g,255):02x}{min(b,255):02x}"


# ══════════════════════════════════════════════════════
#  CUSTOM WIDGETS
# ══════════════════════════════════════════════════════

class FlatButton(tk.Button):
    """Styled tk.Button — no Canvas needed, works on all Python/tkinter versions."""

    def __init__(self, parent, text, bg, fg,
                 command=None, width=None, height=36,
                 parent_bg=BG_ROOT, **kw):
        # Convert pixel width to approx char width (tkinter Button uses char units)
        char_w = max(8, (width or 120) // 8)
        super().__init__(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            activebackground=_darken(bg, 0.12),
            activeforeground=fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            width=char_w,
            font=("Segoe UI", 10, "bold"),
            command=command,
            **kw
        )
        self._bg = bg
        self.bind("<Enter>", lambda _e: self.config(bg=_darken(self._bg, 0.12)))
        self.bind("<Leave>", lambda _e: self.config(bg=self._bg))

    def pack(self, **kw):
        super().pack(ipady=6, **kw)
        return self


class SectionLabel(tk.Frame):
    """Small coloured-bar section heading."""

    def __init__(self, parent, title, accent=AC_BLUE, bg=BG_WHITE, **kw):
        super().__init__(parent, bg=bg, **kw)
        tk.Frame(self, width=3, bg=accent).pack(side="left", fill="y")
        tk.Label(self, text=f"  {title}", fg=accent, bg=bg,
                 font=("Segoe UI", 9, "bold")).pack(side="left")


class StatCard(tk.Frame):
    """Metric card with tinted icon circle, big number, label."""

    def __init__(self, parent, label, icon, accent, **kw):
        super().__init__(parent, bg=BG_WHITE,
                         highlightbackground=BD_DEFAULT,
                         highlightthickness=1, **kw)
        row = tk.Frame(self, bg=BG_WHITE)
        row.pack(fill="x", padx=10, pady=8)

        tint = _blend_with_white(accent, factor=0.18)
        circ = tk.Canvas(row, width=36, height=36, bg=BG_WHITE,
                         highlightthickness=0)
        circ.pack(side="left")
        circ.create_oval(2, 2, 34, 34, fill=tint, outline=accent, width=1)
        circ.create_text(18, 18, text=icon,
                         font=("Segoe UI Emoji", 15))

        meta = tk.Frame(row, bg=BG_WHITE)
        meta.pack(side="left", padx=(12, 0))
        tk.Label(meta, text=label, fg=TX_MUTED, bg=BG_WHITE,
                 font=("Segoe UI", 8), wraplength=130).pack(anchor="w")
        self._val = tk.Label(meta, text="—", fg=TX_HEADING, bg=BG_WHITE,
                             font=("Segoe UI", 18, "bold"))
        self._val.pack(anchor="w")

    def update(self, value, color=TX_HEADING):
        self._val.config(text=str(value), fg=color)


class SentimentPanel(tk.Frame):
    """Emoji + label + polarity score + animated fill bar."""

    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG_WHITE,
                         highlightbackground=BD_DEFAULT,
                         highlightthickness=1, **kw)
        inner = tk.Frame(self, bg=BG_WHITE)
        inner.pack(fill="both", padx=10, pady=10)

        top = tk.Frame(inner, bg=BG_WHITE)
        top.pack(fill="x")

        self._emoji = tk.Label(top, text="  —", fg=TX_MUTED,
                               bg=BG_WHITE, font=("Segoe UI Emoji", 20))
        self._emoji.pack(side="left")

        meta = tk.Frame(top, bg=BG_WHITE)
        meta.pack(side="left", padx=(12, 0))

        self._label = tk.Label(meta, text="Awaiting analysis",
                               fg=TX_MUTED, bg=BG_WHITE,
                               font=("Segoe UI", 11, "bold"), anchor="w")
        self._label.pack(anchor="w")

        self._score = tk.Label(meta, text="polarity score: —",
                               fg=TX_HINT, bg=BG_WHITE,
                               font=("Segoe UI", 8), anchor="w", wraplength=120)
        self._score.pack(anchor="w")

        tk.Frame(inner, height=8, bg=BG_WHITE).pack()

        track = tk.Frame(inner, height=10, bg=BD_DEFAULT)
        track.pack(fill="x")
        self._bar = tk.Frame(track, height=10, bg=BD_DEFAULT)
        self._bar.place(x=0, y=0, relheight=1, relwidth=0)

    def update(self, label, emoji, color, bar_color, polarity):
        self._emoji.config(text=emoji, fg=color)
        self._label.config(text=label, fg=color)
        self._score.config(text=f"polarity score: {polarity:+.3f}")
        self._bar.config(bg=bar_color)
        self._bar.place(relwidth=max(0.03, (polarity + 1) / 2))

    def reset(self):
        self._emoji.config(text="  —", fg=TX_MUTED)
        self._label.config(text="Awaiting analysis", fg=TX_MUTED)
        self._score.config(text="polarity score: —")
        self._bar.config(bg=BD_DEFAULT)
        self._bar.place(relwidth=0)


# ══════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════
def run_app():

    win = tk.Tk()
    win.title("Mini AI Text Analyzer")
    win.geometry("860x600")
    win.resizable(False, False)
    win.configure(bg=BG_ROOT)

    # ── HEADER ──────────────────────────────────────
    header = tk.Frame(win, bg=BG_WHITE, height=58)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Frame(header, width=5, bg=AC_BLUE).pack(side="left", fill="y")

    brain = tk.Canvas(header, width=34, height=34, bg=BG_WHITE,
                      highlightthickness=0)
    brain.pack(side="left", padx=12, pady=12)
    tint = _blend_with_white(AC_BLUE, 0.15)
    brain.create_oval(0, 0, 34, 34, fill=tint, outline=AC_BLUE, width=1)
    brain.create_text(17, 17, text="🧠", font=("Segoe UI Emoji", 15))

    htf = tk.Frame(header, bg=BG_WHITE)
    htf.pack(side="left", padx=4)
    tk.Label(htf, text="Mini AI Text Analyzer",
             fg=TX_HEADING, bg=BG_WHITE,
             font=("Segoe UI", 13, "bold")).pack(anchor="w")
    tk.Label(htf,
             text="NLTK  •  TextBlob  •  Sentiment  •  Spell Correction",
             fg=TX_MUTED, bg=BG_WHITE,
             font=("Segoe UI", 8)).pack(anchor="w")

    status_var = tk.StringVar(value="●  Ready")
    status_lbl = tk.Label(header, textvariable=status_var,
                          fg=AC_GREEN, bg=AC_GREEN_LT,
                          font=("Segoe UI", 9, "bold"),
                          padx=12, pady=5)
    status_lbl.pack(side="right", padx=20)

    tk.Frame(win, height=1, bg=BD_DEFAULT).pack(fill="x")

    # ── BODY ────────────────────────────────────────
    body = tk.Frame(win, bg=BG_ROOT)
    body.pack(fill="both", expand=True, padx=14, pady=10)

    left  = tk.Frame(body, bg=BG_ROOT)
    left.pack(side="left", fill="both", expand=True, padx=(0, 10))

    right = tk.Frame(body, bg=BG_ROOT, width=230)
    right.pack(side="right", fill="y")
    right.pack_propagate(False)

    # ── INPUT CARD ──────────────────────────────────
    in_card = tk.Frame(left, bg=BG_WHITE,
                       highlightbackground=BD_DEFAULT,
                       highlightthickness=1)
    in_card.pack(fill="x")

    in_hdr = tk.Frame(in_card, bg=BG_WHITE)
    in_hdr.pack(fill="x", padx=16, pady=(12, 6))
    SectionLabel(in_hdr, "INPUT TEXT", AC_BLUE).pack(side="left")

    char_var = tk.StringVar(value="0 / 1000")
    tk.Label(in_hdr, textvariable=char_var, fg=TX_HINT, bg=BG_WHITE,
             font=("Segoe UI", 8)).pack(side="right")

    PLACEHOLDER = "Paste or type your text here to begin analysis..."

    input_box = scrolledtext.ScrolledText(
        in_card, height=6, wrap="word",
        bg=BG_FIELD, fg=TX_HINT,
        insertbackground=AC_BLUE,
        selectbackground="#BFDBFE",
        selectforeground=TX_HEADING,
        relief="flat", bd=0,
        font=("Segoe UI", 10),
        padx=10, pady=8
    )
    input_box.pack(fill="x", padx=10, pady=(0, 4))
    input_box.insert("1.0", PLACEHOLDER)

    def _fin(_e):
        if input_box.get("1.0", "end-1c") == PLACEHOLDER:
            input_box.delete("1.0", "end")
            input_box.config(fg=TX_BODY)

    def _fout(_e):
        if not input_box.get("1.0", "end-1c").strip():
            input_box.insert("1.0", PLACEHOLDER)
            input_box.config(fg=TX_HINT)

    def _key(_e=None):
        t = input_box.get("1.0", "end-1c")
        if t != PLACEHOLDER:
            char_var.set(f"{len(t)} / 1000")

    input_box.bind("<FocusIn>",    _fin)
    input_box.bind("<FocusOut>",   _fout)
    input_box.bind("<KeyRelease>", _key)

    tk.Frame(in_card, height=4, bg=BG_WHITE).pack()

    # ── BUTTONS ─────────────────────────────────────
    btn_row = tk.Frame(left, bg=BG_ROOT)
    btn_row.pack(fill="x", pady=8)

    def set_status(text, fg, bg):
        status_var.set(text)
        status_lbl.config(fg=fg, bg=bg)
        win.update_idletasks()

    saved_var = tk.StringVar(value="")

    def process_input():
        raw = input_box.get("1.0", "end-1c").strip()
        if not raw or raw == PLACEHOLDER:
            output_box.config(state="normal")
            output_box.delete("1.0", "end")
            output_box.insert("end",
                "⚠  Please enter some text before analyzing.\n", "warn")
            output_box.config(state="disabled")
            return

        set_status("⟳  Processing…", AC_ORANGE, AC_ORANGE_LT)

        def _worker():
            corrected = correct_text(raw)
            words     = process_text(corrected)
            processed = " ".join(words).capitalize()
            s_label, s_emoji, s_color, s_bar, polarity = get_sentiment(raw)
            div = "─" * 56 + "\n"

            output_box.config(state="normal")
            output_box.delete("1.0", "end")
            output_box.insert("end", "  Original Text\n",   "section")
            output_box.insert("end", raw + "\n",            "body")
            output_box.insert("end", div,                   "sep")
            output_box.insert("end", "  Corrected Text\n",  "section")
            output_box.insert("end", corrected + "\n",      "green")
            output_box.insert("end", div,                   "sep")
            output_box.insert("end", "  Processed Tokens\n","section")
            output_box.insert("end", processed + "\n",      "amber")
            output_box.config(state="disabled")

            card_words.update(len(words), AC_BLUE)
            card_unique.update(len(set(words)), AC_PURPLE)
            sent_panel.update(s_label, s_emoji, s_color, s_bar, polarity)

            save_report(raw, corrected, processed, s_label)
            saved_var.set("✔  Saved to report.txt")
            set_status("✔  Done", AC_GREEN, AC_GREEN_LT)

        threading.Thread(target=_worker, daemon=True).start()

    def clear_all():
        input_box.delete("1.0", "end")
        input_box.insert("1.0", PLACEHOLDER)
        input_box.config(fg=TX_HINT)
        char_var.set("0 / 1000")
        output_box.config(state="normal")
        output_box.delete("1.0", "end")
        output_box.config(state="disabled")
        card_words.update("—", TX_HEADING)
        card_unique.update("—", TX_HEADING)
        sent_panel.reset()
        saved_var.set("")
        set_status("●  Ready", AC_GREEN, AC_GREEN_LT)

    FlatButton(btn_row, "⚡  Analyze", AC_BLUE,   TX_WHITE,
               command=process_input, width=132, height=38, ).pack(side="left", padx=(0,8))
    FlatButton(btn_row, "✕  Clear",   AC_ORANGE,  TX_WHITE,
               command=clear_all,     width=110, height=38, ).pack(side="left", padx=(0,8))
    FlatButton(btn_row, "⏻  Exit",    AC_RED,     TX_WHITE,
               command=win.destroy,   width=100, height=38, ).pack(side="left")

    tk.Label(btn_row, textvariable=saved_var, fg=AC_GREEN, bg=BG_ROOT,
             font=("Segoe UI", 9)).pack(side="right", padx=4)

    # ── OUTPUT CARD ─────────────────────────────────
    out_card = tk.Frame(left, bg=BG_WHITE,
                        highlightbackground=BD_DEFAULT,
                        highlightthickness=1)
    out_card.pack(fill="both", expand=True)

    out_hdr = tk.Frame(out_card, bg=BG_WHITE)
    out_hdr.pack(fill="x", padx=16, pady=(12, 6))
    SectionLabel(out_hdr, "ANALYSIS RESULTS", AC_PURPLE).pack(side="left")

    output_box = scrolledtext.ScrolledText(
        out_card, height=10, wrap="word",
        bg=BG_FIELD, fg=TX_BODY,
        relief="flat", bd=0,
        font=("Segoe UI", 10),
        state="disabled",
        padx=10, pady=8,
        cursor="arrow"
    )
    output_box.pack(fill="both", expand=True, padx=10, pady=(0, 8))

    output_box.tag_config("section", font=("Segoe UI", 9, "bold"),
                          foreground=AC_BLUE, spacing1=12)
    output_box.tag_config("body",    font=("Segoe UI", 11),
                          foreground=TX_BODY, spacing3=4)
    output_box.tag_config("green",   font=("Segoe UI", 11),
                          foreground=AC_GREEN, spacing3=4)
    output_box.tag_config("amber",   font=("Segoe UI", 10),
                          foreground=AC_AMBER, spacing3=4)
    output_box.tag_config("sep",     font=("Segoe UI", 7),
                          foreground=TX_HINT, spacing1=2, spacing3=2)
    output_box.tag_config("warn",    font=("Segoe UI", 10, "italic"),
                          foreground=AC_RED)

    # ── SIDEBAR ─────────────────────────────────────
    tk.Label(right, text="METRICS", fg=TX_MUTED, bg=BG_ROOT,
             font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(0, 8))

    card_words  = StatCard(right, "Word Count",   "📝", AC_BLUE)
    card_words.pack(fill="x", pady=(0, 8))

    card_unique = StatCard(right, "Unique Words", "✨", AC_PURPLE)
    card_unique.pack(fill="x", pady=(0, 10))

    tk.Frame(right, height=1, bg=BD_DEFAULT).pack(fill="x", pady=(0, 10))
    tk.Label(right, text="SENTIMENT", fg=TX_MUTED, bg=BG_ROOT,
             font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(0, 8))

    sent_panel = SentimentPanel(right)
    sent_panel.pack(fill="x")

    # ── FOOTER ──────────────────────────────────────
    tk.Frame(win, height=2, bg=AC_BLUE).pack(fill="x", side="bottom")
    foot = tk.Frame(win, bg=BG_WHITE, height=28)
    foot.pack(fill="x", side="bottom")
    foot.pack_propagate(False)
    tk.Label(foot,
             text="Mini AI Text Analyzer  •  Powered by NLTK + TextBlob",
             fg=TX_MUTED, bg=BG_WHITE,
             font=("Segoe UI", 8, "bold")).pack(side="left", padx=14, pady=6)
    tk.Label(foot, text="© 2025", fg=TX_MUTED, bg=BG_WHITE,
             font=("Segoe UI", 8, "bold")).pack(side="right", padx=14)

    win.mainloop()


if __name__ == "__main__":
    run_app()