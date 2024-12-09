from swarm import Agent, Result
from typing import Dict, Any
from ..utils.aptos_client import AptosClientWrapper

def analyze_portfolio_risk(context_variables: Dict[str, Any]) -> Result:
    """Analyzes portfolio composition and risks"""
    client = context_variables.get("aptos_client")
    address = context_variables.get("monitored_address")
    
    if not client or not address:
        return Result(value="Missing required context variables")
        
    balances = client.get_account_balance(address)
    
    # Calculate total portfolio value and asset concentrations
    total_value = sum(asset['value'] for asset in balances.values())
    concentrations = {
        asset_type: (asset['value'] / total_value * 100) 
        for asset_type, asset in balances.items()
    }
    
    # Check for frozen assets and high concentrations
    alerts = []
    for asset_type, asset in balances.items():
        if asset['is_frozen']:
            alerts.append(f"Warning: {asset_type} is frozen")
        if concentrations[asset_type] > 50:
            alerts.append(f"High concentration in {asset_type}: {concentrations[asset_type]:.1f}%")
    
    if alerts:
        from .alert_agent import alert_agent
        return Result(
            value=alerts,
            agent=alert_agent,
            context_variables={
                "alert_type": "portfolio_risk",
                "alerts": alerts
            }
        )
    
    return Result(value={"concentrations": concentrations})

portfolio_analyzer = Agent(
    name="Portfolio Analyzer",
    model="gpt-4",
    instructions="""You are a portfolio analysis agent responsible for monitoring and analyzing crypto portfolios.
    Your responsibilities:
    1. Track portfolio composition and total value
    2. Monitor concentration risk
    3. Analyze portfolio performance metrics
    4. Alert on risky conditions
    
    Pay special attention to:
    - Concentration risk (>50% in single asset)
    - Sudden value changes
    - Unusual transaction patterns""",
    functions=[analyze_portfolio_risk]
)