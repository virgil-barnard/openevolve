class PlayerBase:
    """
    Sub-classes must implement:
        decide(sensor_dict) -> str   (returns 'UP','DOWN','LEFT','RIGHT')
    """

    def decide(self, sensors):
        raise NotImplementedError("Players must override decide()")
