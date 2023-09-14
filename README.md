# RFM Customer Segmentation with K-Means Clustering
This customer segmentation project employs the RFM (Recency, Frequency, Monetary) analysis in conjunction with K-Means clustering. This approach enables the categorization of customers based on their transactional behavior and helps in identifying distinct customer segments for targeted marketing strategies.

## Methodology
- Data Preprocessing

- RFM Analysis:
1. Recency (R): Measures how recently a customer made a purchase. It is calculated based on the latest transaction date.
2.  Frequency (F): Indicates how often a customer makes purchases. It is derived from the total number of transactions.
3.  Monetary (M): Reflects the total monetary value spent by a customer. It is determined by summing up the transactional values.

- RFM Score Calculation:
Each customer is assigned an RFM score, combining Recency, Frequency, and Monetary values. Higher scores indicate customers to focus.

- K-Means Clustering:
Utilizes the RFM scores as features to perform K-Means clustering. This groups customers into distinct segments based on their similarities in transactional behavior.

- Interpretation of Clusters:
Each cluster represents a unique customer segment with specific characteristics. Understanding these segments helps tailor marketing strategies.

## Story of Dataset
The dataset named Online Retail II contains the online sales transactions of a UK-based retail company between 01/12/2009-09/12/2011. The company's product catalog includes gift items and it is known that most of its customers are wholesalers.

## About Dataset
- *InvoiceNo:* Invoice Number (If this code starts with C, it indicates that the transaction has been canceled)
- *StockCode:* Product Code (Unique for each product)
- *Description:* Product Name
- *Quantity:* Quantity of the product (How many of the products on the invoices were sold)
- *InvoiceDate:* Invoice Date
- *UnitPrice:* Unit Price in Pounds
- *CustomerID:* Unique Customer ID
- *Country:* Country Name
