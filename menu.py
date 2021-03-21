from typing import Any, List, Dict, Callable, NamedTuple

from utils import get_key


NoneFunction = Callable[[], Any]


class MenuOption(NamedTuple):
    description: str
    function: NoneFunction


def menu(menu_text: str, options: List[MenuOption]):
    options_list: List[str] = []
    options_dict: Dict[str, NoneFunction] = {}
    for i, option in enumerate(options, start=1):
        options_list.append(f"{i}) {option.description}")
        options_dict[str(i)] = option.function
    options_text = '\n'.join(options_list)
    print(
        f"{menu_text}\n",
        "\n"
        "Options available:\n"
        "\n"
        f"{options_text}\n"
        "\n"
        "Please choose an option: ",
        end='',
    )
    key = get_key(lambda k: k in options_dict and k or None)
    print(f"{key}\n")
    return options_dict[key]()  # call the chosen option
