"""Build an SVG symbol sprite from icon bounding boxes in an SVG layer."""

import argparse
import copy
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET


SVG_NAMESPACE = "http://www.w3.org/2000/svg"
SVG = f"{{{SVG_NAMESPACE}}}"
EDITOR_NAMESPACES = (
    "http://www.inkscape.org/namespaces/inkscape",
    "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
)

ET.register_namespace("", SVG_NAMESPACE)


def _local_name(tag):
    return tag.rsplit("}", 1)[-1]


def _simplify_presentation(element):
    style_fill = None
    style_opacity = {}
    style = element.attrib.pop("style", "")
    for declaration in style.split(";"):
        property_name, separator, value = declaration.partition(":")
        if not separator:
            continue
        property_name = property_name.strip()
        value = value.strip()
        if property_name == "fill":
            style_fill = value
        elif property_name in {"fill-opacity", "opacity"}:
            style_opacity[property_name] = value

    if style_fill is not None:
        element.set("fill", "none" if style_fill == "none" else "currentColor")
    elif element.get("fill") not in {None, "none"}:
        element.set("fill", "currentColor")

    for property_name, value in style_opacity.items():
        element.set(property_name, value)

    for attribute in list(element.attrib):
        local_name = _local_name(attribute)
        if (
            attribute.startswith(tuple(f"{{{namespace}}}" for namespace in EDITOR_NAMESPACES))
            or local_name == "stroke"
            or local_name.startswith("stroke-")
        ):
            del element.attrib[attribute]

    for child in element:
        _simplify_presentation(child)


def _remove_ids(element):
    element.attrib.pop("id", None)
    for child in element:
        _remove_ids(child)


def _number(value, attribute, rect_id):
    if value is None:
        raise ValueError(f"Rectangle '{rect_id}' has no {attribute!r} attribute.")
    return float(value)


def _guide_rectangles(root, layer_id):
    layer = root.find(f".//{SVG}g[@id='{layer_id}']")
    if layer is None:
        raise ValueError(f"Could not find guide layer '{layer_id}'.")

    rectangles = []
    for rect in layer.findall(f".//{SVG}rect"):
        rect_id = rect.get("id")
        if not rect_id:
            raise ValueError("Every guide rectangle must have an id.")
        if re.fullmatch(r"rect\d+", rect_id):
            continue

        x = _number(rect.get("x", "0"), "x", rect_id)
        y = _number(rect.get("y", "0"), "y", rect_id)
        width = _number(rect.get("width"), "width", rect_id)
        height = _number(rect.get("height"), "height", rect_id)
        if width <= 0 or height <= 0:
            raise ValueError(f"Rectangle '{rect_id}' must have positive dimensions.")

        rectangles.append((rect_id, x, y, width, height))

    if not rectangles:
        raise ValueError(f"Guide layer '{layer_id}' has no rectangles.")

    return layer, rectangles


def _flatten_svg(input_svg, output_svg):
    _run_inkscape(
        input_svg,
        output_svg,
        "select-all;object-to-path;object-stroke-to-path",
    )


