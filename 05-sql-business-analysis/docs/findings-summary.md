# Findings Summary - Olist SQL Business Analysis

## Executive Summary

- Delivered-order revenue totals **R$15.42M** including freight. São Paulo contributes **R$5.77M (37.4%)**, while the five largest states contribute **73.2%**.
- Product demand is broad: the top five categories produce **39.8%** of product revenue. `health_beauty` leads at **R$1.23M**, followed by `watches_gifts` at **R$1.17M**.
- Delivery reliability is strongly associated with customer sentiment. Late orders average **2.57 stars** versus **4.29** for on-time/early orders; **46.1%** of late orders receive one star.
- Credit cards account for **78.5%** of delivered-order payment value and average **3.5 installments**, making installment behavior commercially material.
- The customer base is acquisition-heavy: one-time buyers generate **94.4%** of revenue. Repeat buyers are only 2,801 customers, but their average lifetime value is **R$308.53**, nearly twice the one-time-buyer average of **R$160.73**.

The operational priority is delivery reliability in high-risk states and sellers. The commercial opportunity is retention: repeat customers are scarce but substantially more valuable. Geography and category concentration should guide where service improvements and lifecycle campaigns are tested first.

## Query Findings

### 1. Revenue by State

São Paulo leads with **40,501 delivered orders** and **R$5.77M** in total revenue. Rio de Janeiro and Minas Gerais add **R$2.06M** and **R$1.82M**. The concentration creates scale advantages, but also means service failures in the Southeast can affect a large share of the business.

### 2. Top Product Categories

`health_beauty` generates the most product revenue at **R$1.23M**. `watches_gifts` is second at **R$1.17M** despite lower unit volume, supported by a **R$199.04** average item price. `bed_bath_table` leads unit volume among the top categories with **10,953 items**.

### 3. Monthly Revenue by Category

Across the ten largest categories, **November 2017** is the strongest month at **R$642.9K** in product revenue, consistent with a year-end promotional peak. March-May 2018 also forms a sustained high-revenue period. Monthly output should be interpreted cautiously at the dataset boundaries because 2016 and late 2018 are partial.

### 4. Top Customers by Lifetime Value

The highest observed customer lifetime value is **R$13,664.08**, generated in one order. Most top-spending identities also derive their value from a single high-ticket purchase, so this ranking is primarily a high-order-value list rather than evidence of broad loyalty.

### 5. Delivery Performance by State

Among states with at least 100 delivered orders, Alagoas has the highest late-delivery rate at **23.93%** and averages **24.04 days** to delivery. Maranhão follows at **19.67%** late. Paraná, Minas Gerais, and São Paulo combine meaningful scale with late rates near **5-6%**, providing useful operational benchmarks.

### 6. Payment Method Mix

Credit cards represent **R$12.10M (78.46%)** of payment value. Boleto contributes **17.96%**. Credit-card payments average **3.5 installments**, while the other payment types average one, highlighting the importance of installment economics and authorization performance.

### 7. Review Score and Delivery Analysis

Late delivery is associated with a severe downward shift in reviews: **46.21%** of late orders receive one star and only **22.23%** receive five stars. For on-time/early orders, only **6.59%** receive one star while **62.44%** receive five stars. This is an association, not a causal estimate, but the magnitude makes delivery reliability an obvious experience lever.

### 8. Seller Performance Scorecard

The largest seller in the scorecard produces **R$226,987.93** with a **4.15** average review and **11.57%** late rate. Seller `7e93...753a` provides a more balanced benchmark: **R$165,981.49**, **4.36** stars, and **5.64%** late. Revenue alone is therefore insufficient for seller governance.

### 9. Repeat Customer Revenue

One-time customers contribute **R$14.56M (94.4%)**. Repeat customers contribute only **5.6%**, but average **R$308.53** in lifetime value compared with **R$160.73** for one-time customers. The gap supports a retention test focused on second-purchase conversion.

### 10. Category Basket Pairs

`bed_bath_table` and `furniture_decor` are the most frequent cross-category pair with **70 shared orders**, followed by `bed_bath_table` and `home_confort` with **43**. Pair counts are modest relative to total orders, so they are better used for targeted merchandising tests than broad bundle assumptions.

## Technical Controls

- Revenue and payment facts are analyzed separately to avoid many-to-many multiplication.
- Review rows are reduced to the latest response per order before customer-experience joins; the source contains **547 orders with multiple review rows**.
- Seller delivery and review metrics are calculated at the seller-order grain, while units and revenue retain item-level aggregation.
- Customer retention uses `customer_unique_id`, not the order-level `customer_id`.
- Load validation confirms all expected row counts and zero tested foreign-key orphans.

All exact tables are available in [`../results/`](../results/).
