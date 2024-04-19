def control_coffee_grinder(action: str):
    """
    Control the coffee grinder of the Coffee Machine.

    Parameters:
        action (str): Action to perform on the coffee grinder. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the coffee grinder.
    """
    if action == 'on':
        return "Coffee grinder turned on."
    elif action == 'off':
        return "Coffee grinder turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."


def control_coffee_press(action: str):
    """
    Control the coffee press of the Coffee Machine.

    Parameters:
        action (str): Action to perform on the coffee press. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the coffee press.
    """
    if action == 'on':
        return "Coffee press turned on."
    elif action == 'off':
        return "Coffee press turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."
