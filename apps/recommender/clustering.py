import pandas as pd
from sklearn.preprocessing import LabelEncoder
from kmodes.kmodes import KModes

from apps.frameworks.services import get_all_frameworks
from apps.libraries.services import get_all_libraries
from apps.databases.services import get_all_databases


frameworks_categorical_cols = ['purpose', 'scaling_poss', 'db_integration']
libraries_categorical_cols = ['purpose']
databases_categorical_cols = ['type', 'scaling_poss', 'big_data_poss', 'acid_support']


async def create_dataframes_from_mongo():
    frameworks = await get_all_frameworks()
    libraries = await get_all_libraries()
    databases = await get_all_databases()

    frameworks_df = pd.DataFrame([f.dict() for f in frameworks])
    frameworks_df = frameworks_df[frameworks_df['purpose'].isin(['веб-приложение', 'десктопное приложение',
                                                                 'мобильное приложение'])]
    libraries_df = pd.DataFrame([lib.dict() for lib in libraries])
    databases_df = pd.DataFrame([d.dict() for d in databases])

    return frameworks_df, libraries_df, databases_df


async def encode_dataframe(df, columns):
    encoders = {}
    df = df.copy()

    for column in columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        encoders[column] = le

    return df, encoders


async def create_encoded_dataframes(frameworks_df, libraries_df, databases_df):
    frameworks_df_encoded, frameworks_encoders = await encode_dataframe(frameworks_df.copy(),
                                                                        frameworks_categorical_cols)
    libraries_df_encoded, libraries_encoders = await encode_dataframe(libraries_df.copy(), libraries_categorical_cols)
    databases_df_encoded, databases_encoders = await encode_dataframe(databases_df.copy(), databases_categorical_cols)

    return frameworks_df_encoded, frameworks_encoders, libraries_df_encoded, libraries_encoders, \
        databases_df_encoded, databases_encoders


async def cluster_data(df_encoded, n_clusters, init='Cao', n_init=5, verbose=0):
    km = KModes(n_clusters=n_clusters, init=init, n_init=n_init, verbose=verbose)
    clusters = km.fit_predict(df_encoded)
    df_encoded['cluster'] = clusters
    return km, df_encoded


async def get_clustering_results():
    n_clusters_frameworks, n_clusters_libraries, n_clusters_databases = 4, 4, 4
    frameworks_df, libraries_df, databases_df = await create_dataframes_from_mongo()
    frameworks_df_encoded, frameworks_encoders, libraries_df_encoded, \
        libraries_encoders, databases_df_encoded, databases_encoders = await create_encoded_dataframes(frameworks_df,
                                                                                                       libraries_df,
                                                                                                       databases_df)

    frameworks_km, frameworks_df_clustered = await cluster_data(
        frameworks_df_encoded[frameworks_categorical_cols].copy(),
        n_clusters_frameworks)
    frameworks_df['cluster'] = frameworks_df_clustered['cluster']

    libraries_km, libraries_df_clustered = await cluster_data(libraries_df_encoded[libraries_categorical_cols].copy(),
                                                              n_clusters_libraries)
    libraries_df['cluster'] = libraries_df_clustered['cluster']

    databases_km, databases_df_clustered = await cluster_data(databases_df_encoded[databases_categorical_cols].copy(),
                                                              n_clusters_databases)
    databases_df['cluster'] = databases_df_clustered['cluster']

    return frameworks_df, libraries_df, databases_df, frameworks_encoders, libraries_encoders, \
        databases_encoders, frameworks_km, libraries_km, databases_km
