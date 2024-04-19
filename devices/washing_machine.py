def control_wash_normal(action: str):
    """
    Control the normal wash setting of the Dishwasher.

    Parameters:
        action (str): Action to perform on the normal wash setting. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the normal wash setting.
    """
    if action == 'on':
        return "Normal wash setting turned on."
    elif action == 'off':
        return "Normal wash setting turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."


def control_wash_quick(action: str):
    """
    Control the quick wash setting of the Dishwasher.

    Parameters:
        action (str): Action to perform on the quick wash setting. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the quick wash setting.
    """
    if action == 'on':
        return "Quick wash setting turned on."
    elif action == 'off':
        return "Quick wash setting turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."


def control_wash_delicate(action: str):
    """
    Control the delicate wash setting of the Dishwasher.

    Parameters:
        action (str): Action to perform on the delicate wash setting. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the delicate wash setting.
    """
    if action == 'on':
        return "Delicate wash setting turned on."
    elif action == 'off':
        return "Delicate wash setting turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."

