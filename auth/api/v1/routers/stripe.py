# from datetime import datetime
# from typing import Optional
# from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
from datetime import timedelta
from sqlalchemy import and_, select
# from auth.dependencies import get_db
from auth.services.auth_service import authenticate_user, create_access_token, get_current_user, hash_password, get_user
# from auth.db.models import User
# from pydantic import BaseModel
from jose import JWTError, jwt
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, File, UploadFile, Form
from sqlalchemy.orm import Session
from datetime import datetime
from auth.dependencies import get_db, get_async_db
from auth.services.auth_service import hash_password
from auth.db.models import *
from pydantic import BaseModel, EmailStr, validator, UUID4
from typing import List, Optional
import uuid
import random
import json
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
# import os
import traceback
import requests
from twilio.rest import Client
from auth.schemas.schemas import BankInformationResp, CompanyTaxRegistrationResp, PersonalInformationResp, UserGoalsTargetResp,Users,UserSettingsAssignmentCreate,SettingsSession,UserBusinessDetailsResp,UserGoalsTargetsCreate,UserGoalsTargets,UserBusinessDetailsCreate,UserBusinessDetails,LoginResponse,UserSettings,BankInformation
from auth.services.email_service import send_approval_email,send_profile_not_accepted_email,send_profile_under_verification_email,send_profile_verified_email,send_rejection_email
from auth.services.file_service import validate_file,save_file
import httpx
import os
from sqlalchemy.orm import selectinload  
from sqlalchemy.ext.asyncio import AsyncSession

otp_store = {}

router = APIRouter(tags=['Stripe'],prefix='/api/v1/Stripe')
								

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth_sso/login-sso/")


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
import stripe
import httpx

# app = FastAPI()

# Set your Stripe API key
# stripe.api_key = "sk_test_51POKYm2MPf6Tg7eRlc19aKXQHKkYMABseM3ZovvX7WAEloOby8uBPnjw7v97gKtxqqMdjGaVigBwD3BmtSkownCP00bpdPnLtN"
# stripe.api_version = "2024-06-20"
stripe.api_key = os.getenv("STRIPE_API")
stripe_success_url = os.getenv("success_url")
stripe_cancel_url = os.getenv("cancel_url")

class Feature(BaseModel):
    title: str
    caption: str
    # stripe_feature_id: Optional[str] = None 
class PackageUpdate(BaseModel):
    package_name: Optional[str] = None  # e.g. basic
    state: bool  # e.g. active/non-active 
    display: bool



class PackageCreate(BaseModel):
    subscription_type: str  # e.g. digital/manual
    package_name: Optional[str] = None  # e.g. basic
    team: Optional[str] = None  # e.g. 0-50
    state: bool  # e.g. active/non-active
    recommended: bool  # e.g. True/False
    price_monthly: int  # e.g. 90
    discount_monthly: Optional[int] = None  # e.g. 10
    price_yearly: int  # e.g. 90
    discount_yearly: Optional[int] = None  # e.g. 20
    digital: bool
    manual: bool
    display:bool
    features: List[Feature]  # List of features associated with the package
    

