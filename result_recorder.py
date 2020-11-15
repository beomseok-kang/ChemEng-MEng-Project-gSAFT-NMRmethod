def get_file_name(prop, dev):
  return prop + "_AAD_" + dev + "_dev.csv"

for prop in ["Pvap", "Vsatliq", "Vsatvap"]:
  for dev in ["abs", "rel"]:
    result_f = open("./result/" + get_file_name(prop, dev), "w")
    for recorder in ["beom", "yuting"]:
      file_dir = "./record/" + recorder + "/" + get_file_name(prop, dev)
      f = open(file_dir, "r")
      for line in f.readlines():
        result_f.write(line)
      f.close()
    result_f.close()