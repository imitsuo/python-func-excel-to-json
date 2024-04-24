from io import BytesIO
import functions_framework

import pandas as pd
import numpy as np

@functions_framework.http
def excel_converter_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    if request.content_type != "application/octet-stream":
        return "Invalid content_type", 400

    data = request.get_data()

    if len(data)/1000 > 2000:
        return "Request Entity Too Large", 413

    buffer = BytesIO(data)
    buffer.seek(0)
    df = pd.read_excel(buffer)
    df = df.replace({np.nan: None})

    return df.to_dict(orient="records")
