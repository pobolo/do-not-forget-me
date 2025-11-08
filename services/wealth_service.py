import logging
from typing import Dict, Any, List, Optional
from models.wealthy_individual import WealthyIndividual
from models.portfolio import Portfolio
from services.redis_service import redis_service

logger = logging.getLogger(__name__)

class WealthService:
    def __init__(self):
        self.individual_prefix = "individual:"
        self.portfolio_prefix = "portfolio:"
        self.individuals_set_key = "individuals:all"
        self.wealth_ranking_key = "wealth:ranking"
        self.industry_index_key = "industry:index"
    
    # Individual CRUD operations
    def create_individual(self, individual_data: Dict[str, Any]) -> WealthyIndividual:
        try:
            individual = WealthyIndividual(individual_data)
            individual_key = f"{self.individual_prefix}{individual.id}"
            
            # Store individual data
            redis_service.set(individual_key, individual.to_dict())
            
            # Add to individuals set
            redis_service.sadd(self.individuals_set_key, individual.id)
            
            # Add to wealth ranking sorted set
            redis_service.zadd(self.wealth_ranking_key, {
                individual.id: individual.net_worth
            })
            
            # Add to industry index
            industry_key = f"{self.industry_index_key}:{individual.industry}"
            redis_service.sadd(industry_key, individual.id)
            
            logger.info(f"Created individual: {individual.id}")
            return individual
            
        except Exception as e:
            logger.error(f"Error creating individual: {e}")
            raise
    
    def get_individual(self, individual_id: str) -> Optional[WealthyIndividual]:
        try:
            individual_key = f"{self.individual_prefix}{individual_id}"
            cached = redis_service.get(individual_key)
            
            if cached:
                logger.info(f"Cache hit for individual: {individual_id}")
                return WealthyIndividual.from_dict(cached)
            
            logger.info(f"Cache miss for individual: {individual_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting individual {individual_id}: {e}")
            raise
    
    def update_individual(self, individual_id: str, update_data: Dict[str, Any]) -> Optional[WealthyIndividual]:
        try:
            existing = self.get_individual(individual_id)
            if not existing:
                raise ValueError(f"Individual {individual_id} not found")
            
            # Merge existing data with updates
            updated_data = {**existing.to_dict(), **update_data}
            updated_individual = WealthyIndividual(updated_data)
            
            individual_key = f"{self.individual_prefix}{individual_id}"
            redis_service.set(individual_key, updated_individual.to_dict())
            
            # Update wealth ranking if net worth changed
            if 'net_worth' in update_data and update_data['net_worth'] != existing.net_worth:
                redis_service.zadd(self.wealth_ranking_key, {
                    updated_individual.id: updated_individual.net_worth
                })
            
            return updated_individual
            
        except Exception as e:
            logger.error(f"Error updating individual {individual_id}: {e}")
            raise
    
    def delete_individual(self, individual_id: str) -> bool:
        try:
            individual = self.get_individual(individual_id)
            if not individual:
                raise ValueError(f"Individual {individual_id} not found")
            
            individual_key = f"{self.individual_prefix}{individual_id}"
            
            # Remove from main storage
            redis_service.delete(individual_key)
            
            # Remove from individuals set
            redis_service.srem(self.individuals_set_key, individual.id)
            
            # Remove from wealth ranking
            redis_service.zrem(self.wealth_ranking_key, individual.id)
            
            # Remove from industry index
            industry_key = f"{self.industry_index_key}:{individual.industry}"
            redis_service.srem(industry_key, individual.id)
            
            logger.info(f"Deleted individual: {individual_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting individual {individual_id}: {e}")
            raise
    
    # Portfolio operations
    def create_portfolio(self, portfolio_data: Dict[str, Any]) -> Portfolio:
        try:
            portfolio = Portfolio(portfolio_data)
            portfolio_key = f"{self.portfolio_prefix}{portfolio.id}"
            individual_portfolio_key = f"{self.individual_prefix}{portfolio.individual_id}:portfolio"
            
            redis_service.set(portfolio_key, portfolio.to_dict())
            redis_service.set(individual_portfolio_key, portfolio.to_dict())
            
            return portfolio
            
        except Exception as e:
            logger.error(f"Error creating portfolio: {e}")
            raise
    
    def get_portfolio_by_individual_id(self, individual_id: str) -> Optional[Portfolio]:
        try:
            individual_portfolio_key = f"{self.individual_prefix}{individual_id}:portfolio"
            cached = redis_service.get(individual_portfolio_key)
            
            if cached:
                return Portfolio.from_dict(cached)
            return None
            
        except Exception as e:
            logger.error(f"Error getting portfolio for individual {individual_id}: {e}")
            raise
    
    # Query operations
    def get_all_individuals(self) -> List[WealthyIndividual]:
        try:
            individual_ids = redis_service.smembers(self.individuals_set_key)
            individuals = []
            
            for individual_id in individual_ids:
                individual = self.get_individual(individual_id)
                if individual:
                    individuals.append(individual)
            
            return individuals
            
        except Exception as e:
            logger.error(f"Error getting all individuals: {e}")
            raise
    
    def get_wealth_ranking(self, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            ranked_ids = redis_service.zrevrange(self.wealth_ranking_key, 0, limit - 1, withscores=True)
            ranking = []
            
            for individual_id, net_worth in ranked_ids:
                individual = self.get_individual(individual_id)
                if individual:
                    ranking.append({
                        'individual': individual.to_dict(),
                        'net_worth': net_worth
                    })
            
            return ranking
            
        except Exception as e:
            logger.error(f"Error getting wealth ranking: {e}")
            raise
    
    def get_individuals_by_industry(self, industry: str) -> List[WealthyIndividual]:
        try:
            industry_key = f"{self.industry_index_key}:{industry}"
            individual_ids = redis_service.smembers(industry_key)
            individuals = []
            
            for individual_id in individual_ids:
                individual = self.get_individual(individual_id)
                if individual:
                    individuals.append(individual)
            
            return individuals
            
        except Exception as e:
            logger.error(f"Error getting individuals by industry {industry}: {e}")
            raise
    
    def search_individuals(self, query: str) -> List[WealthyIndividual]:
        try:
            all_individuals = self.get_all_individuals()
            search_term = query.lower()
            
            return [
                ind for ind in all_individuals
                if (search_term in ind.first_name.lower() or
                    search_term in ind.last_name.lower() or
                    search_term in ind.company.lower() or
                    search_term in ind.industry.lower())
            ]
            
        except Exception as e:
            logger.error(f"Error searching individuals: {e}")
            raise
    
    # Analytics
    def get_wealth_statistics(self) -> Dict[str, Any]:
        try:
            all_individuals = self.get_all_individuals()
            
            if not all_individuals:
                return {}
            
            total_wealth = sum(ind.net_worth for ind in all_individuals)
            avg_wealth = total_wealth / len(all_individuals)
            max_wealth = max(ind.net_worth for ind in all_individuals)
            min_wealth = min(ind.net_worth for ind in all_individuals)
            
            # Wealth tier distribution
            wealth_tiers = {}
            for ind in all_individuals:
                wealth_tiers[ind.wealth_tier] = wealth_tiers.get(ind.wealth_tier, 0) + 1
            
            # Industry distribution
            industries = {}
            for ind in all_individuals:
                industries[ind.industry] = industries.get(ind.industry, 0) + 1
            
            return {
                'total_individuals': len(all_individuals),
                'total_wealth': total_wealth,
                'average_wealth': avg_wealth,
                'max_wealth': max_wealth,
                'min_wealth': min_wealth,
                'wealth_tier_distribution': wealth_tiers,
                'industry_distribution': industries
            }
            
        except Exception as e:
            logger.error(f"Error getting wealth statistics: {e}")
            raise
    
    def get_redis_info(self) -> Dict[str, Any]:
        try:
            info = redis_service.info()
            return {
                'connected_clients': info.get('connected_clients', 0),
                'used_memory_human': info.get('used_memory_human', '0'),
                'used_memory_peak_human': info.get('used_memory_peak_human', '0'),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'total_commands_processed': info.get('total_commands_processed', 0)
            }
        except Exception as e:
            logger.error(f"Error getting Redis info: {e}")
            raise

# Global instance
wealth_service = WealthService()