def control_bedroom_light(action: str):
    """
    Control the Bedroom Light.

    Parameters:
        action (str): Action to perform on the bedroom light. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the bedroom light.
    """
    if action == 'on':
        return "Bedroom light turned on."
    elif action == 'off':
        return "Bedroom light turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."
