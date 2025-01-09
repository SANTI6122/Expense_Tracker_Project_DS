      
        
def fetch_data(query):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="EXPENSES"
    )
    data = pd.read_sql(query, connection)
    connection.close()
    return data


st.title("Expense Tracker Dashboard")

#All Expenses
st.header("All Expenses")
query = "SELECT * FROM expense ORDER BY Date asc;"
total_spent = fetch_data(query)
st.dataframe(total_spent)


# Display total spending
query = "SELECT SUM(round(amount_paid)) AS total_spent FROM expense;"
total_spent = fetch_data(query)
st.metric("Total Spending", f"${total_spent['total_spent'][0]:,.2f}")

# Display Monthly Spending
st.header("Monthly Spending")
query = "SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(round(amount_paid)) AS total_spent FROM expense GROUP BY month ORDER BY month;"
monthly_spent = fetch_data(query)
st.line_chart(monthly_spent.set_index('month')['total_spent'])

#Spending By Category
st.header("Spending by Category")
query = "SELECT category, SUM(round(amount_paid)) AS total_spent FROM expense GROUP BY category ORDER BY total_spent DESC;"
category = fetch_data(query)
# Bar Chart
st.bar_chart(category.set_index('category')['total_spent'])

#Spending by Payment Mode
st.header("Spending by Payment Mode")
query = "SELECT payment_mode, SUM(round(amount_paid)) AS total_spent FROM expense GROUP BY payment_mode ORDER BY total_spent DESC;"
payment_mode = fetch_data(query)
#st.bar_chart(payment_mode)
# Pie Chart with Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    payment_mode['total_spent'], 
    labels=payment_mode['payment_mode'], 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=plt.cm.Paired.colors
)
ax.set_title('Spending Proportion by Payment Mode', fontsize=16)
st.pyplot(fig)  # Use st.pyplot to render the figure in Streamlit


#Category-Wise cashback
st.header("Category-Wise Cashback")
query = "SELECT category, SUM(cashback) AS total_cashback FROM expense GROUP BY category ORDER BY total_cashback DESC;"
category_cashback = fetch_data(query)
# Plotting the data
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(category_cashback['category'], category_cashback['total_cashback'], color='orange')
ax.set_title('Total Cashback by Category', fontsize=16)
ax.set_xlabel('Total Cashback', fontsize=12)
ax.set_ylabel('Category', fontsize=12)
ax.invert_yaxis()  # Highest cashback on top
plt.tight_layout()
# Render the plot in Streamlit
st.pyplot(fig)

#Transaction Per Category
st.header("Number of Transactions Per Category")
query = "SELECT category, COUNT(*) AS transaction_count FROM expense GROUP BY category ORDER BY transaction_count DESC;"
category_trans = fetch_data(query)
# Scatter Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(category_trans['category'], category_trans['transaction_count'], color='blue', alpha=0.7)
ax.set_title('Transaction Count by Category', fontsize=16)
ax.set_xlabel('Category', fontsize=12)
ax.set_ylabel('Transaction Count', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
plt.tight_layout()
# Render in Streamlit
st.pyplot(fig)

#Percentage of Spending by Category
st.header("Percentage of Spending by Category")
query = "SELECT category, SUM(round(amount_paid)) AS total_spent,round(SUM(round(amount_paid)) / (SELECT SUM(round(amount_paid)) FROM expense) * 100) AS percentage_spent FROM expense GROUP BY category ORDER BY percentage_spent DESC;"
category_percent = fetch_data(query)
#st.bar_chart(category_percent)
# Donut Chart
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    category_percent['percentage_spent'], 
    labels=category_percent['category'], 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=plt.cm.tab20.colors
)
# Adding a white center circle for the donut effect
center_circle = plt.Circle((0, 0), 0.70, fc='white')
ax.add_artist(center_circle)
ax.set_title('Spending by Category (Donut Chart)', fontsize=16)
plt.tight_layout()
# Render the figure in Streamlit
st.pyplot(fig)

#Average Monthly Spending
st.header("Average Monthly Spending")
query = "SELECT DATE_FORMAT(date, '%Y-%m') AS month, round(AVG(amount_paid)) AS avg_monthly_spent FROM expense GROUP BY month ORDER BY month;"
avg_monthy_spending = fetch_data(query)
# Area Chart
st.area_chart(avg_monthy_spending.set_index('month')['avg_monthly_spent'])


#Spending by Day 
st.header("Spending by Day of the Week")
query = "SELECT DAYNAME(date) AS day_of_week, SUM(round(amount_paid)) AS total_spent FROM expense GROUP BY day_of_week ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');"
daywise_data = fetch_data(query)
st.line_chart(daywise_data.set_index('day_of_week')['total_spent'])


#Payment Mode-wise Cashback
st.header("Payment Mode-Wise Cashback")
query = "SELECT payment_mode, round(SUM(cashback)) AS total_cashback FROM expense GROUP BY payment_mode ORDER BY total_cashback DESC;"
payment_cashback = fetch_data(query)
# Plotting the data
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(payment_cashback['payment_mode'], payment_cashback['total_cashback'], color='orange')
ax.set_title('Total Cashback by Payment Mode', fontsize=16)
ax.set_xlabel('Total Cashback', fontsize=12)
ax.set_ylabel('Payment Mode', fontsize=12)
ax.invert_yaxis()  # Highest cashback on top
plt.tight_layout()
# Render the plot in Streamlit
st.pyplot(fig)


#Spending Distribution by range
st.header("Spending Distribution by Range")
query = "SELECT round(SUM(CASE WHEN category = 'Investments' THEN amount_paid ELSE 0 END)) AS total_investments,round(SUM(CASE WHEN category != 'Investments' THEN amount_paid ELSE 0 END)) AS total_other_spent FROM expense;"
spending_data = fetch_data(query)
# Prepare Data for Pie Chart
labels = ['Investments', 'Other Spending']
values = [spending_data['total_investments'][0], spending_data['total_other_spent'][0]]
# Plot Pie Chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#1f77b4', '#ff7f0e'])
ax.set_title('Spending Breakdown', fontsize=16)
# Render the pie chart in Streamlit
st.pyplot(fig)




#Daily Spending Trend
st.header("Daily Spending Trend")
query = "SELECT date, SUM(amount_paid) AS daily_spent FROM expense GROUP BY date ORDER BY date;"
daily_data = fetch_data(query)
# Vertical Bar Chart
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(daily_data['date'], daily_data['daily_spent'], color='skyblue')
ax.set_title('Daily Spending Trend', fontsize=16)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Daily Spending', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
# Render the bar chart in Streamlit
st.pyplot(fig)

