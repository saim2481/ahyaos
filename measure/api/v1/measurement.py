# # from fastapi import APIRouter, Depends
# # from measure.services.measure_service import perform_measurement
# # from auth.api.v1.auth import oauth2_scheme, verify_token

# # router = APIRouter()

# # @router.get("/measurements")
# # def get_measurement():
# #     return perform_measurement()

# # @router.get("/secure_measurements")
# # def get_secure_measurement(token: str = Depends(oauth2_scheme)):
# #     verify_token(token)
# #     return perform_measurement()


# from fastapi import APIRouter, Depends, HTTPException, status
# from auth.api.v1.auth import verify_token

# router = APIRouter()

# @router.get("/calculate", response_model=dict)
# async def calculate_with_auth(token: str = Depends(verify_token)):
#     # Your calculation logic here
#     return {"result": "calculation result with auth"}

# @router.get("/public-calculate", response_model=dict)
# async def calculate_without_auth():
#     # Your calculation logic here
#     return {"result": "calculation result without auth"}


import traceback
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
# from auth.api.v1.auth import verify_token
from sqlalchemy import select
from sqlalchemy.orm import Session
from measure.db.models import FactorUnit, StripeFeature, StripePackage
from measure.dependencies import get_async_db, get_db
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from measure.schemas import schemas
from measure.services.measure_service import initialize_models, embed_text, compute_cosine_similarity, clean_text, get_recommendations, prepare_final_output, preprocess_text, remove_source_words, update_text
import pickle
import os
import stripe
import httpx
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

stripe.api_key = "sk_test_51POKYm2MPf6Tg7eRlc19aKXQHKkYMABseM3ZovvX7WAEloOby8uBPnjw7v97gKtxqqMdjGaVigBwD3BmtSkownCP00bpdPnLtN"
stripe.api_version = "2024-06-20"
# @router.get("/search/", response_model=list)
# def calculat_with_auth(footprint_description:str):
#     # Initialize the models
#     model_dict = {
#         'model_1': 'all-mpnet-base-v2',
#         'model_2': 'all-MiniLM-L6-v2',
#         'model_3': 'all-distilroberta-v1',
#         'model_4': 'all-MiniLM-L12-v2'
#     }

#     # Initialize the models
#     models = initialize_models(model_dict)

#     # Load pickle files from the local directory with error handling
#     pickle_file_path = r'measure\content\dataframes.pkl'
#     try:
#         with open(pickle_file_path, 'rb') as f:
#             df, df_unique_activity_vector = pickle.load(f)
#     except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError) as e:
#         print(f"Error loading the pickle file: {e}")
#         df, df_unique_activity_vector = None, None

#     # # If the DataFrames were loaded successfully, save them as CSV files
#     # if df is not None and df_unique_activity_vector is not None:
        
#     #     df.to_csv(r'measure\content\dataframe.csv', index=False)
#     #     df_unique_activity_vector.to_csv(r'measure\content\df_unique_activity_vector.csv', index=False)
#     #     print("DataFrames successfully saved as CSV files.")
#     # else:
#     #     print("Failed to load DataFrames from the pickle file.")
#     # df = pd.read_csv(r'measure\content\dataframe.csv')
#     # df_unique_activity_vector = pd.read_csv(r'measure\content\df_unique_activity_vector.csv')
#     # Clean the input description
#     remove_keyword = []
#     footprint_description_processed = clean_text(footprint_description, remove_keyword)


#     # Generate embeddings for the cleaned description
#     search_vectors = {name: embed_text(footprint_description_processed, model) for name, model in models.items()}
#     recommendation = get_recommendations(df, df_unique_activity_vector, search_vectors, footprint_description, footprint_description_processed, model_dict, top_n_per_model=50, top_shortlist=20)

#     final_output = prepare_final_output(recommendation)
#     print(final_output)
#     return final_output.to_dict(orient="records")


