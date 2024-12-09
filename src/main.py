from swarm import Swarm
from utils.aptos_client import AptosClientWrapper
from utils.market_data import MarketDataClient
from agents.real_world_monitor import real_world_monitor
from agents.portfolio_analyzer import portfolio_analyzer
from agents.alert_agent import alert_agent
import time
import os

def main():
    # Initialize Swarm client
    client = Swarm()
    
    # Initialize service clients
    aptos_client = AptosClientWrapper("https://fullnode.mainnet.aptoslabs.com/v1")
    market_client = MarketDataClient(os.getenv("MARKET_API_KEY"))
    
    # Set up context variables
    context = {
        "aptos_client": aptos_client,
        "market_client": market_client,
        "monitored_address": os.getenv("MONITORED_ADDRESS", "0x1"),
        "monitored_tokens": ["apt", "eth", "btc"],
        "alert_thresholds": {
            "transaction_volume": 10,
            "price_change": 0.05,
            "portfolio_concentration": 50
        }
    }
    
    # Start monitoring loop
    while True:
        try:
            # Run market monitoring
            market_response = client.run(
                agent=real_world_monitor,
                messages=[{"role": "system", "content": "Begin market monitoring cycle"}],
                context_variables=context,
                debug=True
            )
            context.update(market_response.context_variables)
            
            # Run portfolio analysis
            portfolio_response = client.run(
                agent=portfolio_analyzer,
                messages=[{"role": "system", "content": "Begin portfolio analysis cycle"}],
                context_variables=context,
                debug=True
            )
            context.update(portfolio_response.context_variables)
            
            # Sleep between cycles
            time.sleep(60)
            
        except Exception as e:
            print(f"Error in monitoring cycle: {e}")
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()