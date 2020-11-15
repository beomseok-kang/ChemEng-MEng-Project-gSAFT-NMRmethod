import gSAFTmm
import func_lib as func

recorder = "beom"

compound_name = raw_input("Please put in the compound name.\n")
reference_name = raw_input("Please put in the reference molecule name.\n")

## files

Pvap_filename = "Pvap_" + compound_name + ".csv"
Vsatliq_filename = "Vsatliq_" + compound_name + ".csv"
Vsatvap_filename = "Vsatvap_" + compound_name + ".csv"
NMRcompound_filename = "NMR_" + compound_name + ".csv"
NMRreference_filename = "NMR_" + reference_name + ".csv"

def get_dir(filename, compound):
  return "./data/" + compound + "/" + filename

Pvap_file = func.get_file(get_dir(Pvap_filename, compound_name))
Vsatliq_file = func.get_file(get_dir(Vsatliq_filename, compound_name))
Vsatvap_file = func.get_file(get_dir(Vsatvap_filename, compound_name))

NMRcompound_file = func.get_file(get_dir(NMRcompound_filename, compound_name))
NMRreference_file = func.get_file(get_dir(NMRreference_filename, reference_name))

## gSAFT system

Sys = gSAFTmm.System("GC_Mie_Databank_TL_MW_091120.xml<" + compound_name + ">")

## deviations (average values)

com_arr = func.get_NMR_arr(NMRcompound_file)
ref_arr = func.get_NMR_arr(NMRreference_file)

abs_dev = func.get_avg_abs_dev(com_arr, ref_arr)
rel_dev = func.get_avg_rel_dev(com_arr, ref_arr)

print(abs_dev, rel_dev)

## properties and AAD calculation

Pvap_data = func.get_prop_arr(Pvap_file, "Pvap")
Vsatliq_data = func.get_prop_arr(Vsatliq_file, "Vsatliq")
Vsatvap_data = func.get_prop_arr(Vsatvap_file, "Vsatvap")

print(Pvap_data)
print(Vsatliq_data)
print(Vsatvap_data)

Pvap_AAD = func.get_AAD_avg(Pvap_data, Sys, "VapourPressure")
Vsatliq_AAD = func.get_AAD_avg(Vsatliq_data, Sys, "SaturationLiquidDensity")
Vsatvap_AAD = func.get_AAD_avg(Vsatvap_data, Sys, "SaturationVapourDensity")

## record

for isRel in [True, False]:
  dev = rel_dev if isRel else abs_dev
  for prop in ["Pvap", "Vsatvap", "Vsatliq"]:
    AAD = eval(prop + "_AAD")
    if not AAD:
      print("The property \"" + prop + "\" does not have a AAD value available, so the data hasn't been recorded.")
      continue
    func.record(prop, isRel, recorder, compound_name, dev, AAD)

print(
  """
  \n\n
  ##############################################
  All the processes have been done successfully.
  ##############################################
  \n\n
  """
)