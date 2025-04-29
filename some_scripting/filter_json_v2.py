import json
import sys
import csv

# Función para obtener los datos complejos de un diccionario anidado
def get_complex_data(item):
    if "packageVulnerabilityDetails" in item:
        #nested_dict = item["packageVulnerabilityDetails"]
        package_vulnerability_details = item["packageVulnerabilityDetails"]
        vulnerability_id = package_vulnerability_details.get("vulnerabilityId", "")
        source_url = package_vulnerability_details.get("sourceUrl", "")
        return vulnerability_id, source_url
        #return nested_dict.get("vulnerabilityId", ""), nested_dict.get("sourceUrl", "")
    return "", ""

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file.json output_file.csv")
        return

    input_file = sys.argv[1]

    with open(input_file, "r") as file:
        data = json.load(file)

    data_list = data.get("findings", [])
    print(f"Total findings: {len(data_list)}")

    with open(sys.argv[2], "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        
        # Escribir encabezados
        csv_writer.writerow(["vulnerabilityId", "severity", "exploitAvailable", "findingArn", "firstObservedAt", "lastObservedAt", "sourceUrl"])
        
        for item in data_list:
            field1 = item.get("severity", "")
            field2 = item.get("exploitAvailable", "")
            field3 = item.get("findingArn", "")
            field4 = item.get("firstObservedAt", "")
            field5 = item.get("lastObservedAt", "")
            vulnerabilityId, sourceUrl = get_complex_data(item)
            
            csv_writer.writerow([vulnerabilityId, field1, field2, field3, field4, field5, sourceUrl])

    print("CSV created successfully.")

if __name__ == "__main__":
    main()
