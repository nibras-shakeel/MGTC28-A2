import pandas as pd
import streamlit as st
import sqlite3
import sqlalchemy

def get_employee_dataframe():
    """Fetches employee data along with salary and country information 
    from the database and returns it as a dataframe."""
    db_connection = sqlite3.connect('./db/utsc-exercise.db')
    employee_salary_df = pd.read_sql("""SELECT e.*, s.YearlyCompensation, cm.Country, 
                                        e.FirstName || ' ' || e.LastName as FullName
                                        FROM Employee e 
                                        LEFT JOIN Salary s ON e.EmployeeId = s.EmployeeId
                                        LEFT JOIN OfficeCountryMapping cm ON cm.OfficeId = e.OfficeId""", db_connection)
    db_connection.close()
    return employee_salary_df

def get_num_employees():
    """Fetches the total number of unique employees in the Employee table."""
    db_engine = sqlalchemy.create_engine(f"sqlite:///db/utsc-exercise.db")
    with db_engine.connect() as connection:
        # Execute the distinct count query
        result = connection.execute(sqlalchemy.text("SELECT COUNT(DISTINCT EmployeeId) FROM Employee"))
        return result.scalar()

def get_avg_salary_by_job_title(employee_salary_df: pd.DataFrame, selected_titles: list):
    """Creates the multi-select filter widget to select job titles, and 
    creates the graph that displays average salary by job title."""
    # Filter the dataframe based on selected job titles
    filtered_df = employee_salary_df[employee_salary_df['JobTitle'].isin(selected_titles)]

    # Group by JobTitle and calculate the average salary
    avg_salary_by_job_title = filtered_df.groupby('JobTitle')['YearlyCompensation'].mean().reset_index()
    
    # Plot the graph
    st.subheader("Average Salary by Job Title")
    st.bar_chart(avg_salary_by_job_title, x='JobTitle', y='YearlyCompensation')

# TODO: MAKE THIS USING THE MODEL FUNCTION ABOVE (Copy-pasting is your friend here)
# HINT: The country column in the dataframe is 'Country'
def get_avg_salary_by_country(employee_salary_df: pd.DataFrame, selected_countries: list):
    """Displays the average salary by country."""
    # Filter the dataframe based on selected countries
    filtered_df = employee_salary_df[employee_salary_df['Country'].isin(selected_countries)]
    
    # Group by Country and calculate the average salary
    avg_salary_by_country = filtered_df.groupby('Country')['YearlyCompensation'].mean().reset_index()
    
    # Plot the graph
    st.subheader("Average Salary by Country")
    st.bar_chart(avg_salary_by_country, x='Country', y='YearlyCompensation')

# TODO: MAKE THIS USING THE MODEL FUNCTION ABOVE (Copy-pasting is your friend here)
def get_num_employees_by_country(employee_salary_df: pd.DataFrame, selected_countries: list):
    """Displays the number of employees by country."""
    # Filter the dataframe based on selected countries
    filtered_df = employee_salary_df[employee_salary_df['Country'].isin(selected_countries)]
    
    # Group by Country and count the number of employees
    employees_by_country = filtered_df.groupby('Country').size().reset_index(name='Count')
    
    # Plot the graph
    st.subheader("Number of Employees by Country")
    st.bar_chart(employees_by_country, x='Country', y='Count')

# TODO: MAKE THIS USING THE MODEL FUNCTION ABOVE (Copy-pasting is your friend here)
def get_num_employees_by_job_title(employee_salary_df: pd.DataFrame, selected_titles: list):
    """Displays the number of employees by job title."""
    # Filter the dataframe based on selected job titles
    filtered_df = employee_salary_df[employee_salary_df['JobTitle'].isin(selected_titles)]
    
    # Group by JobTitle and count the number of employees
    employees_by_job_title = filtered_df.groupby('JobTitle').size().reset_index(name='Count')
    
    # Plot the graph
    st.subheader("Number of Employees by Job Title")
    st.bar_chart(employees_by_job_title, x='JobTitle', y='Count')

if __name__ == '__main__':
    # Streamlit app title
    st.title('Employee Salary Analysis')

    # Fetch and display the total number of employees
    num_employees = get_num_employees()
    st.write(f"Total number of employees = {num_employees}")

    # Fetch the employee data
    employee_salary_df = get_employee_dataframe()

    # Get unique job titles from the dataframe and make a multiselect filter for them
    job_titles = employee_salary_df['JobTitle'].unique()
    selected_titles = st.multiselect('Select Job Title', job_titles, default=job_titles)
    
    # Avg salary by job title graph
    get_avg_salary_by_job_title(employee_salary_df, selected_titles)
    
    # Number of employees by job title graph
    get_num_employees_by_job_title(employee_salary_df, selected_titles)

    # Get unique countries from the dataframe and make a multiselect filter for them
    countries = employee_salary_df['Country'].unique()
    selected_countries = st.multiselect('Select Countries', countries, default=countries)
    
    # Avg salary by country graph
    get_avg_salary_by_country(employee_salary_df, selected_countries)
    
    # Number of employees by country graph
    get_num_employees_by_country(employee_salary_df, selected_countries)
