from flask import jsonify, request
from typing import Dict, Any
from services.wealth_service import wealth_service

class IndividualController:
    @staticmethod
    def create_individual():
        try:
            data = request.get_json()
            individual = wealth_service.create_individual(data)
            return jsonify({
                'success': True,
                'individual': individual.to_dict()
            }), 201
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @staticmethod
    def get_individual(individual_id: str):
        try:
            individual = wealth_service.get_individual(individual_id)
            if individual:
                return jsonify({
                    'success': True,
                    'individual': individual.to_dict()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Individual not found'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @staticmethod
    def update_individual(individual_id: str):
        try:
            data = request.get_json()
            individual = wealth_service.update_individual(individual_id, data)
            return jsonify({
                'success': True,
                'individual': individual.to_dict()
            })
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @staticmethod
    def delete_individual(individual_id: str):
        try:
            success = wealth_service.delete_individual(individual_id)
            return jsonify({
                'success': True,
                'message': 'Individual deleted successfully'
            })
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @staticmethod
    def get_all_individuals():
        try:
            individuals = wealth_service.get_all_individuals()
            return jsonify({
                'success': True,
                'individuals': [ind.to_dict() for ind in individuals],
                'count': len(individuals)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @staticmethod
    def get_wealth_ranking():
        try:
            limit = request.args.get('limit', 10, type=int)
            ranking = wealth_service.get_wealth_ranking(limit)
            return jsonify({
                'success': True,
                'ranking': ranking,
                'limit': limit
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @staticmethod
    def get_individuals_by_industry(industry: str):
        try:
            individuals = wealth_service.get_individuals_by_industry(industry)
            return jsonify({
                'success': True,
                'industry': industry,
                'individuals': [ind.to_dict() for ind in individuals],
                'count': len(individuals)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @staticmethod
    def search_individuals():
        try:
            query = request.args.get('q', '')
            if not query:
                return jsonify({
                    'success': False,
                    'error': 'Query parameter "q" is required'
                }), 400
            
            individuals = wealth_service.search_individuals(query)
            return jsonify({
                'success': True,
                'query': query,
                'individuals': [ind.to_dict() for ind in individuals],
                'count': len(individuals)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

individual_controller = IndividualController()