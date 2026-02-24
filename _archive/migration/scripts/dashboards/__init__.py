"""
Dashboard Generators

Produces Dataview-powered markdown files for Obsidian firm and case dashboards.
All Dataview queries use FROM "cases" or FROM "_entity/{role}" scoping for
performance at 14K+ file vault scale.
"""

from dashboards.firm_dashboard import generate_firm_dashboard
from dashboards.case_dashboard import generate_case_dashboard_template

__all__ = [
    "generate_firm_dashboard",
    "generate_case_dashboard_template",
]
