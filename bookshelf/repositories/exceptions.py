class ConflictError(Exception):
    def __init__(self, field: str):
        self._field = field
        super().__init__(f"Conflict with field {field}")

    @property
    def field(self) -> str:
        return self._field
