import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

class Portfolio:
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id', f"port_{uuid.uuid4().hex[:8]}")
        self.individual_id = data['individual_id']
        self.assets = data.get('assets', [])
        self.investments = data.get('investments', [])
        self.liquid_assets = float(data.get('liquid_assets', 0))
        self.real_estate_value = float(data.get('real_estate_value', 0))
        self.stock_portfolio_value = float(data.get('stock_portfolio_value', 0))
        self.private_equity_value = float(data.get('private_equity_value', 0))
        self.risk_tolerance = data.get('risk_tolerance', 'Moderate')  # Conservative, Moderate, Aggressive
        self.last_valuation_date = data.get('last_valuation_date', datetime.now().isoformat())
        self.created_at = data.get('created_at', datetime.now().isoformat())
        self.updated_at = datetime.now().isoformat()
    
    @property
    def total_value(self) -> float:
        return (self.liquid_assets + self.real_estate_value + 
                self.stock_portfolio_value + self.private_equity_value)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'individual_id': self.individual_id,
            'assets': self.assets,
            'investments': self.investments,
            'liquid_assets': self.liquid_assets,
            'real_estate_value': self.real_estate_value,
            'stock_portfolio_value': self.stock_portfolio_value,
            'private_equity_value': self.private_equity_value,
            'total_value': self.total_value,
            'risk_tolerance': self.risk_tolerance,
            'last_valuation_date': self.last_valuation_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Portfolio':
        return cls(data)
    
    def __str__(self):
        return f"Portfolio {self.id} - Total Value: ${self.total_value:,.2f}"