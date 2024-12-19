from agentix import tool
from typing import Optional, List, Dict, Union

@tool
def TF_run_command(
    command: str,
    session_name: Optional[str] = None,
    timeout: Optional[int] = None
) -> str:
    """Execute a command in a terminal session"""
    ...

@tool
def TF_ensure_session(
    session_name: str,
    session_type: str = "shell",
    config: Optional[Dict] = None
) -> bool:
    """Ensure a terminal session exists and is properly configured"""
    ...

@tool
def TF_set_current_session(session_name: str) -> bool:
    """Set the active terminal session"""
    ...

@tool
def TF_run_python_file(
    file_path: str,
    args: Optional[List[str]] = None,
    env: Optional[Dict[str, str]] = None
) -> str:
    """Execute a Python file in a dedicated session"""
    ...

@tool
def TF_get_session_output(
    session_name: str,
    last_n_lines: Optional[int] = None
) -> List[str]:
    """Get output from a terminal session"""
    ...

@tool
def TF_send_input(
    session_name: str,
    input_text: str,
    end: str = "\n"
) -> bool:
    """Send input to a terminal session"""
    ...

@tool
def TF_wait_for_pattern(
    session_name: str,
    pattern: str,
    timeout: Optional[int] = None
) -> bool:
    """Wait for a specific pattern in terminal output"""
    ...
