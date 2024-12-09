from aptos_sdk.async_client import IndexerClient
from typing import Optionabol, Dict, Any
import asyncio

class AptosClientWrapper:
    def __init__(self, node_url: str):
        """Initialize Aptos client wrapper"""
        self.client = IndexerClient("https://api.mainnet.aptoslabs.com/v1/graphql")
        
    async def _get_account_resources(self, address: str) -> Dict[str, Any]:
        query = """
        query GetAccountResources($address: String) {
            current_fungible_asset_balances(
                where: {owner_address: {_eq: $address}}
            ) {
                amount
                asset_type
                is_frozen
            }
        }
        """
        variables = {"address": address}
        try:
            result = await self.client.query(query, variables)
            return result["data"]["current_fungible_asset_balances"]
        except Exception as e:
            print(f"Error fetching resources: {e}")
            return {}

    def get_account_balance(self, address: str) -> Dict[str, Any]:
        """Get account balance and resources"""
        try:
            resources = asyncio.run(self._get_account_resources(address))
            return {
                resource['asset_type']: {
                    'value': resource['amount'],
                    'is_frozen': resource['is_frozen']
                }
                for resource in resources
            }
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return {}

    async def _get_account_transactions(self, address: str, limit: int) -> list:
        query = """
        query GetAccountTransactions($address: String, $limit: Int) {
            account_transactions(
                where: {account_address: {_eq: $address}}
                order_by: {transaction_version: desc}
                limit: $limit
            ) {
                transaction_version
                fungible_asset_activities {
                    amount
                    asset_type
                    entry_function_id_str
                }
            }
        }
        """
        variables = {"address": address, "limit": limit}
        try:
            result = await self.client.query(query, variables)
            return result["data"]["account_transactions"]
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []

    def get_transactions(self, address: str, limit: int = 25) -> list:
        """Get recent transactions for an address"""
        try:
            return asyncio.run(self._get_account_transactions(address, limit))
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []