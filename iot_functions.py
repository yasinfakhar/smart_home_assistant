import pygame


from typing import List
from langchain.tools import BaseTool, StructuredTool, tool


@tool
def turn_on_lamps(device_ids: List[int]) -> bool:
    """
    Turns on the lamps with the given device identifiers.

    Args:
        device_ids (List[str]): A list of device identifiers.

    Returns:
        bool: True if the lamps turned on successfully, False otherwise.
    """
    return True


@tool
def turn_off_lamps(device_ids: List[int]) -> bool:
    """
    Turns off the lamps with the given device identifiers.

    Args:
        device_ids (List[str]): A list of device identifiers.

    Returns:
        bool: True if the lamps turned off successfully, False otherwise.
    """

    return True


@tool
def activate_part_mode():
    """
    Activates the part mode.
    """
    pygame.mixer.init()
    # Load the music file
    pygame.mixer.music.load("music.mp3")
    # Play the music indefinitely (-1 indicates infinite loop)
    pygame.mixer.music.play(-1)


@tool
def deactivate_part_mode():
    """
    Deactivates the part mode.
    """
    pygame.mixer.music.stop()


def get_iot_functions():
    return [turn_off_lamps, turn_on_lamps, activate_part_mode, deactivate_part_mode]
