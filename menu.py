import shutil
import textwrap
from typing import List, Dict, Callable, NamedTuple, TypeVar

from utils import get_key

MenuReturn = TypeVar("MenuReturn")
MenuFunction = Callable[[], MenuReturn]

width, height = shutil.get_terminal_size()
text_wrapper = textwrap.TextWrapper(
    width=width, tabsize=4, replace_whitespace=False, break_on_hyphens=False
)


class MenuOption(NamedTuple):
    description: str
    function: MenuFunction


def menu(menu_text: str, options: List[MenuOption]) -> MenuReturn:
    options_list: List[str] = []
    options_dict: Dict[str, MenuFunction] = {}
    for i, option in enumerate(options, start=1):
        options_list.append(f"{i}) {option.description}")
        options_dict[str(i)] = option.function
    options_text = '\n'.join(options_list)
    print(
        f"{text_wrapper.fill(menu_text)}\n",
        "\n"
        "Options available:\n"
        "\n"
        f"{text_wrapper.fill(options_text)}"
    )
    key: str = get_key("Please choose an option: ", lambda k: k in options_dict and k or None)
    print(f"{key}\n")
    return options_dict[key]()  # call the chosen option
