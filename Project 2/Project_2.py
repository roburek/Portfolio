import pandas as pd
import numpy as np

def merge_all_data(user_health_file, supplement_usage_file, experiments_file, user_profiles_file):
    health_df = pd.read_csv(user_health_file)
    supp_df = pd.read_csv(supplement_usage_file)
    exp_df = pd.read_csv(experiments_file)
    profile_df = pd.read_csv(user_profiles_file)

    health_df['date'] = pd.to_datetime(health_df['date'], errors='coerce')
    supp_df['date'] = pd.to_datetime(supp_df['date'], errors='coerce')

    supp_df['experiment_id'] = supp_df['experiment_id'].astype(str)
    exp_df['experiment_id'] = exp_df['experiment_id'].astype(str)

    supp_df['supplement_name'] = supp_df['supplement_name'].fillna('').astype(str).str.strip()
    supp_df.loc[supp_df['supplement_name'] == '', 'supplement_name'] = 'No intake'
    supp_df['dosage_unit'] = supp_df['dosage_unit'].astype(str).str.lower().str.strip()

    supp_df['dosage_grams'] = np.where(
        supp_df['dosage_unit'] == 'mg',
        supp_df['dosage'] / 1000,
        supp_df['dosage']
    )

    supp_df['is_placebo'] = (
        supp_df['is_placebo']
        .astype(str)
        .str.strip()
        .str.lower()
        .map({'true': True, '1': True, 'yes': True,
              'false': False, '0': False, 'no': False})
        .astype('boolean')
    )

    supp_df = supp_df.merge(
        exp_df[['experiment_id', 'name']],
        on='experiment_id', how='left'
    ).rename(columns={'name': 'experiment_name'})

    merged = pd.merge(health_df, supp_df, on=['user_id', 'date'], how='outer')
    merged = pd.merge(merged, profile_df, on='user_id', how='left')

    merged['sleep_hours'] = (
        merged['sleep_hours']
        .astype(str)
        .str.replace('[^0-9\\.]', '', regex=True)
        .replace('', np.nan)
    )
    merged['sleep_hours'] = pd.to_numeric(merged['sleep_hours'], errors='coerce')

    def age_to_group(age):
        if pd.isna(age):
            return 'Unknown'
        elif age < 18: return 'Under 18'
        elif age <= 25: return '18-25'
        elif age <= 35: return '26-35'
        elif age <= 45: return '36-45'
        elif age <= 55: return '46-55'
        elif age <= 65: return '56-65'
        else: return 'Over 65'

    merged['user_age_group'] = merged['age'].apply(age_to_group)
    merged['supplement_name'] = merged['supplement_name'].fillna('No intake')

    mask = merged['supplement_name'] == 'No intake'
    merged.loc[mask, 'dosage_grams'] = np.nan
    merged.loc[mask, 'is_placebo'] = pd.NA
    merged['is_placebo'] = merged['is_placebo'].astype('boolean')  # ensure <NA> stays

    final_columns = [
        'user_id', 'date', 'email', 'user_age_group',
        'experiment_name', 'supplement_name',
        'dosage_grams', 'is_placebo',
        'average_heart_rate', 'average_glucose',
        'sleep_hours', 'activity_level'
    ]
    final_df = merged[final_columns].sort_values(['user_id', 'date']).reset_index(drop=True)
    return final_df