@router.get("/search/", response_model=List)
async def calculat_with_auth(
    footprint_description:str,
    grouped:bool=Query(False,description="return data to be grouped or not"),
    Exclude_words:list=Query([],description="list of excluded words"),
    Country_filter:list=Query([],description="list of country filters"),
    Year_filter:list=Query([],description="list of year filters"),
    Unit_filter:list=Query([],description="list of unit filters")
    
    ):
    # Initialize the models
    Year_filter = [int(year) for year in Year_filter]
   # Initialize the models
    model_dict = {
        'model_1': 'all-mpnet-base-v2',
        'model_2': 'all-MiniLM-L6-v2',
        'model_3': 'all-distilroberta-v1',
        'model_4': 'all-MiniLM-L12-v2'
    }

    # Initialize the models
    models = initialize_models(model_dict)


    ## Climatiq DB Embeddings
    Regenerate = False

    if Regenerate==True:
        # Load Climatiq data
        activitymapping = pd.read_csv('climatiq_data2.csv')
        activitymapping['country'] = activitymapping['region'].apply(lambda x: x.split('-')[0] if isinstance(x, str) else '')
        activitymapping = activitymapping[['activity_id','id','sector','category', 'unit_type', 'country','year','source_dataset', 'factor']]
        activitymapping['activity_name'] = activitymapping.activity_id + ' ' + activitymapping.sector +  ' '  + activitymapping.category


        remove_words = ['type']
        activitymapping['processed_sector'] = activitymapping['sector'].apply(lambda x: preprocess_text(x, remove_words))
        activitymapping['processed_sector'] = activitymapping.apply(lambda x: ('sector is ' + x.processed_sector + '. ') if pd.notna(x.processed_sector) and x.processed_sector !='' else '', axis=1)

        activitymapping['processed_category_og'] = activitymapping['category'].apply(lambda x: preprocess_text(x, remove_words))
        #activitymapping['processed_category'] = activitymapping.apply(lambda x: ('emission category is ' + x.processed_category_og + '') if pd.notna(x.processed_category_og) and x.processed_category_og!='' else '', axis=1)
        activitymapping['processed_category'] = activitymapping.apply(lambda x: ('category is ' + x.processed_category_og + '') if pd.notna(x.processed_category_og) and x.processed_category_og!='' else '', axis=1)

        activitymapping['processed_activity_id_og'] = activitymapping['activity_id'].apply(lambda x: preprocess_text(x, remove_words))
        activitymapping['processed_activity_id_og'] = activitymapping.apply(remove_source_words, axis=1)
        activitymapping['processed_activity_id'] = activitymapping.apply(lambda x: (' and subcategory is ' + x.processed_activity_id_og + '. ') if pd.notna(x.processed_activity_id_og) and x.processed_activity_id_og!='' else '.', axis=1)

        #activitymapping['processed_activity_name'] = activitymapping['processed_activity_name'].apply(lambda x: 'emissions from ' + x)
        #activitymapping['processed_activity_name'] = activitymapping.apply(lambda x:  x.processed_sector + x.processed_category + x.processed_activity_id, axis=1)
        activitymapping['processed_activity_name'] = activitymapping.apply(lambda x:  x.processed_category + x.processed_activity_id, axis=1)

        # exclude other activites from same category
        activitymapping['processed_activity_name_detailed'] = activitymapping.apply(lambda x: update_text(x, df), axis=1)

        activitymapping_unique_activity_vector= activitymapping.drop_duplicates(subset=['processed_activity_name'])
        print(len(activitymapping_unique_activity_vector))
        print(len(activitymapping))

        activitymapping_unique_activity_vector['activity_name_vector_model_1'] = activitymapping_unique_activity_vector['processed_activity_name'].apply(lambda x: embed_text(x, model = models['model_1']))
        activitymapping_unique_activity_vector['activity_name_vector_model_2'] = activitymapping_unique_activity_vector['processed_activity_name'].apply(lambda x: embed_text(x, model = models['model_2']))
        activitymapping_unique_activity_vector['activity_name_vector_model_3'] = activitymapping_unique_activity_vector['processed_activity_name'].apply(lambda x: embed_text(x, model = models['model_3']))
        activitymapping_unique_activity_vector['activity_name_vector_model_4'] = activitymapping_unique_activity_vector['processed_activity_name'].apply(lambda x: embed_text(x, model = models['model_4']))

        df = activitymapping
        df_unique_activity_vector = activitymapping_unique_activity_vector
        with open('dataframes_v2.pkl', 'wb') as f:
            pickle.dump((df, df_unique_activity_vector), f)
    else:
        pickle_file_path = r'measure\content\dataframes.pkl'

    with open(pickle_file_path, 'rb') as f:
        df, df_unique_activity_vector = pickle.load(f)


    if False:
        activitymapping_unique_activity_vector_1 = activitymapping_unique_activity_vector[['activity_id','id','processed_activity_name','activity_name_vector_model_1','activity_name_vector_model_2','activity_name_vector_model_3','activity_name_vector_model_4']]
        df_unique_activity_vector_1 = df_unique_activity_vector[['activity_id','id','processed_activity_name','activity_name_vector_model_1','activity_name_vector_model_2','activity_name_vector_model_3','activity_name_vector_model_4']]
        are_identical = df_unique_activity_vector_1.equals(activitymapping_unique_activity_vector_1)
        are_identical


    # Load pickle files from the local directory with error handling
    # pickle_file_path = r'measure\content\dataframes.pkl'
    # try:
    #     with open(pickle_file_path, 'rb') as f:
    #         df, df_unique_activity_vector = pickle.load(f)
    # except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError) as e:
    #     print(f"Error loading the pickle file: {e}")
    #     df, df_unique_activity_vector = None, None

    # # If the DataFrames were loaded successfully, save them as CSV files
    # if df is not None and df_unique_activity_vector is not None:
        
    #     df.to_csv(r'measure\content\dataframe.csv', index=False)
    #     df_unique_activity_vector.to_csv(r'measure\content\df_unique_activity_vector.csv', index=False)
    #     print("DataFrames successfully saved as CSV files.")
    # else:
    #     print("Failed to load DataFrames from the pickle file.")
    # df = pd.read_csv(r'measure\content\dataframe.csv')
    # df_unique_activity_vector = pd.read_csv(r'measure\content\df_unique_activity_vector.csv')
    # Clean the input description
    # remove_keyword = []
    # Unit_filter = ['WeightOverDistance']
    # Warning if filters are outside list
    unique_country = df['country'].unique()
    unique_year = df['year'].unique()
    unique_units = df['unit_type'].unique()

    missing_values = [item for item in Country_filter if item not in unique_country]
    if missing_values:
        print(f"Error: The following countries are missing: {missing_values}")

    missing_values = [item for item in Year_filter if item not in unique_year]
    if missing_values:
        print(f"Error: The following years are missing: {missing_values}")

    missing_values = [item for item in Unit_filter if item not in unique_units]
    if missing_values:
        print(f"Error: The following years are missing: {missing_values}")

    df_unique_activity_vector_filtered = df_unique_activity_vector
    df_filtered = df
    print(len(df_filtered))

    if len(Exclude_words) > 0:
        for keyword in Exclude_words:
            df_filtered = df_filtered[~(df_filtered['activity_id'].str.contains(keyword))]
            print(len(df_filtered))

    if len(Country_filter) > 0:
        df_filtered = df_filtered[df_filtered['country'].isin(Country_filter)]
        print(len(df_filtered))


    if len(Year_filter) > 0:
        df_filtered = df_filtered[df_filtered['year'].isin(Year_filter)]
        print(len(df_filtered))

    if len(Unit_filter) > 0:
        df_filtered = df_filtered[df_filtered['unit_type'].isin(Unit_filter)]
        print(len(df_filtered))

    print(len(df_unique_activity_vector_filtered))

    df_unique_activity_vector_filtered = df_unique_activity_vector_filtered[df_unique_activity_vector_filtered['processed_activity_name'].isin(df_filtered['processed_activity_name'].unique())]
    print(len(df_unique_activity_vector_filtered))



    # df_unique_activity_vector_filtered = df_unique_activity_vector
    # df_filtered = df
    # print(len(df_filtered))

    # if len(Exclude_words) > 0:
    #     for keyword in Exclude_words:
    #         df_filtered = df_filtered[~(df_filtered['activity_id'].str.contains(keyword))]
    #         print(len(df_filtered))

    # if len(Country_filter) > 0:
    #     df_filtered = df_filtered[df_filtered['country'].isin(Country_filter)]
    #     print(len(df_filtered))


    # if len(Year_filter) > 0:
    #     df_filtered = df_filtered[df_filtered['year'].isin(Year_filter)]
    #     print(len(df_filtered))

    # if len(Unit_filter) > 0:
    #     df_filtered = df_filtered[df_filtered['unit_type'].isin(Unit_filter)]
    #     print(len(df_filtered))

    # print(len(df_unique_activity_vector_filtered))

    # df_unique_activity_vector_filtered = df_unique_activity_vector_filtered[df_unique_activity_vector_filtered['processed_activity_name'].isin(df_filtered['processed_activity_name'].unique())]
    # print(len(df_unique_activity_vector_filtered))
        
    # # Clean the input description
    # remove_keyword = []
    # footprint_description_processed = clean_text(footprint_description, remove_keyword)


    # # Generate embeddings for the cleaned description
    # search_vectors = {name: embed_text(footprint_description_processed, model) for name, model in models.items()}
    # recommendation = get_recommendations(df_filtered, df_unique_activity_vector_filtered, search_vectors, footprint_description, footprint_description_processed, model_dict, top_n_per_model=50, top_shortlist=20)
    # print(recommendation)
    # final_output = prepare_final_output(recommendation)
    
    # return final_output.to_dict(orient="records")
    # Clean the input description
    remove_keyword = []
    footprint_description_processed = clean_text(footprint_description, remove_keyword)


    # Generate embeddings for the cleaned description
    search_vectors = {name: embed_text(footprint_description_processed, model) for name, model in models.items()}
    recommendation = get_recommendations(df_filtered, df_unique_activity_vector_filtered, search_vectors, footprint_description, footprint_description_processed, model_dict, top_n_per_model=50, top_shortlist=20)

    final_output = prepare_final_output(recommendation)
    if len(final_output.columns) == 0:
       return final_output.to_dict(orient="records")
    final_output_display = final_output[final_output['rank'] <= 25]

    if grouped ==False:
        final_output_display = final_output_display.sort_values(by=['rank'], ascending=[True])
        final_output_display = final_output_display[['footprint','activity_id', 'unit_type', 'country', 'year', 'id','rank']]
        final_output_display.reset_index(drop=True, inplace=True)
        final_output_display
        return final_output_display.to_dict(orient="records")


    final_output_display_grouped = final_output_display.groupby(['footprint', 'activity_id']).agg({
                            #  'counter': 'mean',
                            #  'score': 'mean',
                        'rank': 'mean',
                        'unit_type': lambda x: ', '.join(sorted(set(x.astype(str)))),
                        'country': lambda x: ', '.join(sorted(set(x.astype(str)))),
                        'year': lambda x: ', '.join(sorted(set(x.astype(str)))),
                        'id': lambda x: ', '.join(sorted(set(x.astype(str))))
                            }).reset_index()

    final_output_display_grouped = final_output_display_grouped.sort_values(by=['rank'], ascending=[True])
    final_output_display_grouped = final_output_display_grouped[['footprint','activity_id', 'unit_type', 'country', 'year', 'id','rank']]
    final_output_display_grouped.reset_index(drop=True, inplace=True)
    final_output_display_grouped
    return final_output_display_grouped.to_dict(orient="records")

    
    

