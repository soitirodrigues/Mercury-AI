import json
from pathlib import Path

class TestFixtures:
    @staticmethod
    def load_fixture(fixture_name: str):
        """Load test fixture data from JSON files"""
        fixtures_dir = Path(__file__).parent / 'fixtures'
        if not fixtures_dir.exists():
            raise FileNotFoundError(f"Fixtures directory not found at {fixtures_dir}")

        fixture_path = fixtures_dir / f"{fixture_name}.json"
        if not fixture_path.exists():
            raise FileNotFoundError(f"Fixture {fixture_name} not found")

        with open(fixture_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def create_sample_decision_scenario():
        """Create a basic decision scenario fixture"""
        return {
            "context": {
                "risk_score": 0.75,
                "customer_profile": {
                    "age": 35,
                    "income": 85000,
                    "credit_history": ["good", "late_payment_2023"]
                },
                "transaction": {
                    "amount": 5000,
                    "type": "purchase",
                    "merchant": "Example Merchant"
                }
            },
            "expected": {
                "decision": "approve",
                "grade": "A2"
            }
        }

    @staticmethod
    def create_edge_case_scenario():
        """Create a complex edge case fixture"""
        return {
            "context": {
                "risk_score": 0.45,
                "customer_profile": {
                    "age": 25,
                    "income": 45000,
                    "credit_history": ["good", "late_payment_2022", "dispute_2023"]
                },
                "transaction": {
                    "amount": 12000,
                    "type": "cash_advance",
                    "merchant": "HighRiskMerchant"
                }
            },
            "expected": {
                "decision": "reject",
                "grade": "D4"
            }
        }

    @staticmethod
    def create_invalid_input():
        """Create a malformed input for error testing"""
        return {
            "context": "invalid_json",
            "transaction": 123,
            "customer_profile": True
        }

    @staticmethod
    def create_high_risk_scenario():
        """
        Create a high-risk transaction scenario with multiple risk factors
        """
        return {
            "context": {
                "risk_score": 0.92,
                "customer_profile": {
                    "age": 22,
                    "income": 30000,
                    "credit_history": ["late_payment_2023", "dispute_2023", "charge_off_2022"]
                },
                "transaction": {
                    "amount": 25000,
                    "type": "cash_advance",
                    "merchant": "VeryHighRiskMerchant"
                }
            },
            "expected": {
                "decision": "reject",
                "grade": "F7"
            }
        }

    @staticmethod
    def create_missing_data_scenario():
        """
        Create a scenario with missing required fields
        """
        return {
            "context": {},
            "transaction": {
                "amount": 500,
                "type": "purchase"
            }
        }

    @staticmethod
    def create_extreme_value_scenario():
        """
        Create a scenario with extreme values for stress testing
        """
        return {
            "context": {
                "risk_score": 1.0,
                "customer_profile": {
                    "age": 100,
                    "income": 1000000,
                    "credit_history": ["good"] * 20  # Long credit history
                },
                "transaction": {
                    "amount": 1000000,
                    "type": "purchase",
                    "merchant": "ExtremelyLargeTransactionMerchant"
                }
            },
            "expected": {
                "decision": "manual_review",
                "grade": "N/A"
            }
        }
