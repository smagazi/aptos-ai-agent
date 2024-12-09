"""
File: real_world_monitor.py
Purpose: Monitors real-time cryptocurrency price movements and triggers alerts

Interactions:
- Depends on: ../utils/market_data.py for MarketDataClient
- Calls: alert_agent.py when price movements exceed thresholds
- Used by: main.py for market monitoring functionality

Key Features:
- Monitors token prices across markets
- Calculates price changes over 24h periods
- Triggers alerts based on configurable thresholds
- Supports multiple tokens (default: "apt")

Note: Requires a properly initialized market_client in context_variables
"""

"""
File: transaction_monitor.py
Purpose: Monitors blockchain transactions for unusual patterns and volume

Interactions:
- Depends on: ../utils/aptos_client.py for blockchain interaction
- Calls: alert_agent.py when unusual activity is detected
- Used by: main.py for transaction monitoring

Key Features:
- Analyzes transaction volumes
- Detects unusual activity patterns
- Configurable volume thresholds
- Automatic alerting system

Note: Requires AptosClientWrapper instance and monitored_address in context_variables
"""

"""
File: aptos_client.py
Purpose: Wrapper for Aptos blockchain interaction functionality

Interactions:
- Used by: ../agents/transaction_monitor.py, ../agents/portfolio_analyzer.py
- Depends on: aptos_sdk external package

Key Features:
- Account management and initialization
- Balance checking
- Transaction history retrieval
- Error handling for API calls

Note: Requires aptos-sdk package to be installed
Dependencies: pip install aptos-sdk
"""


"""
File: alert_agent.py
Purpose: Processes and delivers alerts from monitoring agents

Interactions:
- Called by: real_world_monitor.py, transaction_monitor.py
- Used by: main.py for alert handling

Key Features:
- Alert formatting and prioritization
- Severity level determination
- Multi-channel alert delivery
- Configurable alert thresholds

Note: Alert delivery channels should be configured in context_variables
"""

"""
File: portfolio_analyzer.py
Purpose: Analyzes cryptocurrency portfolio performance and metrics

Interactions:
- Depends on: ../utils/aptos_client.py for blockchain data
- Used by: main.py for portfolio analysis

Key Features:
- Portfolio value calculation
- Performance metrics
- Asset distribution analysis
- Historical performance tracking

Note: Requires AptosClientWrapper instance in context_variables
"""

"""
File: main.py
Purpose: Entry point for the financial monitoring system

Interactions:
- Imports and orchestrates all agent modules
- Initializes necessary clients and configurations
- Manages agent execution flow

Key Features:
- System initialization
- Agent coordination
- Configuration management
- Error handling and logging

Note: Run this file to start the monitoring system
Usage: python src/main.py
"""