@router.get("/list-packages")
async def list_stripe_packages(
    limit: int = 3,
    subscription_type: Optional[str] = None,
    package_name: Optional[str] = None,
    team: Optional[str] = None,
    state: Optional[str] = None,
    recommended: Optional[bool] = None,
    display: Optional[bool] = None,
    price_monthly: Optional[int] = None,
    discount_monthly: Optional[int] = None,
    price_yearly: Optional[int] = None,
    discount_yearly: Optional[int] = None,
    stripe_product_id: Optional[str] = None,
    stripe_price_monthly_id: Optional[str] = None,
    stripe_price_yearly_id: Optional[str] = None,
    coupon_monthly_id: Optional[str] = None,
    coupon_yearly_id: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        # Start with the base query
        query = select(StripePackage)

        # Apply filters if provided
        if subscription_type:
            query = query.where(StripePackage.subscription_type == subscription_type)
        if package_name:
            query = query.where(StripePackage.package_name == package_name)
        if team:
            query = query.where(StripePackage.team == team)
        if state:
            query = query.where(StripePackage.state == state)
        if display is not None:
            query = query.where(StripePackage.display == display)
        if recommended is not None:
            query = query.where(StripePackage.recommended == recommended)    
        if price_monthly is not None:
            query = query.where(StripePackage.price_monthly == price_monthly)
        if discount_monthly is not None:
            query = query.where(StripePackage.discount_monthly == discount_monthly)
        if price_yearly is not None:
            query = query.where(StripePackage.price_yearly == price_yearly)
        if discount_yearly is not None:
            query = query.where(StripePackage.discount_yearly == discount_yearly)
        if stripe_product_id:
            query = query.where(StripePackage.stripe_product_id == stripe_product_id)
        if stripe_price_monthly_id:
            query = query.where(StripePackage.stripe_price_monthly_id == stripe_price_monthly_id)
        if stripe_price_yearly_id:
            query = query.where(StripePackage.stripe_price_yearly_id == stripe_price_yearly_id)
        if coupon_monthly_id:
            query = query.where(StripePackage.coupon_monthly_id == coupon_monthly_id)
        if coupon_yearly_id:
            query = query.where(StripePackage.coupon_yearly_id == coupon_yearly_id)

        # Limit the number of packages returned
        query = query.limit(limit)

        # Execute the query
        result = await db.execute(query)
        
        packages = result.scalars().all()

        # If no packages are found, return a 404 error
        if not packages:
            raise HTTPException(status_code=404, detail="No packages found")

        # Prepare response data
        response = []
        for package in packages:
            # discounted_price_monthly = package.price_monthly - (package.discount_monthly if package.discount_monthly else 0)
            # discounted_price_yearly = package.price_yearly - (package.discount_yearly if package.discount_yearly else 0)

            package_data = {
                "package_id": package.id,
                "subscription_type": package.subscription_type,
                "package_name": package.package_name,
                "team": package.team,
                "state": package.state,
                "recommended": package.recommended,
                "price_monthly": package.price_monthly,
                "discount_monthly": package.discount_monthly,
                "discounted_price_monthly": package.discounted_price_monthly,
                "price_yearly": package.price_yearly,
                "discount_yearly": package.discount_yearly,
                "discounted_price_yearly": package.discounted_price_yearly,
                "features": package.features,  # Directly return the JSON data
                "stripe_product_id": package.stripe_product_id,
                "stripe_price_monthly_id": package.stripe_price_monthly_id,
                "stripe_price_yearly_id": package.stripe_price_yearly_id,
                "coupon_monthly_id": package.coupon_monthly_id,
                "coupon_yearly_id": package.coupon_yearly_id,
                "created_at": package.created_at,
                "display":package.display
            }
            response.append(package_data)

        return {"message": f"Successfully retrieved {len(response)} packages", "packages": response}

    except Exception as e:
        print(f"Error fetching packages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post('/create-package')
async def create_package(data: PackageCreate, db: AsyncSession = Depends(get_async_db)):
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
                unit_amount=int(data.price_monthly * 100),
                recurring={"interval": "month"},
                product=product.id
            )

            price_yearly = stripe.Price.create(
                currency="usd",
                unit_amount=int(data.price_yearly * 100),
                recurring={"interval": "year"},
                product=product.id
            )

            # Step 3: Handle discounts (coupons)
            coupon_monthly = None
            coupon_yearly = None

            if data.discount_monthly:
                coupon_monthly = stripe.Coupon.create(
                    # amount_off=int(data.discount_monthly * 100),
                    percent_off=data.discount_monthly,
                    currency="usd",
                    duration="forever",
                    applies_to={"products": [product.id]}
                )

            if data.discount_yearly:
                coupon_yearly = stripe.Coupon.create(
                    # amount_off=int(data.discount_yearly * 100),
                    percent_off=data.discount_yearly,
                    currency="usd",
                    duration="forever",
                    applies_to={"products": [product.id]}
                )

            # Calculate the percentage-based discounted prices
            discounted_price_monthly = data.price_monthly - (data.price_monthly * (data.discount_monthly / 100) if data.discount_monthly else 0)
            discounted_price_yearly = data.price_yearly - (data.price_yearly * (data.discount_yearly / 100) if data.discount_yearly else 0)

            new_package = StripePackage(
                subscription_type=data.subscription_type,
                package_name=data.package_name,
                team=data.team,
                state=data.state,
                manual=data.manual,
                digital=data.digital,
                recommended=data.recommended,
                display=data.display,
                price_monthly=data.price_monthly,
                discount_monthly=data.discount_monthly,
                price_yearly=data.price_yearly,
                discount_yearly=data.discount_yearly,
                discounted_price_monthly=discounted_price_monthly,  # Percentage discount applied
                discounted_price_yearly=discounted_price_yearly,    # Percentage discount applied
                stripe_product_id=product.id,
                stripe_price_monthly_id=price_monthly.id,
                stripe_price_yearly_id=price_yearly.id,
                coupon_monthly_id=coupon_monthly.id if coupon_monthly else None,
                coupon_yearly_id=coupon_yearly.id if coupon_yearly else None,

                features=[feature.dict() for feature in data.features]
            )
            db.add(new_package)

            # db.add(new_package)
            await db.flush()

            # Step 5: Create and attach features to Stripe product and insert into DB
            created_features = []
            for feature in data.features:
                stripe_feature = stripe.entitlements.Feature.create(
                    name=feature.title,
                    lookup_key=feature.title.replace(" ", "-").lower()
                )

                stripe.Product.create_feature(
                    product=product.id,
                    entitlement_feature=stripe_feature.id
                )

                new_feature = StripeFeature(
                    package_id=new_package.id,
                    stripe_feature_id=stripe_feature.id,
                    title=feature.title,
                    caption=feature.caption
                )
                db.add(new_feature)
                created_features.append({
                    "stripe_feature_id": stripe_feature.id,
                    "title": feature.title,
                    "caption": feature.caption
                })
            await db.commit()

            # Step 6: Prepare the response with details
            response = {
                "message": "Package created successfully",
                "package_id": new_package.id,
                "subscription type":data.subscription_type,
                "package_name":data.package_name,
                "team":data.team,
                "state":data.state,
                "recommended":data.recommended,
                "display":data.display,
                "price_monthly":data.price_monthly,
                "discount_monthly":data.discount_monthly,
                "price_yearly":data.price_yearly,
                "discount_yearly":data.discount_yearly,
                
                "stripe_product_id": product.id,
                "stripe_price_monthly_id": price_monthly.id,
                "stripe_price_yearly_id": price_yearly.id,
                "coupon_monthly_id": coupon_monthly.id if coupon_monthly else None,
                "coupon_yearly_id": coupon_yearly.id if coupon_yearly else None,
                "discounted_price_monthly": discounted_price_monthly,
                "discounted_price_yearly": discounted_price_yearly,
                "features": created_features,
                
            }

            return response
        else:
            print("Manual method required for non-digital packages.")
            return {"message": "Manual method required for non-digital packages."}
    
    except stripe.error.StripeError as e:
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Stripe Error: {str(e)}")
    
    except Exception as e:
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the package")


@router.put("/modify-package/{package_id}")
async def modify_package(
    package_id: int, 
    package_update:PackageUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        # Step 1: Fetch the package from the database
        package = await db.get(StripePackage, package_id)
        
        # Step 2: Check if the package exists
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
        
        # Step 3: Modify the fields only if they are provided in the request
        if package_update.display is not None:
            package.display = package_update.display
        
        if package_update.state is not None:
            package.state = package_update.state
        
        package.package_name = package_update.package_name
        package.updated_at = datetime.utcnow()
            
            # Update the corresponding product in Stripe with the new metadata
        stripe.Product.modify(
                package.stripe_product_id,  # Use the Stripe product ID from the database
                active= package_update.state,
                name= package_update.package_name
                # metadata={"active": status}  # Update metadata as needed
            )
        
        # Step 4: Save the changes
        await db.commit()
        
        return {
            "message": "Package updated successfully", 
            "package_id": package.id, 
            "display": package.display, 
            "status": package.state,
            "stripe_product_id": package.stripe_product_id  # Include Stripe product ID in the response
        }

    except stripe.error.StripeError as e:
        # If there is a Stripe error, rollback the transaction and return an error message
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Stripe Error: {str(e)}")

    except Exception as e:
        # If something else goes wrong, rollback the transaction and raise a server error
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/modify-package/{package_id}")
async def delete_package(
    package_id: int, 
    db: AsyncSession = Depends(get_async_db)
):
    
    try:
        # Step 1: Fetch the package from the database
        package = await db.get(StripePackage, package_id)
        
        # Step 2: Check if the package exists
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
        
    
        package.display = False
    
        package.state = False

        package.deleted_at = datetime.utcnow()

        stripe.Product.modify(
                package.stripe_product_id,  # Use the Stripe product ID from the database
                active= False
                # metadata={"active": status}  # Update metadata as needed
            )
        
        await db.commit()

        return {
            "msg": "Package deleted successfully"
        }

    except stripe.error.StripeError as e:
        # If there is a Stripe error, rollback the transaction and return an error message
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Stripe Error: {str(e)}")

    except Exception as e:
        # If something else goes wrong, rollback the transaction and raise a server error
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")   

        


# @router.put("/modify-package/{package_id}")
# async def modify_package(
#     package_id: int, 
#     display: bool = None, 
#     status: str = None, 
#     db: AsyncSession = Depends(get_async_db)
# ):
#     try:
#         # Step 1: Fetch the package from the database
#         package = await db.get(StripePackage, package_id)
        
#         # Step 2: Check if the package exists
#         if not package:
#             raise HTTPException(status_code=404, detail="Package not found")
        
#         # Step 3: Modify the fields only if they are provided in the request
#         if display is not None:
#             package.display = display
        
#         if status is not None:
#             package.status = status
            
#             # Update the corresponding product in Stripe with the new metadata
#             stripe.Product.modify(
#                 package.stripe_product_id,  # Use the Stripe product ID from the database
#                 metadata={"status": status}  # Update metadata as needed
#             )
        
#         # Step 4: Save the changes
#         await db.commit()
        
#         return {
#             "message": "Package updated successfully", 
#             "package_id": package.id, 
#             "display": package.display, 
#             "status": package.status
#         }

#     except stripe.error.StripeError as e:
#         # If there is a Stripe error, rollback the transaction and return an error message
#         await db.rollback()
#         raise HTTPException(status_code=400, detail=f"Stripe Error: {str(e)}")

#     except Exception as e:
#         # If something else goes wrong, rollback the transaction and raise a server error
#         await db.rollback()
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @router.put("/modify-package/{package_id}")
# async def modify_package(package_id: int, display: bool = None, status: str = None, db: AsyncSession = Depends(get_async_db)):
#     try:
#         # Step 1: Fetch the package from the database
#         package = await db.get(StripePackage, package_id)
        
#         # Step 2: Check if the package exists
#         if not package:
#             raise HTTPException(status_code=404, detail="Package not found")
        
#         # Step 3: Modify the fields only if they are provided in the request
#         if display is not None:
#             package.display = display
        
#         if status is not None:
#             package.status = status
        
#         # Step 4: Save the changes
#         await db.commit()
        
#         return {"message": "Package updated successfully", "package_id": package.id, "display": package.display, "status": package.status}

#     except Exception as e:
#         # If something goes wrong, rollback the transaction and raise a server error
#         await db.rollback()
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
# @router.put('/modify-package/{package_id}')
# async def modify_package(
#     package_id: str,
#     display: bool,
#     status: str,
#     db: AsyncSession = Depends(get_async_db)
# ):
#     try:
#         # Step 1: Fetch the existing package from your DB
#         package = await db.get(StripePackage, id)
#         if not package:
#             raise HTTPException(status_code=404, detail="Package not found")

#         # Step 2: Modify the Stripe product to update display and status
#         updated_product = stripe.Product.modify(
#             package.stripe_product_id,  # Use the stored Stripe product ID
#             metadata={"display": display},  # Example metadata modification for `display`
#             active=status                 # Change the active status
#         )

#         # Step 3: Update the package details in the local DB
#         package.display = display
#         package.state = "active" if status else "inactive"  # Update status to active/inactive
#         db.add(package)
#         await db.commit()

#         return {
#             "message": "Package updated successfully",
#             "package_id": package_id,
#             "display": display,
#             "status": "active" if status else "inactive",
#             "stripe_product_id": updated_product.id
#         }
    
#     except stripe.error.StripeError as e:
#         raise HTTPException(status_code=400, detail=f"Stripe Error: {str(e)}")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail="An error occurred while updating the package")

@router.post("/create-checkout-session")
async def create_checkout_session(
    price: str = Query(..., description="The price ID of the product."),
    quantity: int = Query(1, description="The quantity of the product."),
    mode: str = Query('subscription', description="The mode of the checkout session. Defaults to 'subscription'."),
    success_url: str = Query(f"{stripe_success_url}?session_id={{CHECKOUT_SESSION_ID}}", description="URL to redirect to after successful payment."),
    cancel_url: str = Query(f"{stripe_cancel_url}?session_id={{CHECKOUT_SESSION_ID}}", description="URL to redirect to if payment is canceled."),
    coupon_id: str = Query(None, description="Optional coupon ID to apply a discount.")
):
    try:
        # Prepare the session parameters
        session_params = {
            # 'payment_method_types': ['card'],
            'line_items': [{
                'price': price,
                'quantity': quantity,
            }],
            'mode': mode,
            'success_url': success_url,
            'cancel_url': cancel_url,
        }

        # If a coupon ID is provided, add the discount
        if coupon_id:
            session_params['discounts'] = [{'coupon': coupon_id}]

        # Create the checkout session
        session = stripe.checkout.Session.create(**session_params)

        # Return the session URL for the client to redirect to
        return {
            "message": "Checkout session created successfully wowow",
            "checkout_url": session.url,
            "session": session.id
        }

    except stripe.error.StripeError as e:
        # Handle Stripe API errors
        raise HTTPException(status_code=400, detail=f"Stripe Error: {str(e)}")

    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



@router.post("/create-subscription")
async def create_subscription(
    customer_id: str = Query(..., description="The ID of the customer."),
    price_id: str = Query(..., description="The price ID for the subscription."),
    discount_id: str = Query(None, description="Optional discount ID to apply to the subscription.")
):
    try:
        # Prepare subscription parameters
        subscription_params = {
            'customer': customer_id,
            'items': [{'price': price_id}]
        }

        # Add discount if provided
        if discount_id:
            subscription_params['discounts'] = [{'coupon': discount_id}]
        
        # Create subscription with Stripe
        subscription = stripe.Subscription.create(**subscription_params)
        
        # Return subscription details
        return {
            "message": "Subscription created successfully",
            "subscription": subscription
        }
    
    except stripe.error.StripeError as e:
        # Handle Stripe API errors
        raise HTTPException(status_code=400, detail=f"Stripe Error: {str(e)}")
    
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")    