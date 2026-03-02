import os
from dotenv import load_dotenv
from mindee import ClientV2, InferenceParameters, PathInput


# Load environment variables from a .env file
load_dotenv()

input_path = "invoice.jpeg"
api_key = os.getenv("MINDEE_V2_API_KEY")
model_id = "5af9168d-0b18-4641-b95c-196456f616c0"

# Init a new client
mindee_client = ClientV2(api_key)
# Set inference parameters
params = InferenceParameters(
    # ID of the model, required.
    model_id=model_id,

    # Options: set to `True` or `False` to override defaults

    # Enhance extraction accuracy with Retrieval-Augmented Generation.
    rag=None,
    # Extract the full text content from the document as strings.
    raw_text=None,
    # Calculate bounding box polygons for all fields.
    polygon=None,
    # Boost the precision and accuracy of all extractions.
    # Calculate confidence scores for all fields.
    confidence=None,
)

# Load a file from disk
input_source = PathInput(input_path)

# Send for processing using polling
response = mindee_client.enqueue_and_get_inference(
    input_source, params
)

fields = response.inference.result.fields

data = {
    "invoice_no": fields["invoice_number"].value,
    "date": fields["date"].value,
    "vendor": fields["supplier_name"].value,
    "po_no": fields["po_number"].value,
    "amount": fields["total_amount"].value,
    "tax": fields["total_tax"].value,
}

line_items = []
if "line_items" in fields:
    for item in fields["line_items"].items:
        sub = item.fields
        line_items.append({
            "description": sub["description"].value,
            "quantity": sub["quantity"].value,
            "total_price": sub["total_price"].value,
            
        })

print(data)
print(line_items)