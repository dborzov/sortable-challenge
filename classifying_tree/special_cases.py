"""
   Consts for special matching cases
   (like that HP and Hewlett-Packard are the same thing)
"""

MANUFACTURER_SPECIAL_CASES = {
  "general electric": set([
    "general[\s-]*electric",
    "ge"
  ]),
  "fujifilm": set([
    "fuji[\s-]*film",
    "fuji"
  ]),
  "hp": set([
    "hp",
    "hewlett[\s-]*packard"
  ]),
  "konica minolta": set([
    "konica[\s-]*minolta",
    "konica",
    "minolta"
  ])
}
