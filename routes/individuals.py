from flask import Blueprint
from controllers.individual_controller import individual_controller

individuals_bp = Blueprint('individuals', __name__)

# CRUD routes
individuals_bp.route('/individuals', methods=['POST'])(individual_controller.create_individual)
individuals_bp.route('/individuals', methods=['GET'])(individual_controller.get_all_individuals)
individuals_bp.route('/individuals/<string:individual_id>', methods=['GET'])(individual_controller.get_individual)
individuals_bp.route('/individuals/<string:individual_id>', methods=['PUT'])(individual_controller.update_individual)
individuals_bp.route('/individuals/<string:individual_id>', methods=['DELETE'])(individual_controller.delete_individual)

# Query routes
individuals_bp.route('/individuals/ranking', methods=['GET'])(individual_controller.get_wealth_ranking)
individuals_bp.route('/individuals/industry/<string:industry>', methods=['GET'])(individual_controller.get_individuals_by_industry)
individuals_bp.route('/individuals/search', methods=['GET'])(individual_controller.search_individuals)