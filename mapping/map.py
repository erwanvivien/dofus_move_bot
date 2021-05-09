import sys
import re


def get_content(filename: str) -> str:
    """
    Gets whole file content and returns it
    """

    f = open(filename, "r")
    content = f.read()
    f.close()
    return content


MAPS_NAME = ["Incarnam", "Amakna"]

res = {}


def get_line_info(line: str, map_name: str, separator: str) -> tuple:
    """
    Parses a line of format
    `x <-> y` or `x -> y`

    Returns a tuple of `(x, y, map_nampe)`
    """
    line_tuple = line.split("<->")

    left = line_tuple[0].strip()
    right = line_tuple[1].strip()
    to_map = map_name

    if " " in right:
        tmp = right.split(" ")
        right = tmp[0].strip()
        to_map = tmp[1].strip()
        if to_map not in MAPS_NAME:
            raise Exception(
                f"{to_map} is not a valid map")

    return (left, right, to_map)


# Used by function bellow
coordinates_regex = re.compile(r"(-)?[0-9]{1,2},(-)?[0-9]{1,2}")


def get_int_coo(coo: str) -> tuple:
    """
    Parses a coordinate to return a tuple `(x, y)`
    """
    if coordinates_regex.fullmatch(coo) == None:
        raise Exception(
            f"Coordinate ({coo}) does not match coordinate pattern")
    return map(int, coo.split(","))


def get_tuple_info(left: str, right: str) -> tuple:
    """
    Returns x and y (map coordinates in %)
    """
    x1, y1 = get_int_coo(left)
    x2, y2 = get_int_coo(right)

    x = "?"
    if y1 == y2:
        diff = x1 - x2
        if diff == 1:
            x = "0"
        elif diff == -1:
            x = "100"
    elif x1 == x2 and abs(y1 - y2) == 1:
        x = "50"

    y = "?"
    if x1 == x2:
        diff = y1 - y2
        if diff == 1:
            y = "0"
        elif diff == -1:
            y = "100"
    elif y1 == y2 and abs(x1 - x2) == 1:
        y = "50"

    return (x, y)


def create_to_map(coo_to: str, map_name: str,
                  coo_x: str, coo_y: str) -> dict:
    """
    Takes all the parameters and returns a JSon object
    """
    tmp = {}
    tmp["to"] = coo_to
    tmp["mapName"] = map_name
    tmp["x"] = coo_x
    tmp["y"] = coo_y

    return tmp


def get_coo_in_map(coo_list: list, coo_from: str) -> dict:
    for counter, k in enumerate(coo_list):
        for k, _ in k.items():
            if k == coo_from:
                return coo_list[counter]
    return None


def parse_line(current: dict, line: str, double=False):
    if double:
        left, right, to_map = get_line_info(line, map_name, "<->")
    else:
        left, right, to_map = get_line_info(line, map_name, "->")

    x1, y1 = get_tuple_info(left, right)
    if double:
        x2, y2 = get_tuple_info(right, left)

    left_obj = get_coo_in_map(current, left)
    if left_obj == None:
        left_obj = {left: []}
        current += [left_obj]

    if double:
        right_obj = get_coo_in_map(current, right)
        if right_obj == None:
            right_obj = {right: []}
            current += [right_obj]

    item1 = create_to_map(right, to_map, x1, y1)
    if double:
        item2 = create_to_map(left, map_name, x2, y2)

    if not item1 in left_obj[left]:
        left_obj[left] += [item1]
    if double:
        if not item2 in right_obj[right]:
            right_obj[right] += [item2]


master_line_regex = re.compile(r"^.* \*$")
for map_name in MAPS_NAME:
    res[map_name] = []
    current = res[map_name]

    content = get_content("mapping/" + map_name.lower())

    line_counter = 1
    for line in content.split("\n"):
        if not line:
            continue
        if "<->" in line:
            parse_line(current, line, True)
        elif "->" in line:
            parse_line(current, line, False)
        elif master_line_regex.fullmatch(line):  # For 4 directions one
            left = line[:-2]
            x, y = get_int_coo(left)
            for (x_, y_) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                parse_line(current, f"{x},{y}" +
                           " <-> " f"{x + x_},{y + y_}", True)
        else:
            raise Exception(
                f"A line must always contain an arrow, see line {line_counter} in file {map_name}")

        line_counter += 1

print(res)
