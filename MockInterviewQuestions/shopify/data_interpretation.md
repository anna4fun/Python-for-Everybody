#  Data interpretation + visualization: traffic spike with worse funnel
You’re given a dataset with 3 years of daily metrics for the App Store. You notice:

A large traffic spike that is not explained by normal seasonality.
Add-to-cart (ATC) rate drops sharply during the spike.
Conversion rate drops slightly.
Assume the table below (you may create derived fields like YoY, WoW, and rolling averages):

Table: daily_app_store_metrics
"""
date (DATE)
sessions (INT) — total visits to the App Store
product_views (INT)
add_to_cart (INT)
purchases (INT)
revenue (NUMERIC)
channel (STRING) — e.g., organic, paid_search, email, affiliate, referral
device_type (STRING) — desktop/mobile/tablet
geo (STRING)
merchant_tier (STRING) — e.g., trial/basic/plus
landing_page (STRING)
app_category (STRING)
is_bot_suspected (BOOL) — if available
"""

Tasks
1. List plausible hypotheses that could cause sessions ↑ while ATC rate ↓ and conversion ↓/flat (cover both product and data-quality causes).
2. Propose the most useful charts you would build (in Python or Google Sheets) to validate/refute your hypotheses.
3. Explain what follow-up data you would request if the dataset is insufficient.

Define rates as:
ATC_rate = add_to_cart / product_views (or justify an alternative)
CVR = purchases / sessions
Output expected: a structured investigation plan plus the key visualizations you’d generate.