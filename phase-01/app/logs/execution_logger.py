from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
from ..schemas.task_schema import ExecutionStep

console = Console()

class ExecutionLogger:
    @staticmethod
    def log(agent_name: str, action: str, details: str = None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = "green"
        if "Orchestrator" in agent_name:
            color = "cyan"
        elif "Sales" in agent_name:
            color = "yellow"
        elif "PM" in agent_name:
            color = "magenta"
        elif "Content" in agent_name:
            color = "blue"
        elif "Support" in agent_name:
            color = "red"

        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append(f"{agent_name}: ", style=f"bold {color}")
        text.append(action)
        if details:
            text.append(f" -> {details}", style="italic")
        
        console.print(text)

    @staticmethod
    def log_step(step: ExecutionStep):
        ExecutionLogger.log(step.agent_name, step.action, step.details)

    @staticmethod
    def display_final_response(response: str):
        console.print(Panel(response, title="Final Response", border_style="bold green"))
