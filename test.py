from duplicates import DataSanitization


data = DataSanitization("duplicates.txt")
print(data.sanitize())
print(data.manual_delete("iPhone"))
print(data.manual_replacement("5dMark III", "5D Mark III"))
print(data.renamed_by_sanitized)
