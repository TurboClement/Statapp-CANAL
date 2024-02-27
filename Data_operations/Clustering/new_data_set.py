import sys
sys.path.append("Data_operations")

from Tool_Functions.cleaning_data import *
from Tool_Functions.comportment_reabo import * 
from Tool_Functions.join_data import * 



def create_new_data_set_n_reabos(data_path, data_path_results):
    """
    Creates a new dataset 'new_data_set' from 'df_Données_Reabos_odd' dataframe where the columns are the 
    TYPE_PROMON
    """

    # Load 'df_Données_Reabos_odd' dataframe
    df_Données_Reabos_odd = file_to_dataframe(data_path + "df_Données_Reabos_odd.csv")

    # Perform statistical analysis on 'df_Données_Reabos_odd' dataframe
    df = count_abo_conditions(df_Données_Reabos_odd, ['ID_ABONNE', 'TYPE_PROMON'], 'DATE_ACTE_REEL')

    # Create a pivot table from 'df' dataframe we exchange the lines and columns
    new_data_set = df.pivot_table(index='ID_ABONNE', columns='TYPE_PROMON', values='NB_DATE_ACTE_REEL')

    # Reset index of the pivot table
    new_data_set = new_data_set.reset_index()

    # Replace NaN values with 0
    new_data_set.fillna(0, inplace=True)

    # Convert floating-point values to integers
    new_data_set = new_data_set.astype(int)

    # Save 'new_data_set' dataframe to a CSV file
    save_to_csv_file(new_data_set, data_path_results + "df_n_reabos_ODD.csv")

    return True




def create_new_data_set_delai_reabo(data_path, data_path_results):
    """
    Creates a new dataset 'new_data_set' from 'df_Données_Reabos_odd' dataframe where the columns are the 
    TYPE_PROMON
    """

    # Load 'df_Données_Reabos_odd' dataframe
    df_Données_Reabos_odd = file_to_dataframe(data_path + "df_Données_Reabos_odd.csv")

    # Perform statistical analysis on 'df_Données_Reabos_odd' dataframe
    df = mean_time_reabo(df_Données_Reabos_odd, ['ID_ABONNE','TYPE_PROMON'], 'DELAI_REABO')

    # Create a pivot table from 'df' dataframe we exchange the lines and columns
    new_data_set = df.pivot_table(index='ID_ABONNE', columns='TYPE_PROMON', values='MEAN_DELAI_REABO')

    # Reset index of the pivot table
    new_data_set = new_data_set.reset_index()

    # Replace NaN values with 0
    new_data_set.fillna(math.inf, inplace=True)

    # Convert floating-point values to integers
    new_data_set = new_data_set.astype(float)

    # Save 'new_data_set' dataframe to a CSV file
    save_to_csv_file(new_data_set, data_path_results + "df_n_reabos_mean_time_ODD.csv")

    return True

def create_new_data_set(data_path, data_path_results):
    """
    Creates a new dataset 'new_data_set' from 'df_Données_Reabos_odd' dataframe where the columns are the 
    TYPE_PROMON
    """

    # Load 'df_Données_Reabos_odd' dataframe
    df_Données_Reabos_odd = file_to_dataframe(data_path + "df_Données_Reabos_odd.csv")

    # Create df_n_reabos_ODD
    df_n_reabos_ODD = count_abo_conditions(df_Données_Reabos_odd, ['ID_ABONNE', 'TYPE_PROMON'], 'DATE_ACTE_REEL')
    df_n_reabos_ODD = df_n_reabos_ODD.pivot_table(index='ID_ABONNE', columns='TYPE_PROMON', values='NB_DATE_ACTE_REEL')
    df_n_reabos_ODD = df_n_reabos_ODD.reset_index()
    df_n_reabos_ODD.fillna(0, inplace=True)
    df_n_reabos_ODD = df_n_reabos_ODD.astype(int)
    new_column_names = {col: col + '_n_REABOS' if col != 'ID_ABONNE' else col for col in df_n_reabos_ODD.columns}
    df_n_reabos_ODD = df_n_reabos_ODD.rename(columns=new_column_names)


    # Create df_n_reabos_mean_time_ODD
    df_n_reabos_mean_time_ODD = mean_time_reabo(df_Données_Reabos_odd, ['ID_ABONNE','TYPE_PROMON'], 'DELAI_REABO')
    df_n_reabos_mean_time_ODD = df_n_reabos_mean_time_ODD.pivot_table(index='ID_ABONNE', columns='TYPE_PROMON', values='MEAN_DELAI_REABO')
    df_n_reabos_mean_time_ODD = df_n_reabos_mean_time_ODD.reset_index()
    df_n_reabos_mean_time_ODD.fillna(math.inf, inplace=True)
    df_n_reabos_mean_time_ODD = df_n_reabos_mean_time_ODD.astype(float)
    new_column_names = {col: col + '_MEAN_TIME' if col != 'ID_ABONNE' else col for col in df_n_reabos_mean_time_ODD.columns}
    df_n_reabos_mean_time_ODD = df_n_reabos_mean_time_ODD.rename(columns=new_column_names)

    # Join df_n_reabos_mean_time_ODD df_n_reabos_ODD
    df = join_dataFrames(df_n_reabos_ODD,df_n_reabos_mean_time_ODD,"ID_ABONNE")

    # Save 'new_data_set' dataframe to a CSV file
    save_to_csv_file(df, data_path_results + "new_datas.csv")

    return True