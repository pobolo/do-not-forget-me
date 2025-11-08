import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.wealth_service import wealth_service

def seed_sample_data():
    """Seed the database with sample wealthy individuals data"""
    
    sample_individuals = [
        {
            'first_name': 'James',
            'last_name': 'Rutherford',
            'company': 'Rutherford Holdings',
            'title': 'CEO & Founder',
            'net_worth': 2100000000,
            'industry': 'Technology',
            'source_of_wealth': 'Software',
            'email': 'james.r@rutherfordholdings.com',
            'phone': '(212) 555-0101',
            'city': 'New York',
            'state': 'NY'
        },
        {
            'first_name': 'Sophia',
            'last_name': 'Chen',
            'company': 'Chen Capital',
            'title': 'Managing Partner',
            'net_worth': 850000000,
            'industry': 'Finance',
            'source_of_wealth': 'Investments',
            'email': 'sophia.chen@chencapital.com',
            'phone': '(415) 555-0102',
            'city': 'San Francisco',
            'state': 'CA'
        },
        {
            'first_name': 'Marcus',
            'last_name': 'Vanderbilt',
            'company': 'Vanderbilt Enterprises',
            'title': 'Chairman',
            'net_worth': 3500000000,
            'industry': 'Real Estate',
            'source_of_wealth': 'Inheritance & Development',
            'email': 'marcus@vanderbiltent.com',
            'phone': '(312) 555-0103',
            'city': 'Chicago',
            'state': 'IL'
        },
        {
            'first_name': 'Isabella',
            'last_name': 'Rodriguez',
            'company': 'TechNova Inc.',
            'title': 'Founder',
            'net_worth': 1200000000,
            'industry': 'Technology',
            'source_of_wealth': 'E-commerce',
            'email': 'isabella@technova.com',
            'phone': '(310) 555-0104',
            'city': 'Los Angeles',
            'state': 'CA'
        },
        {
            'first_name': 'Alexander',
            'last_name': 'Thompson',
            'company': 'Thompson Pharma',
            'title': 'CEO',
            'net_worth': 950000000,
            'industry': 'Healthcare',
            'source_of_wealth': 'Pharmaceuticals',
            'email': 'alex.thompson@thompsonpharma.com',
            'phone': '(617) 555-0105',
            'city': 'Boston',
            'state': 'MA'
        }
    ]
    
    sample_portfolios = [
        {
            'individual_id': '',  # Will be filled after individual creation
            'liquid_assets': 500000000,
            'real_estate_value': 800000000,
            'stock_portfolio_value': 600000000,
            'private_equity_value': 200000000,
            'risk_tolerance': 'Aggressive',
            'assets': ['Primary Residence', 'Commercial Real Estate', 'Tech Stocks'],
            'investments': ['VC Fund', 'Hedge Fund', 'Private Equity']
        },
        {
            'individual_id': '',
            'liquid_assets': 200000000,
            'real_estate_value': 300000000,
            'stock_portfolio_value': 250000000,
            'private_equity_value': 100000000,
            'risk_tolerance': 'Moderate',
            'assets': ['Multiple Properties', 'Blue Chip Stocks'],
            'investments': ['Growth Funds', 'Real Estate Trusts']
        }
    ]
    
    print("Seeding sample data...")
    
    # Create individuals
    created_individuals = []
    for individual_data in sample_individuals:
        try:
            individual = wealth_service.create_individual(individual_data)
            created_individuals.append(individual)
            print(f"Created individual: {individual.first_name} {individual.last_name}")
        except Exception as e:
            print(f"Error creating individual: {e}")
    
    # Create portfolios for first two individuals
    if len(created_individuals) >= 2:
        sample_portfolios[0]['individual_id'] = created_individuals[0].id
        sample_portfolios[1]['individual_id'] = created_individuals[1].id
        
        for portfolio_data in sample_portfolios:
            try:
                portfolio = wealth_service.create_portfolio(portfolio_data)
                print(f"Created portfolio for individual: {portfolio.individual_id}")
            except Exception as e:
                print(f"Error creating portfolio: {e}")
    
    print("Seed data completed!")
    print(f"Created {len(created_individuals)} individuals")
    
    # Display statistics
    stats = wealth_service.get_wealth_statistics()
    print(f"\nWealth Statistics:")
    print(f"Total individuals: {stats.get('total_individuals', 0)}")
    print(f"Total wealth: ${stats.get('total_wealth', 0):,.2f}")
    print(f"Average wealth: ${stats.get('average_wealth', 0):,.2f}")

if __name__ == '__main__':
    seed_sample_data()