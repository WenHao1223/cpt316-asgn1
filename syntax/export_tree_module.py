# syntax_tree_export_module.py
from PIL import Image, ImageDraw, ImageFont

HSPACE = 24   # horizontal gap between siblings
VSPACE = 48   # vertical gap between levels
PADDING = 24  # image padding
TXTPAD = 10   # padding inside a node box
FONTSIZE = 16

def _text_size(text, font):
    # width, height via bbox
    l, t, r, b = font.getbbox(text)
    return (r - l), (b - t)

def _node_label(node):
    return f"{node.node_type}: {node.value}" if node.value is not None else node.node_type

def _node_box_size(node, font):
    tw, th = _text_size(_node_label(node), font)
    return tw + 2 * TXTPAD, th + 2 * TXTPAD

def _subtree_size(node, font):
    """Returns (width, height) needed for the whole subtree rooted at node."""
    nw, nh = _node_box_size(node, font)
    if not node.children:
        return nw, nh  # leaf
    child_sizes = [_subtree_size(c, font) for c in node.children]
    total_children_w = sum(w for w, _ in child_sizes) + HSPACE * (len(child_sizes) - 1)
    total_w = max(nw, total_children_w)
    total_h = nh + VSPACE + max(h for _, h in child_sizes)
    return total_w, total_h

def _draw_subtree(draw, node, x_center, y_top, font):
    """Draw node centered at x_center, top at y_top; return center x of this node."""
    label = _node_label(node)
    nw, nh = _node_box_size(node, font)
    left = x_center - nw / 2
    right = x_center + nw / 2
    bottom = y_top + nh

    # node box + text
    draw.rectangle([left, y_top, right, bottom], outline="black", width=2)
    draw.text((left + TXTPAD, y_top + TXTPAD), label, font=font, fill="black")

    if not node.children:
        return x_center  # leaf

    # Layout children block centered under parent
    child_sizes = [_subtree_size(c, font) for c in node.children]
    total_children_w = sum(w for w, _ in child_sizes) + HSPACE * (len(child_sizes) - 1)
    start_x = x_center - total_children_w / 2

    # draw each child
    child_centers = []
    cx = start_x
    y_child = bottom + VSPACE
    for c, (cw, ch) in zip(node.children, child_sizes):
        child_center = cx + cw / 2
        # edge: parent bottom center -> child top center
        child_nw, child_nh = _node_box_size(c, font)
        child_top = y_child
        child_top_center = (child_center, child_top)
        parent_bottom_center = (x_center, bottom)
        draw.line([parent_bottom_center, child_top_center], fill="black", width=2)
        # draw child subtree
        _draw_subtree(draw, c, child_center, child_top, font)
        child_centers.append(child_center)
        cx += cw + HSPACE

    return x_center

def export_tree_png(tree, filename):
    # font
    try:
        font = ImageFont.truetype("consola.ttf", FONTSIZE)  # Consolas if available
    except:
        font = ImageFont.load_default()

    # compute whole image size
    tw, th = _subtree_size(tree, font)
    img_w = int(tw + 2 * PADDING)
    img_h = int(th + 2 * PADDING)

    img = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(img)

    # center root horizontally
    root_center_x = img_w / 2
    root_top_y = PADDING
    _draw_subtree(draw, tree, root_center_x, root_top_y, font)

    img.save(filename)
    print(f"Saved PNG: {filename}")
