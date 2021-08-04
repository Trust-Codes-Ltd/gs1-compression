"""tableS1 is used for the semantic interpretation and expresses
which simple keys or compound keys are instance identifiers
(uniquely identifying only one thing globally)."""
# TODO extend tableS1 fully.
# Format is primary key : null or list of AIs of which one must be specified.
TABLE_S1 = {"01": {"requires": ["21", "235"]}, "00": {"requires": None},
            "8006": {"requires": ["21"]}, "8010": {"requires": ["8011"]},
            "8004": {"requires": None}, "8003": {"minLength": 15},
            "253": {"minLength": 14}, "254": {"minLength": 14}}
# this is incomplete but sufficient for initial testing
