import re


BAD_C_NAME_PATTERN = re.compile('[^a-zA-Z_0-9:]')


def demangled_name_to_c_str(name):
    """
    Removes or replaces characters from demangled symbol so that it was possible to create legal C structure from it
    """
    if not BAD_C_NAME_PATTERN.findall(name):
        return name
    idx = name.find("operator")
    if idx >= 0:
        idx += len("operator")
        if name[idx:idx + 2] == "==":
            name = name.replace("operator==", "operator_EQ_")
        elif name[idx:idx + 2] == "!=":
            name = name.replace("operator!=", "operator_NEQ_")
        elif name[idx] == "=":
            name = name.replace("operator=", "operator_ASSIGN_")
        elif name[idx:idx + 2] == "++":
            name = name.replace("operator++", "operator_INC_")
        elif name[idx:idx + 2] == "--":
            name = name.replace("operator*", "operator_PTR_")
        elif name[idx:idx + 2] == "->":
            name = name.replace("operator->", "operator_REF_")
        elif name[idx:idx + 2] == "[]":
            name = name.replace("operator[]", "operator_IDX_")
        elif name[idx] == "*":
            name = name.replace("operator*", "operator_PTR_")
        elif name[idx:idx + 2] == "&&":
            name = name.replace("operator&&", "operator_LAND_")
        elif name[idx:idx + 2] == "||":
            name = name.replace("operator||", "operator_LOR_")
        elif name[idx] == "!":
            name = name.replace("operator!", "operator_LNOT_")
        elif name[idx] == "&":
            name = name.replace("operator&", "operator_AND_")
        elif name[idx] == "|":
            name = name.replace("operator|", "operator_OR_")
        elif name[idx] == "^":
            name = name.replace("operator^", "operator_XOR_")
        elif name[idx:idx + 2] == "<<":
            name = name.replace("operator<<", "operator_LEFT_SHIFT_")
        elif name[idx:idx + 2] == ">>":
            name = name.replace("operator>>", "operator_RIGHT_SHIFT_")
        elif name[idx] == "+":
            name = name.replace("operator*", "operator_ADD_")
        elif name[idx] == "-":
            name = name.replace("operator*", "operator_SUB_")
        elif name[idx] == "*":
            name = name.replace("operator*", "operator_SUB_")
        elif name[idx] == "/":
            name = name.replace("operator*", "operator_DIV_")
        elif name[idx: idx + 4] == " new":
            name = name.replace("operator new", "operator_NEW_")
        elif name[idx: idx + 7] == " delete":
            name = name.replace("operator delete", "operator_DELETE_")
        elif name[idx] == ' ':
            pass
        else:
            raise AssertionError("Replacement of demangled string by c-string for keyword `operatorXXX` is not yet"
                                 "implemented ({}). You can do it by yourself or create an issue".format(name))

    name = name.replace("~", "DESTRUCTOR_")
    name = name.replace("*", "_PTR")
    name = name.replace("<", "_t_")
    name = name.replace(">", "_t_")
    name = "_".join(filter(len, BAD_C_NAME_PATTERN.split(name)))
    return name