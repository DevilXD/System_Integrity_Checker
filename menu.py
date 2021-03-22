import shutil
from typing import List, Dict, Callable, NamedTuple, TypeVar

from utils import get_key

MenuReturn = TypeVar("MenuReturn")
MenuFunction = Callable[[], MenuReturn]

width, height = shutil.get_terminal_size()


def clean_lines(text: str) -> str:
    final_lines = []
    for line in text.split('\n'):
        while True:
            if len(line) > width and (j := line.rfind(' ', 0, width)) >= 0:
                final_lines.append(line[:j])
                line = line[j+1:]
            else:
                final_lines.append(line)
                break
    return '\n'.join(final_lines)


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
        f"{clean_lines(menu_text)}\n",
        f"\n"
        "Options available:\n"
        "\n"
        f"{clean_lines(options_text)}"
    )
    key: str = get_key("Please choose an option: ", lambda k: k in options_dict and k or None)
    return options_dict[key]()  # call the chosen option
