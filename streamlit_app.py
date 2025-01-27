import streamlit as st
# from openai import OpenAI
import pandas as pd
import os
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class VantaTest:
    testId: str
    category: str
    detailedDescription: str
    name: str
    testGroup: Optional[str]

# Define test blueprint patterns
TEST_BLUEPRINT_PATTERNS = [
    (r'^[\w-]+-account-linked-in-vanta$', 'ACCOUNT_LINKED_IN_VANTA'),
    (r'^[\w-]+-code-change-approved-or-justified$', 'CODE_CHANGE_HAS_APPROVAL_OR_JUSTIFICATION'),
    (r'^alerts-addressed-within-sla-[\w-]+-[\w-]+-[\w-]+$', 'SECURITY_ALERT_ADDRESSED'),
    (r'^[\w-]+-account-access-removed-on-termination$', 'ACCOUNT_ACCESS_REMOVED_ON_TERMINATION'),
    (r'^[\w-]+-account-mfa-enabled$', 'ACCOUNT_MFA_ENABLED'),
    (r'^packages-checked-for-vulnerabilities-records-closed-[\w-]+-[\w-]+$', 'VULNERABILITIES_CLOSED'),
    (r'^[\w-]+-scanning-configuration$', 'VULN_SCANNING_CONFIGURATION'),
    (r'^[\w-]+-account-access-removed-on-termination$', 'ACCOUNT_ACCESS_REMOVED_ON_TERMINATION_MISMAPPED'),
    (r'^approved-[\w-]+-exists$', 'POLICY_APPROVAL'),
    (r'^employees-accepted-[\w-]+$', 'POLICY_ACCEPTANCE')
]

def get_blueprint_test_group(test_id: str):
    # Check each pattern against the test_id
    for pattern in TEST_BLUEPRINT_PATTERNS:
        regex = pattern[0]
        if re.match(regex, test_id):
            return pattern[1]
            
    return None


st.title("📄 Test de-deduper")
st.write(
    """this is a demo of streamlit and some test deduping logic"""
)

uploaded_file = st.file_uploader(
    "Upload the file noam sent you", type=("csv")
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    all_tests = []

    for index, row in df.iterrows():
        test = VantaTest(
            testId=row["testId"],
            category=row["category"],
            detailedDescription=row["detailedDescription"],
            name=row["name"],
            testGroup=None
        )
        all_tests.append(test)

    tests_with_group = [test for test in all_tests if test.testGroup is not None]
    st.write(f"found {len(tests_with_group)} tests with a group of {len(all_tests)}")

    for test in all_tests:
        maybe_group = get_blueprint_test_group(test.testId)
        if maybe_group:
            test.testGroup = maybe_group

    tests_with_group = [test for test in all_tests if test.testGroup is not None]
    st.write(f"found {len(tests_with_group)} tests with a group of {len(all_tests)}")


    st.write("here's a sample of some tests")
    new_df = pd.DataFrame(tests_with_group)
    st.write(new_df.head(10))

    st.write("here's a sample of some tests without a group")
    new_df = pd.DataFrame([test for test in all_tests if test.testGroup is None])
    st.write(new_df.head(10))

    test_histogram = new_df["testGroup"].value_counts()
    st.write(test_histogram)

    st.slider("how many tests to show?", min_value=1, max_value=100, value=10)
    

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")
# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
# else:

#     # Create an OpenAI client.
#     client = OpenAI(api_key=openai_api_key)

#     # Let the user upload a file via `st.file_uploader`.
#     uploaded_file = st.file_uploader(
#         "Upload a document (.txt or .md)", type=("txt", "md")
#     )

#     # Ask the user for a question via `st.text_area`.
#     question = st.text_area(
#         "Now ask a question about the document!",
#         placeholder="Can you give me a short summary?",
#         disabled=not uploaded_file,
#     )

#     if uploaded_file and question:

#         # Process the uploaded file and question.
#         document = uploaded_file.read().decode()
#         messages = [
#             {
#                 "role": "user",
#                 "content": f"Here's a document: {document} \n\n---\n\n {question}",
#             }
#         ]

#         # Generate an answer using the OpenAI API.
#         stream = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             stream=True,
#         )

#         # Stream the response to the app using `st.write_stream`.
#         st.write_stream(stream)
