# from typing import List, Optional
# from pydantic import BaseModel, EmailStr, constr
#
# # Define constraints for username and password
# UsernameStr = constr(min_length=3, max_length=255)  # Example constraints
# PasswordStr = constr(min_length=8)  # Example constraints
#
#
# class CodeUserPermissions(BaseModel):
#     code_id: int
#     user_id: int
#     permission_level: str  # Could be an Enum for stricter type checking
#
#
# class Code(BaseModel):
#     code_id: int
#     title: str
#     code_content_location: str  # Path or URL to code content
#     associated_users: List[CodeUserPermissions] = []  # Initialize as empty list
#     other_details: Optional[dict] = None  # Use Optional for potentially missing data
#
#
# class User(BaseModel):
#     user_id: int
#     username: UsernameStr
#     email: EmailStr
#     password: PasswordStr  # In a real application, you'd likely not store the actual password here, but a password hash.
#     associated_codes: List[Code] = []  # Initialize as empty list
#     other_details: Optional[dict] = None
#
#
# class Session(BaseModel):
#     session_id: int
#     code_id: int
#     active_users: List[CodeUserPermissions] = []  # List of CodeUserPermissions objects
#
#
