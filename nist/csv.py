import os
import json

dic = dict({ 'Pvap': 'pvap', 'Vsatliq': 'satliq', 'Vsatvap': 'satvap' })

f_dirs = os.listdir("./json")
for f_dir in f_dirs:
  with open("./json/" + f_dir) as json_file:
    data = json.load(json_file)
    compound = data["compound"]
    folder = "../data/" + compound
    if not os.path.exists(folder):
      os.mkdir(folder)
      print("Folder Created: " + folder)
    for p in ['Pvap', 'Vsatliq', 'Vsatvap']:
      if data[dic[p]]["isThere"]:
        string = data[dic[p]]["table"].replace(u"\xa0", "")
        if p == 'Pvap':
          rows = string.split("\n")
          heading = rows[0].split(",")
          heading[1] = "Vapour Pressure (Pa)"
          rows[0] = ",".join(heading)
          for i in range(1, len(rows)):
            row_data = rows[i].split(",")
            try:
              row_data[1] = str(float(row_data[1]) * 1000)
              rows[i] = ",".join(row_data)
            except:
              pass
          string = "\n".join(rows)
        with open(folder + "/" + p + "_" + compound + ".csv", "w") as csv_file:
          csv_file.write(string)
          csv_file.close()
    json_file.close()


    