import math
from django.conf import settings

from evennia.utils.evtable import EvTable
from evennia.utils.ansi import ANSIString


def styled_table(viewer, *args, **kwargs):
    """
    Create an EvTable styled by on user preferences.

    Args:
        *args (str): Column headers. If not colored explicitly, these will get colors
            from user options.
    Kwargs:
        any (str, int or dict): EvTable options, including, optionally a `table` dict
            detailing the contents of the table.
    Returns:
        table (EvTable): An initialized evtable entity, either complete (if using `table` kwarg)
            or incomplete and ready for use with `.add_row` or `.add_collumn`.

    """
    viewer = viewer.get_account() if viewer else None
    default_style = settings.OPTIONS_ACCOUNT_DEFAULT
    border_color = viewer.options.get("border_color") if viewer else default_style['border_color'][2]
    column_color = viewer.options.get("column_names_color") if viewer else default_style['column_names_color'][2]

    colornames = ["|%s%s|n" % (column_color, col) for col in args]

    h_line_char = kwargs.pop("header_line_char", "~")
    header_line_char = ANSIString(f"|{border_color}{h_line_char}|n")
    c_char = kwargs.pop("corner_char", "+")
    corner_char = ANSIString(f"|{border_color}{c_char}|n")

    b_left_char = kwargs.pop("border_left_char", "||")
    border_left_char = ANSIString(f"|{border_color}{b_left_char}|n")

    b_right_char = kwargs.pop("border_right_char", "||")
    border_right_char = ANSIString(f"|{border_color}{b_right_char}|n")

    b_bottom_char = kwargs.pop("border_bottom_char", "-")
    border_bottom_char = ANSIString(f"|{border_color}{b_bottom_char}|n")

    b_top_char = kwargs.pop("border_top_char", "-")
    border_top_char = ANSIString(f"|{border_color}{b_top_char}|n")

    table = EvTable(
        *colornames,
        header_line_char=header_line_char,
        corner_char=corner_char,
        border_left_char=border_left_char,
        border_right_char=border_right_char,
        border_top_char=border_top_char,
        **kwargs,
    )
    return table


def _render_decoration(
        viewer,
        header_text=None,
        fill_character=None,
        edge_character=None,
        mode="header",
        color_header=True,
        width=None,
):
    """
    Helper for formatting a string into a pretty display, for a header, separator or footer.

    Kwargs:
        header_text (str): Text to include in header.
        fill_character (str): This single character will be used to fill the width of the
            display.
        edge_character (str): This character caps the edges of the display.
        mode(str): One of 'header', 'separator' or 'footer'.
        color_header (bool): If the header should be colorized based on user options.
        width (int): If not given, the client's width will be used if available.

    Returns:
        string (str): The decorated and formatted text.

    """
    viewer = viewer.get_account() if viewer else None
    colors = dict()
    default_style = settings.OPTIONS_ACCOUNT_DEFAULT
    colors["border"] = viewer.options.get("border_color") if viewer else default_style['border_color'][2]
    colors["headertext"] = viewer.options.get(f"{mode}_text_color") if viewer else default_style[f"{mode}_text_color"][2]
    colors["headerstar"] = viewer.options.get(f"{mode}_star_color") if viewer else default_style[f"{mode}_star_color"][2]

    width = width if width else settings.CLIENT_DEFAULT_WIDTH
    if edge_character:
        width -= 2

    if header_text:
        if color_header:
            header_text = ANSIString(header_text).clean()
            header_text = ANSIString("|n|%s%s|n" % (colors["headertext"], header_text))
        if mode == "header":
            begin_center = ANSIString(
                "|n|%s<|%s* |n" % (colors["border"], colors["headerstar"])
            )
            end_center = ANSIString("|n |%s*|%s>|n" % (colors["headerstar"], colors["border"]))
            center_string = ANSIString(begin_center + header_text + end_center)
        else:
            center_string = ANSIString("|n |%s%s |n" % (colors["headertext"], header_text))
    else:
        center_string = ""

    fill_character = viewer.options.get("%s_fill" % mode) if viewer else default_style[f"{mode}_fill"][2]

    remain_fill = width - len(center_string)
    if remain_fill % 2 == 0:
        right_width = remain_fill / 2
        left_width = remain_fill / 2
    else:
        right_width = math.floor(remain_fill / 2)
        left_width = math.ceil(remain_fill / 2)

    right_fill = ANSIString("|n|%s%s|n" % (colors["border"], fill_character * int(right_width)))
    left_fill = ANSIString("|n|%s%s|n" % (colors["border"], fill_character * int(left_width)))

    if edge_character:
        edge_fill = ANSIString("|n|%s%s|n" % (colors["border"], edge_character))
        main_string = ANSIString(center_string)
        final_send = (
                ANSIString(edge_fill) + left_fill + main_string + right_fill + ANSIString(edge_fill)
        )
    else:
        final_send = left_fill + ANSIString(center_string) + right_fill
    return final_send


def styled_header(viewer, *args, **kwargs):
    """
    Create a pretty header.
    """

    if "mode" not in kwargs:
        kwargs["mode"] = "header"
    return _render_decoration(viewer, *args, **kwargs)


def styled_separator(viewer, *args, **kwargs):
    """
    Create a separator.

    """
    if "mode" not in kwargs:
        kwargs["mode"] = "separator"
    return _render_decoration(viewer, *args, **kwargs)


def styled_footer(viewer, *args, **kwargs):
    """
    Create a pretty footer.

    """
    if "mode" not in kwargs:
        kwargs["mode"] = "footer"
    return _render_decoration(viewer, *args, **kwargs)


__all__ = ['styled_table', 'styled_header', 'styled_separator', 'styled_footer']
