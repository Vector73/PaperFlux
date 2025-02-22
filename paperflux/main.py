import signal
import sys
from src.scheduler.jobs import PaperProcessingScheduler
from src.web.app import PaperFluxUI
import threading

def signal_handler(signum, frame):
    print("\nShutting down gracefully...")
    scheduler.stop()
    sys.exit(0)

def main():
    global scheduler
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the scheduler in a background thread
    scheduler = PaperProcessingScheduler()
    scheduler_thread = threading.Thread(target=scheduler.start, daemon=True)
    scheduler_thread.start()

    # Create and launch the Gradio interface
    ui = PaperFluxUI()
    interface = ui.create_interface()
    interface.launch(server_name="0.0.0.0", share=True)

if __name__ == "__main__":
    main()