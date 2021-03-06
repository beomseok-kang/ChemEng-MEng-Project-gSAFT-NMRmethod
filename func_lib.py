def get_file(file_dir):
  try:
    return open(file_dir, "r")
  except:
    print("There does not exist the file \"" + file_dir + "\". Please try again.")
    return None

### NMR Data Handling

def get_NMR_arr(f):
  if not f:
    raise ValueError("The NMR data does not exist. Please try again.")
  result = []
  f_string = f.read()
  f_string = f_string.replace("\r", "\n")
  for line in f_string.split("\n")[1:]:
    try:
      result.append(float(line.split(",")[1]))
    except:
      print("There was an issue: \"" + line + "\" cannot be converted to float.")
  return result

def get_avg_abs_dev(com_arr, ref_arr):
  # each arr should be in the format: [chem_shift_Carbon1, chem_shift_Carbon2, ...]
  if len(com_arr) != len(ref_arr):
    print("The two molecules have different number of carbons")
    return None
  else:
    summation = 0
    for i in range(len(com_arr)):
      summation += abs(com_arr[i] - ref_arr[i])
    return summation / len(com_arr)

def get_avg_rel_dev(com_arr, ref_arr):
  # each arr should be in the format: [chem_shift_Carbon1, chem_shift_Carbon2, ...]
  if len(com_arr) != len(ref_arr):
    print("The two molecules have different number of carbons")
    return None
  else:
    summation = 0
    for i in range(len(com_arr)):
      summation += abs(com_arr[i] - ref_arr[i]) / ref_arr[i]
    return summation / len(com_arr)

### Property Data Handling

def get_prop_arr(f, name):
  if not f:
    print("The property file does not exist: " + name + ".")
    return None
  result = []
  f_string = f.read()
  f_string = f_string.replace("\r", "\n")
  for line in f_string.split("\n")[1:]:
    try:
      data = [float(i) for i in line.split(",")[0:2]]
      result.append((data[0], data[1]))
    except:
      print("There was an issue: \"" + line + "\" cannot be converted to float.")
  return result

def get_AAD_avg(prop_arr, System, prop_name):
  if not prop_arr:
    print("The property data does not exist, and therefore the AAD cannot be calculated: " + prop_name + ".")
    return None
  result = []
  for prop in prop_arr:
    T, exp = prop
    pred = getattr(System, prop_name)(T)
    result.append(abs((exp - pred) / exp))
  return sum(result) / len(result)

### Record the data

def record(prop, isRel, who, compound, dev, AAD):
  file_dir = "./" + ("record/" + who + "/" if who == "beom" else "") + prop + "_AAD_" + ("rel" if isRel else "abs") + "_dev.csv"
  with open(file_dir, "a") as f:
    f.write(compound + ',' + str(dev) + "," + str(AAD) + "\n")
