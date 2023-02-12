from states.state_start import StateStart
from dotenv import load_dotenv


# Load env variables
load_dotenv()

# State Definition
start = StateStart()
start.run()