def _run_inkscape(input_svg, output_svg, actions):
    try:
        subprocess.run(
            [
                "inkscape",
                input_svg,
                f"--actions={actions}",
                "--export-plain-svg",
                f"--export-filename={output_svg}",
            ],
            check=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError("Inkscape must be installed and available on PATH.") from error
    except subprocess.CalledProcessError as error:
        raise RuntimeError("Inkscape could not flatten the source SVG.") from error


def _combine_symbol_paths(artwork, rect_id, x, y, width, height, temp_dir):
    source_path = temp_dir / f"{rect_id}.svg"
    flattened_path = temp_dir / f"{rect_id}-flattened.svg"
    intersection_path = temp_dir / f"{rect_id}-intersection.svg"
    clipped_path = temp_dir / f"{rect_id}-clipped.svg"
    source = ET.Element(
        f"{SVG}svg",
        {
            "width": f"{width:g}",
            "height": f"{height:g}",
            "viewBox": f"0 0 {width:g} {height:g}",
        },
    )
    translated_artwork = ET.SubElement(
        source,
        f"{SVG}g",
        {"transform": f"translate({-x:g} {-y:g})"},
    )
    for element in artwork:
        clone = copy.deepcopy(element)
        _remove_ids(clone)
        _simplify_presentation(clone)
        translated_artwork.append(clone)

    ET.ElementTree(source).write(source_path, encoding="utf-8", xml_declaration=True)
    _run_inkscape(
        str(source_path),
        str(flattened_path),
        ";".join(
            [
                "select-all:all",
                "selection-ungroup",
            ]
            * 8
            + [
                "select-all",
                "path-combine",
            ]
        ),
    )

    paths = ET.parse(flattened_path).getroot().findall(f".//{SVG}path")
    path_data = " ".join(path.get("d", "") for path in paths).strip()
    if not path_data:
        raise ValueError(f"Icon '{rect_id}' has no path data after flattening.")

    intersection = ET.Element(
        f"{SVG}svg",
        {
            "width": f"{width:g}",
            "height": f"{height:g}",
            "viewBox": f"0 0 {width:g} {height:g}",
        },
    )
    ET.SubElement(intersection, f"{SVG}path", {"id": "art", "d": path_data})
    ET.SubElement(
        intersection,
        f"{SVG}path",
        {
            "id": "crop",
            "d": f"M 0 0 H {width:g} V {height:g} H 0 Z",
        },
    )
    ET.ElementTree(intersection).write(intersection_path, encoding="utf-8", xml_declaration=True)
    _run_inkscape(
        str(intersection_path),
        str(clipped_path),
        "select-by-id:art;select-by-id:crop;path-intersection",
    )

    clipped_paths = ET.parse(clipped_path).getroot().findall(f".//{SVG}path")
    clipped_data = " ".join(path.get("d", "") for path in clipped_paths).strip()
    if not clipped_data:
        raise ValueError(f"Icon '{rect_id}' has no path data after clipping.")
    return clipped_data


def compile_precise_spritesheet_by_layer_input(input_svg, output_spritesheet, squares_layer_id):
    """Create one plain-SVG, clipped, current-color symbol for each guide rectangle."""
    source_path = Path(input_svg)
    output_path = Path(output_spritesheet)
    tree = ET.parse(source_path)
    _, rectangles = _guide_rectangles(tree.getroot(), squares_layer_id)

    with tempfile.TemporaryDirectory(prefix="prosango-icon-sprite-") as temp_dir:
        flattened_path = Path(temp_dir) / "flattened.svg"
        _flatten_svg(str(source_path), str(flattened_path))

        flattened_root = ET.parse(flattened_path).getroot()
        flattened_guide_layer = flattened_root.find(f".//{SVG}g[@id='{squares_layer_id}']")
        if flattened_guide_layer is None:
            raise ValueError(f"Flattened SVG has no guide layer '{squares_layer_id}'.")

        artwork = [
            child
            for child in flattened_root
            if child is not flattened_guide_layer
            and _local_name(child.tag) not in {"defs", "metadata", "namedview"}
        ]

        sprite_sheet = ET.Element(f"{SVG}svg", {"style": "display: none"})
        defs = ET.SubElement(sprite_sheet, f"{SVG}defs")

        for rect_id, x, y, width, height in rectangles:
            symbol = ET.SubElement(
                defs,
                f"{SVG}symbol",
                {
                    "id": rect_id,
                    "viewBox": f"0 0 {width:g} {height:g}",
                    "overflow": "hidden",
                },
            )
            path_data = _combine_symbol_paths(
                artwork,
                rect_id,
                x,
                y,
                width,
                height,
                Path(temp_dir),
            )
            ET.SubElement(
                symbol,
                f"{SVG}path",
                {"d": path_data, "fill": "currentColor"},
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_tree = ET.ElementTree(sprite_sheet)
    ET.indent(output_tree, space="  ")
    output_tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Created {output_path} with {len(rectangles)} symbols.")


def main():
    assets_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=assets_dir / "master_icons.svg")
    parser.add_argument("--output", type=Path, default=assets_dir / "production_icons.svg")
    parser.add_argument("--layer", default="layer2", help="ID of the guide rectangle layer")
    args = parser.parse_args()

    compile_precise_spritesheet_by_layer_input(args.input, args.output, args.layer)


if __name__ == "__main__":
    main()
