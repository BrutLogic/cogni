from rich.console import Console
from rich.theme import Theme


class Logger:


    def debug(self, message: str):
        print(f"[red b u][[DEBUG]][blue]{message}")

    def _info(self, message: str):
        self.console.log(message, style="info")

    def warning(self, message: str):
        self.console.log(message, style="warning")

    def error(self, message: str):
        self.console.log(message, style="error")

    def critical(self, message: str):
        self.console.log(message, style="critical")

    def set_level(self, level):
        level_methods = {
            'debug': self.debug,
            'info': self.info,
            'warning': self.warning,
            'error': self.error,
            'critical': self.critical,
        }
        if level in level_methods:
            self._log_level_method = level_methods[level]
            self.console.log(f"Log level set to: {level}", style="info")
        else:
            self.console.log(f"Invalid log level: {level}. No changes made.", style="error")
    def log(self, message: str):
        if not hasattr(self, '_log_level_method'):
            self.set_level('debug')  # Default to debug level if not set
        self._log_level_method(message)

logger = Logger()
