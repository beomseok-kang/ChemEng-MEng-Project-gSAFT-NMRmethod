import os
import func_lib as funcs

folders = os.listdir("./data")
for prop in ["Pvap", "Vsatvap", "Vsatliq"]:
  result_f = open("./number_of_points_" + prop + ".csv", "w")
  result_f.write("Compound,Tmin,Tmax,n\n")
  for folder in folders:
    try:
      f_dir = prop + "_" + folder + ".csv"
      with open("./data/" + folder + "/" + f_dir, "r") as f:
        arr = funcs.get_prop_arr(f, prop)
        Tmax, Tmin = int(max(a[0] for a in arr)), int(min(a[0] for a in arr))
        n = len(arr)
        result_f.write("{0},{1},{2},{3}\n".format(folder, Tmin, Tmax, n))
        f.close()
    except:
      print("The file does not exist: " + prop + ", " + folder)
  result_f.close()
      