import re


def get_base(path):
    """
    :param str path:
    :return: Base
    :rtype: str
    """
    return path.split("|")[-1]


def get_name(path):
    """
    :param str path:
    :return: Name
    :rtype: str
    """
    return get_base(path).split(":")[-1]


def get_namespace(path):
    """
    :param str path:
    :return: Namespace
    :rtype: str/None
    """
    base = get_base(path)
    if base.find(":") != -1:
        return base.split(":")[0]


def split_component(path):
    """
    Split a path in its node, component and values. If the path doesn't
    contain any components or values None's will be returned for these
    elements. The splitting of the node and components are very straight
    forward as they can be split on a "." and a "[" character. The values
    are a bit different. Values can be presented as a range with the ":"
    if that character is found a range will be returned. It is also possible
    that the component takes a number of values, thinking about uv, map etc.
    These will be represented as a tuple. As there is so many possibilities
    of output it is up to the user to know what the input is and what the
    expected output would be of that string.

    :param str path:
    :return: Node, component, values
    :rtype: str, str, int/tuple/list
    """
    def split_to_node_and_attribute(path):
        """
        If a "." character is found in the path. It will split the path on
        the first instance of that character. The first part is the node,
        the second the attribute.

        :param str path:
        :return: Node, attribute
        :rtype: str, str/None
        """
        # validate path
        if not path.count("."):
            return path, None

        # split path
        return path.split(".", 1)

    def split_to_component_and_string_values(attr):
        """
        If a "[" character is found in the attr. It will split the attr on
        the first instance of that character. In the return of the values
        the "[" character is still present.

        :param str/None attr:
        :return: Component, values
        :rtype: str/None, str/None
        """
        if attr is None or not attr.count("["):
            return attr, None

        index = attr.index("[")
        values = attr[index:]
        component = attr[:index]

        return component, values

    def process_string_value(string_value):
        """
        Process the string value and convert it into either a range if a
        ":" character is present in the string. Or a float or an int depending
        on if a "." character is present in the scene.

        :param str string_value:
        :return: Value
        :rtype: int/float/list
        """
        if string_value.count(":"):
            values = [
                int(v) + i
                for i, v in enumerate(string_value.split(":"))
                if v.isdigit()
            ]

            if len(values) != 2:
                raise RuntimeError("Unable to process string value: '{}'!".format(string_value))

            return range(*values)
        else:
            return float(string_value) if string_value.count(".") else int(string_value)

    def process_string_values(string_values):
        """
        Find the values between the "[" and "]" character and loop these
        values and convert them into ranges, floats or ints using the
        process_string_value function. Depending on the length of the
        list and the type the process_string_value function returns, the
        return type of this function may vary.

        :param str/None string_values:
        :return: Values
        :rtype: int/float/list/tuple
        """
        # validate values
        if string_values is None:
            return None

        # split values from brackets
        values = re.findall("(?<=\[).+?(?=\])", string_values)

        if len(values) == 1:
            return process_string_value(values[0])
        else:
            return tuple(
                process_string_value(v)
                for v in values
            )

    # do splits
    node, attr = split_to_node_and_attribute(path)
    component, string_values = split_to_component_and_string_values(attr)
    values = process_string_values(string_values)

    return node, component, values


def as_list(l):
    """
    Force the provided argument as a list.

    :param str/list/tuple l:
    :return: List
    :rtype: list
    """
    if l is None:
        return []
    elif type(l) == tuple:
        return list(l)
    elif type(l) != list:
        return [l]

    return l


def split_list(l, n):
    """
    Split a list into chunks.

    :param list l:
    :param int n:
    :return: Split list
    :rtype: list
    """
    return list(l[i:i + n] for i in xrange(0, len(l), n))
