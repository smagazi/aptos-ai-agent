from swarm import Agent, Result
from typing import Dict, Any

def send_alert(context_variables: Dict[str, Any]) -> Result:
    """Send alerts through configured channels based on alert type and severity.
    
    Args:
        context_variables: Dictionary containing alert_type, alerts, and severity
    """
    alert_type = context_variables.get("alert_type", "general")
    alerts = context_variables.get("alerts", [])
    severity = context_variables.get("severity", "medium")
    
    # Format alert message based on type
    if alert_type == "price_movement":
        message = "Price Movement Alert:\n" + "\n".join(
            f"- {alert['token']}: {alert['change']*100:.1f}% change to ${alert['current_price']:.2f}"
            for alert in alerts
        )
    elif alert_type == "portfolio_risk":
        message = "Portfolio Risk Alert:\n" + "\n".join(
            f"- High concentration in {alert['token']}: {alert['percentage']:.1f}%"
            for alert in alerts
        )
    else:
        message = f"General Alert: {alerts}"
    
    alert_message = f"[{severity.upper()}] {message}"
    print(f"\nALERT: {alert_message}\n")
    
    return Result(
        value=f"Alert sent: {alert_message}",
        context_variables={"last_alert": alert_message}
    )

alert_agent = Agent(
    name="Alert Agent",
    model="gpt-4",
    instructions="""You are an alert management agent responsible for processing and delivering alerts.
    Your responsibilities:
    1. Process incoming alerts from other agents
    2. Format alerts appropriately based on type
    3. Determine alert priority and severity
    4. Deliver alerts through appropriate channels
    
    Handle alerts with appropriate urgency based on severity level.""",
    functions=[send_alert]
)