from langchain_core.tools import tool

@tool
def make_plots(variables, variables_store):
    """
        Plot multiple figures for each variable on the input list.
        Variables on the same sublist will be plotted on the same figure.
        
        Args:
            variables: list of lists containing the variable name for each subplot
    """

    for i in range(len(variables)):
        sub_var = variables[i]
        for j in range(len(sub_var)):
            query = f"""
                SELECT * FROM embedding_metadata
                WHERE key = 'signal_name'
                AND string_value = '{sub_var[j]}'
                COLLATE NOCASE
            """
            
            sql_cursor = variables_store.get_sql_cursor()
            res = sql_cursor.execute(query)
            if(not res.fetchall()):
                matches = variables_store.vector_store.similarity_search(
                    sub_var[j],
                    k=1)
                var_name = matches[0].metadata['signal_name']
                variables[i][j] = var_name
        variables_store.close_sql_con()
    return variables