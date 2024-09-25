
lookup_fields=['country_name', 'state_name', 'city_name', 'industry_sector_name', 'industry_name', 'sub_industry_name']
# Extract unique names for lookup
lookup_values = {field: set() for field in lookup_fields}
row_index = 1

for field in lookup_fields:
        lookup_values[field].add(field)

print(lookup_values)