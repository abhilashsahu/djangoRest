""" Utility function to load csv records into DB using Django models

usage: load_csv_into_db.py [-h] -file_path FILE_PATH -model MODEL

<TODO: This is not the conventional way to write the import script
    but due to time limit>
"""

import datetime
import argparse
import os, sys
import pandas as pd
import numpy as np

from django.db import transaction

# Below code snippet sets the context to this Django Project
proj_path = "../TestProject"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TestProject.settings")
sys.path.append(proj_path)

os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from test_app.models import Project, WTG


def get_cmd_line_args():
    """ Function to extract command line user input using argparse module

        :return: The argparse object containing user passed command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-file_path', type=str, required=True,
                        help='File path(full path) to the data source')
    parser.add_argument('-model', type=str, required=True,
                        help='Django model name against which the records are to be imported')

    return parser.parse_args()


def get_records_from_csv(file_path):
    """ Function to get records from csv

        :param file_path: A string containing the file path of the csv
        :return: List of dictionary records from the csv
    """
    df = pd.read_csv(file_path)
    data = df.replace(np.nan, None)
    return data.to_dict('records')


def format_date_columns(record):
    """ Function to format the csv date columns to django standard DateField"""
    date_columns = ['acquisition_date', 'COD']

    for date_column in date_columns:
        try:
            if date_column in record:
                record[date_column] = datetime.datetime.strptime(record[date_column], "%d/%m/%Y").strftime("%Y-%m-%d")
        except:
            record[date_column] = None


def process_db_import(table_name, records):
    """ Function to process the user request and redirects the control to appropriate
            db model

        :param table_name: A string containing name of the model to be imported
        :param records: A list of dictionaries containing the db records to be imported
    """
    if table_name.lower() == "project":
        import_projects(records)
    elif table_name.lower() == "wtg":
        import_wtgs(records)
    else:
        print(f"Error!! The request db model '{table_name}' "
              f"doesn't support csv import yet")


def import_wtgs(records):
    """ Function to iterate over the records from the CSV and insert the data into WTG Table

        :param records: A list of dictionaries containing Wind Turbine Generators
    """

    with transaction.atomic(): # Makes sure the transaction is atomic
        for record in records:
            format_date_columns(record)
            # Get the project id and remove from dict to avoid duplicate writing of project_ids
            project_id = record.pop('project_id')
            project = Project.objects.get(id=project_id)

            print(f"Processing WTG: '{record['WTG_number']}'")
            db_obj = WTG(project_id=project, **record)
            db_obj.save()
            print(f"Added WTG '{record['WTG_number']}' to DB")
            print("------------------------------------------------")


def import_projects(records):
    """ Function to iterate over the records from the CSV and insert the data into Project Table

        :param records: A list of dictionaries containing Projects
    """
    with transaction.atomic():
        for record in records:
            format_date_columns(record)

            print(f"Processing project: '{record['project_name']}'")
            db_obj = Project(**record)
            db_obj.save()
            print(f"Added project '{record['project_name']}' to DB")
            print("------------------------------------------------")


if __name__ == '__main__':
    user_input = get_cmd_line_args()
    csv_records = get_records_from_csv(user_input.file_path)
    process_db_import(user_input.model, csv_records)
