import asyncio
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from app.orchestration.workflow_manager import WorkflowManager
from app.logs.execution_logger import ExecutionLogger

console = Console()

async def main():
    console.print(Panel.fit(
        "[bold cyan]AI Business Operations Manager[/bold cyan]\n"
        "[dim]Stage 1: Multi-Agent System (CLI)[/dim]",
        border_style="cyan"
    ))

    workflow_manager = WorkflowManager()

    while True:
        try:
            user_input = Prompt.ask("\n[bold green]How can the AI workforce help you today?[/bold green]")
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                console.print("[yellow]Shutting down AI workforce. Goodbye![/yellow]")
                break

            if not user_input.strip():
                continue

            console.print("\n[bold]Starting autonomous workflow...[/bold]")
            
            final_response = await workflow_manager.execute_workflow(user_input)
            
            ExecutionLogger.display_final_response(final_response)

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
