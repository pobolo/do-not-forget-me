import uuid
from datetime import datetime
from typing import Dict, Any, Optional

class WealthyIndividual:
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id', f"ind_{uuid.uuid4().hex[:8]}")
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.company = data['company']
        self.title = data['title']
        self.net_worth = float(data['net_worth'])
        self.industry = data['industry']
        self.source_of_wealth = data['source_of_wealth']
        self.email = data['email']
        self.phone = data.get('phone', '')
        self.city = data.get('city', '')
        self.state = data.get('state', '')
        self.wealth_tier = data.get('wealth_tier', self._calculate_wealth_tier())
        self.last_contact_date = data.get('last_contact_date', datetime.now().isoformat())
        self.created_at = data.get('created_at', datetime.now().isoformat())
        self.updated_at = datetime.now().isoformat()
    
    def _calculate_wealth_tier(self) -> str:
        if self.net_worth >= 1_000_000_000:
            return "Ultra High Net Worth"
        elif self.net_worth >= 500_000_000:
            return "High Net Worth"
        else:
            return "Affluent"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company': self.company,
            'title': self.title,
            'net_worth': self.net_worth,
            'industry': self.industry,
            'source_of_wealth': self.source_of_wealth,
            'email': self.email,
            'phone': self.phone,
            'city': self.city,
            'state': self.state,
            'wealth_tier': self.wealth_tier,
            'last_contact_date': self.last_contact_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WealthyIndividual':
        return cls(data)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company}) - ${self.net_worth:,.2f}"