import func_lib as f

def get_file_name(prop, dev):
  return prop + "_AAD_" + dev + "_dev.csv"

references = dict()

for prop in ["Pvap", "Vsatliq", "Vsatvap"]:
  for dev in ["abs", "rel"]:
    data_f = open("./result/" + get_file_name(prop, dev), "r")
    result_f = open("./bycarbon/" + get_file_name(prop, dev), "w")
    for line in data_f.readlines():
      not_processed = True
      while not_processed:
        try:
          # d = deviation
          compound, d, AAD = line.rstrip().split(",")
          if not references.get(compound):
            ref_input = input("compound: " + compound + "\n")
            if ref_input == "":
              recheck = input("Wanna skip? Y/N" + "\n")
              if recheck == "Y":
                references.update({ compound: "no_ref" })
                break
              continue
            references.update({ compound: ref_input })
          reference = references.get(compound)
          if reference == "no_ref":
            break 
          compound_NMR_f = f.get_file("./data/" + compound + "/NMR_" + compound + ".csv")
          compound_NMR = f.get_NMR_arr(compound_NMR_f)
          reference_NMR_f = f.get_file("./data/" + reference + "/NMR_" + reference + ".csv")
          reference_NMR = f.get_NMR_arr(reference_NMR_f)
          print(compound_NMR, "\n", reference_NMR)
          if len(compound_NMR) != len(reference_NMR):
            print("REFERENCE INCORRECT: " + compound + ", " + reference)
            continue
          carbon1_compound_shift = max(compound_NMR[0], compound_NMR[-1])
          carbon1_reference_shift = reference_NMR[0]
          abs_dev = abs(carbon1_compound_shift - carbon1_reference_shift)
          rel_dev = abs_dev / carbon1_reference_shift
          deviation = abs_dev if dev == "abs" else rel_dev
          result_f.write(compound + "," + str(deviation) + "," + AAD + "\n")
          not_processed = False
          print("processed successfully")
        except:
          not_processed = False
          print("unexpected Error")
    result_f.close()
    data_f.close()