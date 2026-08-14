import pandas as pd
from django.http import HttpResponse
from rest_framework.exceptions import NotFound, ValidationError


def generate_locations_export(queryset, export_format="json"):
    locations_data = list(
        queryset.values(
            "id",
            "name",
            "description",
            "address",
            "latitude",
            "longitude",
            "category__name",
            "rating",
            "created_at",
        )
    )

    if not locations_data:
        raise NotFound("No data available for export.")

    df = pd.DataFrame(locations_data)

    if export_format == "csv":
        content = df.to_csv(index=False, encoding="utf-8-sig")
        content_type = "text/csv"
    elif export_format == "json":
        content = df.to_json(orient="records", force_ascii=False, date_format="iso")
        content_type = "application/octet-stream"
    else:
        raise ValidationError("Unsupported format. Use 'csv' or 'json'.")

    response = HttpResponse(content, content_type=f"{content_type}; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="locations.{export_format}"'

    return response