@router.get("/calculate", response_model=dict)
def calculat_with_auth():

    # Your calculation logic here
    return {"result": "calculation result with auth"}

@router.get("/units/", response_model=List[schemas.FactorUnitsRead])
async def get_units(db: AsyncSession = Depends(get_async_db)):

    units = await db.execute(select(FactorUnit))
    units_results = units.scalars().all()


    return units_results

@router.get("/public-calculate", response_model=dict)
def calculate_without_auth():
    # Your calculation logic here
    return {"result": "calculation result without auth"}

@router.post('/create-package', tags=["Stripe Packages"])
async def create_package(data: schemas.PackageCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        
        if data.subscription_type.lower() == 'digital':
            # Step 1: Create the product in Stripe
            product = stripe.Product.create(
                name=data.package_name or "New Plan",
                active=True
            )

            # Step 2: Create prices (monthly & yearly) in Stripe
            price_monthly = stripe.Price.create(
                currency="usd",
                unit_amount=int(data.price_monthly * 100),  # Convert to cents
                recurring={"interval": "month"},
                product=product.id
            )

            price_yearly = stripe.Price.create(
                currency="usd",
                unit_amount=int(data.price_yearly * 100),  # Convert to cents
                recurring={"interval": "year"},
                product=product.id
            )

            # Step 3: Handle discounts (coupons) for monthly and yearly prices
            coupon_monthly = None
            coupon_yearly = None

            if data.discount_monthly:
                coupon_monthly = stripe.Coupon.create(
                    amount_off=int(data.discount_monthly * 100),  # Convert to cents
                    currency="usd",
                    duration="forever",
                    applies_to={"products": [product.id]}  # Apply to the specific product
                )

            if data.discount_yearly:
                coupon_yearly = stripe.Coupon.create(
                    amount_off=int(data.discount_yearly * 100),  # Convert to cents
                    currency="usd",
                    duration="forever",
                    applies_to={"products": [product.id]}
                )

            # Step 4: Insert package details into the database
            new_package = StripePackage(
                subscription_type=data.subscription_type,
                package_name=data.package_name,
                team=data.team,
                state=data.state,
                recommended=data.recommended,
                price_monthly=data.price_monthly,
                discount_monthly=data.discount_monthly,
                price_yearly=data.price_yearly,
                discount_yearly=data.discount_yearly,
                features=[feature.dict() for feature in data.features]  # Store features as JSONB
            )
            db.add(new_package)
            await db.flush()
       
           

            # Step 5: Create and attach features to Stripe product and insert into DB
            created_features = []  # To collect feature details for response
            feature_entities = []
            for feature in data.features:
                # Create feature in Stripe
                stripe_feature = stripe.entitlements.Feature.create(
                    name=feature.title,
                    lookup_key=feature.title.replace(" ", "-").lower()  # Generate a unique lookup key
                )

                # Attach the feature to the product
                stripe.Product.create_feature(
                    product=product.id,
                    entitlement_feature=stripe_feature.id
                )

                # Store the feature in the database
                new_feature = StripeFeature(
                    package_id=new_package.id,
                    title=feature.title,
                    caption=feature.caption
                )
                db.add(new_feature)
                feature_entities.append(new_feature)
                # Collect the created feature information
                created_features.append({
                    # "feature_id": new_feature.id,
                    "stripe_feature_id": stripe_feature.id,
                    "title": feature.title,
                    "caption": feature.caption
                })
            await db.commit()  
            # for new_feature in feature_entities:

            #     await db.refresh(new_feature)
    
            # Step 6: Prepare the response with details (including features and discounts)
            response = {
                "message": "Package created successfully",
                "package_id": new_package.id,
                "stripe_product_id": product.id,
                "stripe_price_monthly_id": price_monthly.id,
                "stripe_price_yearly_id": price_yearly.id,
                "original_price_monthly": data.price_monthly,
                "original_price_yearly": data.price_yearly,
                "features": created_features  # Include the created features in the response
            }

            if coupon_monthly:
                response["coupon_monthly_id"] = coupon_monthly.id
                response["discounted_price_monthly"] = data.price_monthly - data.discount_monthly

            if coupon_yearly:
                response["coupon_yearly_id"] = coupon_yearly.id
                response["discounted_price_yearly"] = data.price_yearly - data.discount_yearly
            
            
                
           
            

            return response
        else:
                # For non-digital packages, print manual method message
                print("Manual method required for non-digital packages.")
                return {"message": "Manual method required for non-digital packages."}
    
    except stripe.error.StripeError as e:
        traceback.print_exc()
        db.rollback()  # Rollback transaction in case of Stripe error
        raise HTTPException(status_code=400, detail=f"Stripe Error: {str(e)}")

    except Exception as e:
        traceback.print_exc()
        print(f"Unexpected error: {str(e)}")
        db.rollback()  # Rollback transaction for any other error
        raise HTTPException(status_code=500, detail="An error occurred while creating the package")