from swarm import Agent, Result
from typing import Dict, Any
from ..utils.market_data import MarketDataClient

def monitor_price_changes(context_variables: Dict[str, Any]) -> Result:
    """monitor token prices and detect significant price movements.
    
    Args:
        context_variables: dictionary containing market_client, monitored_tokens, and thresholds
    """
    market_client: MarketDataClient = context_variables.get("market_client")
    tokens = context_variables.get("monitored_tokens", ["apt"])
    thresholds = context_variables.get("alert_thresholds", {})
    
    if not market_client:
        return Result(value="Error: Market client not initialized")
    
    price_changes = {}
    alerts = []
    
    for token in tokens:
        current_price = market_client.get_token_price(token)
        history = market_client.get_price_history(token)
        
        if not current_price or not history:
            continue
            
        price_24h_ago = history["prices"][0][1]
        price_change = (current_price - price_24h_ago) / price_24h_ago
        price_changes[token] = price_change
        
        if abs(price_change) > thresholds.get("price_change", 0.05):
            alerts.append({
                "token": token,
                "change": price_change,
                "current_price": current_price
            })
    
    if alerts:
        from .alert_agent import alert_agent
        return Result(
            value=alerts,
            agent=alert_agent,
            context_variables={
                "alert_type": "price_movement",
                "alerts": alerts,
                "severity": "high" if any(abs(a["change"]) > 0.1 for a in alerts) else "medium"
            }
        )
    
    return Result(value=price_changes)

real_world_monitor = Agent(
    name="Real World Monitor",
    model="gpt-4",
    instructions="""You are a market monitoring agent responsible for tracking real-time price movements in crypto markets.
    Your responsibilities:
    1. Monitor token prices across different markets
    2. Detect significant price movements
    3. Calculate price changes and volatility metrics
    4. Alert the alert agent when significant movements are detected
    
    When price movements exceed thresholds, immediately hand off to the alert agent with relevant context.""",
    functions=[monitor_price_changes]
)

