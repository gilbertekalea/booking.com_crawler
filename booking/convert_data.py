# This file contains methods that will be used to convert data to different formats such as JSON, CSV, etc.
import csv, json


class ConvertData:

    def __init__(self, data):
        self.data = data
    

    def convert_to_json(self,file_name: str):
        with open(f'../data_request{file_name}.json', 'w') as json_file:
            json.dump(self.data, json_file)
        return json.dumps(self.data)

    def convert_to_csv(self, file_name: str) -> None:
        with open(f'../data_request/{file_name}.csv', 'w', newline='') as csv_file:

            writer = csv.DictWriter(csv_file, fieldnames=self.data[0].keys())
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)
      
    def convert_to_excel(self, file_name: str):
        pass
  
if __name__ == "__main__":
    data = [
        {
            'city': 'London',
            'hotel_name': 'Hotel 1',
            'hotel_type': 'Hotel',
            'location': 'London',
            'price': '100',
            'score': '4.5',
            'checkin': '2020-01-01',
        },
         {
            'city': 'London',
            'hotel_name': 'Hotel 1',
            'hotel_type': 'Hotel',
            'location': 'London',
            'price': '100',
            'score': '4.5',
            'checkin': '2020-01-01',
        }
    ]
    obj = ConvertData(data)
    print(obj.convert_to_json('test'))
    print(obj.convert_to_csv('test'))