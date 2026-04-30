# CreateContributionTestScript.py
#
# Developed by Jeffrey Rissman
#
# This is a Python script that is used to generate a Vensim command script.
# The Vensim command script will perform one run with all selected policies
# enabled, one run with all policies disabled (a BAU run),
# and one run with each defined subset (or "group") within the set of selected
# policies turned off or turned on (depending on a user setting in this script).


# File Names
# ----------
# Rather than including input and output file names in the code below, we assign all the file
# names to variables in this section.  This allows the names to be easily changed if desired.
ModelFile = "EPS.mdl" # The name of the Vensim model file (typically with .mdl or .vpmx extension)
FirstYear = "2020" # The first year you wish to include in the output file (cannot be prior to first simulated year)
FinalYear = "2060" # The last year you wish to include in the output file (cannot be later than last simulated year)
OutputScript = "GeneratedContributionTestScript - 145.cmd" # The desired filename of the Vensim command script to be generated
RunResultsFile = "ContributionTestResults - 145.tsv" # The desired filename for TSV file containing model run results
OutputVarsFile = "OutputVarsForWedgeDiagram.lst" # The name of the file containing a list of variables to be included in the RunResultsFile
                                                 # May optionally also be used as a SAVELIST for Vensim (see below)

# Other Settings
# --------------
RunName = "MostRecentRun" # The desired name for all runs performed.  Used as the filename for the .vdfx files that Vensim creates
EnableOrDisableGroups = "Enable" # Should each group be enabled or disabled in turn?
								 # Essentially, this is testing either the contribution of a group in the proximity of the
								 # BAU case ("Enable") or in the proximity of a scenario defined in the non-zero values of
								 # the policies listed below ("Disable").
PolicySchedule = 4 # The number of the policy implementation schedule file to be used (in InputData/plcy-schd/FoPITY)


# Index definitions
# -----------------
# Each policy is a Python list.  The numbers below are a key to the meaning of the four entries
# that compose each policy, so we can refer to them by meaningful names in the code.
# Note that the fourth entry in each policy, Settings, is itself a list that contains various
# setting values.  Do not change any names or numbers in this section.
Enabled = 0
LongName = 1
ShortName = 2
Settings = 3
Group = 4


# Policy Options
# --------------
# This section specifies which policies should be included in the Vensim command script
# (called here "enabled" policies) and what setting values for those policies should
# be included.  Unless you are using "Enable" Groups mode, all non-repeating
# combinations of the settings for enabled policies will
# be included in the Vensim command script, so do not enable too many policies at once, or
# Vensim will be unable to complete the necessary runs in a reasonable amount of time.
# Each policy is on a single line:
  # You may change the first entry of each policy to "False" to enable the policy or "False" to disable it.
  # The second and third entries are the long and short name of the policy, used internally by this script.  Do not change these names.
  # The fourth entry in each policy is a list of setting values enclosed with square brackets.
    # You may change these values, add more values (separated by commas), and delete values.
    # Any enabled policy must have a minimum of one setting value.  A policy that is disabled
    # and a policy with a setting of zero produce identical results.
  # The fifth entry in each policy is its group name.  By default, each policy is in its own group (and its subscripts share that group).
    # Change the group names so multiple policies share a name (like "financial policies") to cause them to be enabled or disabled together.

PotentialPolicies = (
# Transportation Sector Policies
(False,"Percentage Reduction of Separately Regulated Pollutants[LDVs,VOC]","Conventional Pollutant Standards - LDVs VOCs",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[LDVs,CO]","Conventional Pollutant Standards - LDVs CO",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[LDVs,NOx]","Conventional Pollutant Standards - LDVs NOx",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[LDVs,PM10]","Conventional Pollutant Standards - LDVs PM10",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[LDVs,PM25]","Conventional Pollutant Standards - LDVs PM2.5",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[LDVs,SOx]","Conventional Pollutant Standards - LDVs SOx",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[LDVs,BC]","Conventional Pollutant Standards - LDVs BC",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[LDVs,OC]","Conventional Pollutant Standards - LDVs OC",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[HDVs,VOC]","Conventional Pollutant Standards - HDVs VOCs",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[HDVs,CO]","Conventional Pollutant Standards - HDVs CO",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[HDVs,NOx]","Conventional Pollutant Standards - HDVs NOx",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[HDVs,PM10]","Conventional Pollutant Standards - HDVs PM10",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[HDVs,PM25]","Conventional Pollutant Standards - HDVs PM2.5",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[HDVs,SOx]","Conventional Pollutant Standards - HDVs SOx",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[HDVs,BC]","Conventional Pollutant Standards - HDVs BC",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[HDVs,OC]","Conventional Pollutant Standards - HDVs OC",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[aircraft,VOC]","Conventional Pollutant Standards - aircraft VOCs",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[aircraft,NOx]","Conventional Pollutant Standards - aircraft NOx",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[rail,VOC]","Conventional Pollutant Standards - rail VOCs",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[rail,CO]","Conventional Pollutant Standards - rail CO",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[rail,NOx]","Conventional Pollutant Standards - rail NOx",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[rail,PM10]","Conventional Pollutant Standards - rail PM10",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[rail,PM25]","Conventional Pollutant Standards - rail PM2.5",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[rail,BC]","Conventional Pollutant Standards - rail BC",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[rail,OC]","Conventional Pollutant Standards - rail OC",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[ships,VOC]","Conventional Pollutant Standards - ships VOCs",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[ships,CO]","Conventional Pollutant Standards - ships CO",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[ships,NOx]","Conventional Pollutant Standards - ships NOx",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[ships,PM10]","Conventional Pollutant Standards - ships PM10",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[ships,PM25]","Conventional Pollutant Standards - ships PM2.5",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[ships,BC]","Conventional Pollutant Standards - ships BC",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[ships,OC]","Conventional Pollutant Standards - ships OC",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[motorbikes,VOC]","Conventional Pollutant Standards - motorbikes VOCs",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[motorbikes,CO]","Conventional Pollutant Standards - motorbikes CO",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[motorbikes,NOx]","Conventional Pollutant Standards - motorbikes NOx",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[motorbikes,PM10]","Conventional Pollutant Standards - motorbikes PM10",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[motorbikes,PM25]","Conventional Pollutant Standards - motorbikes PM2.5",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[motorbikes,SOx]","Conventional Pollutant Standards - motorbikes SOx",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[motorbikes,BC]","Conventional Pollutant Standards - motorbikes BC",[0,1],"Conventional Pollutant Standard"),
(False,"Percentage Reduction of Separately Regulated Pollutants[motorbikes,OC]","Conventional Pollutant Standards - motorbikes OC",[0,1],"Conventional Pollutant Standard"),
(True,"EV Charger Deployment","Electric Vehicle Charger Deployment",[0,300],"EV Charger Deployment"),
(True,"Reduce EV Range Anxiety and Charging Time","Electric Vehicle Range n Charging Time",[0,1],"EV Range n Charging Time"),
(True,"Minimum Required ZEV Sales Percentage[passenger,LDVs]","Zero-Emission Vehicle Sales Standard - Passenger Cars and SUVs",[0,1],"ZEV Sales Standard"),
(True,"Minimum Required ZEV Sales Percentage[freight,LDVs]","Zero-Emission Vehicle Sales Standard - Freight Light and Medium Commercial Trucks",[0,1],"ZEV Sales Standard"),
(True,"Minimum Required ZEV Sales Percentage[passenger,HDVs]","Zero-Emission Vehicle Sales Standard - Passenger Buses",[0,1],"ZEV Sales Standard"),
(True,"Minimum Required ZEV Sales Percentage[freight,HDVs]","Zero-Emission Vehicle Sales Standard - Freight Heavy Duty Trucks",[0,1],"ZEV Sales Standard"),
(True,"Minimum Required ZEV Sales Percentage[passenger,aircraft]","Zero-Emission Vehicle Sales Standard - Passenger Commercial flights",[0,0.5],"ZEV Sales Standard"),
(True,"Minimum Required ZEV Sales Percentage[passenger,rail]","Zero-Emission Vehicle Sales Standard - Passenger Rail",[0,1],"ZEV Sales Standard"),
(True,"Minimum Required ZEV Sales Percentage[freight,rail]","Zero-Emission Vehicle Sales Standard - Freight Rail",[0,1],"ZEV Sales Standard"),
(True,"Minimum Required ZEV Sales Percentage[passenger,ships]","Zero-Emission Vehicle Sales Standard - Passenger Recreational boats",[0,0.4],"ZEV Sales Standard"),
(True,"Minimum Required ZEV Sales Percentage[freight,ships]","Zero-Emission Vehicle Sales Standard - Freight Cargo ships",[0,0.5],"ZEV Sales Standard"),
(True,"Minimum Required ZEV Sales Percentage[passenger,motorbikes]","Zero-Emission Vehicle Sales Standard - Passenger Motorbikes",[0,1],"ZEV Sales Standard"),
(True,"Minimum Required ZEV Sales Percentage[freight,motorbikes]","Zero-Emission Vehicle Sales Standard - Freight Motorbikes",[0,1],"ZEV Sales Standard"),
(True,"Boolean Use Non BAU ZEV Qualifying Vehicle Defintions","Non BAU ZEV Qualifying Vehicles",[0,1],"ZEV Sales Standard"),
(False,"Additional EV Subsidy Percentage[passenger,LDVs]","Electric Vehicle Subsidy - Passenger Cars and SUVs",[0,0.5],"EV Subsidy"),
(True,"Additional EV Subsidy Percentage[freight,LDVs]","Electric Vehicle Subsidy - Freight Light and Medium Commercial Trucks",[0,0.15],"EV Subsidy"),
(True,"Additional EV Subsidy Percentage[freight,HDVs]","Electric Vehicle Subsidy - Freight Heavy Duty Trucks",[0,0.15],"EV Subsidy"),
(False,"LDVs Feebate Rate","Feebate",[0,1],"Feebate"),
(True,"Percentage Additional Improvement of Fuel Economy Std[passenger,LDVs]","Fuel Economy Standard - Passenger Cars and SUVs",[0,32],"Vehicle Fuel Economy Standards"),
(True,"Percentage Additional Improvement of Fuel Economy Std[freight,LDVs]","Fuel Economy Standard - Freight Light and Medium Commercial Trucks",[0,0.3],"Vehicle Fuel Economy Standards"),
(True,"Percentage Additional Improvement of Fuel Economy Std[passenger,HDVs]","Fuel Economy Standard - Passenger Buses",[0,0.3],"Vehicle Fuel Economy Standards"),
(True,"Percentage Additional Improvement of Fuel Economy Std[freight,HDVs]","Fuel Economy Standard - Freight Heavy Duty Trucks",[0,0.3],"Vehicle Fuel Economy Standards"),
(False,"Percentage Additional Improvement of Fuel Economy Std[passenger,aircraft]","Fuel Economy Standard - Passenger Commercial flights",[0,1],"Vehicle Fuel Economy Standards"),
(False,"Percentage Additional Improvement of Fuel Economy Std[freight,aircraft]","Fuel Economy Standard - Freight Commercial flights",[0,1],"Vehicle Fuel Economy Standards"),
(True,"Percentage Additional Improvement of Fuel Economy Std[passenger,rail]","Fuel Economy Standard - Passenger Rail",[0,0.09],"Vehicle Fuel Economy Standards"),
(True,"Percentage Additional Improvement of Fuel Economy Std[freight,rail]","Fuel Economy Standard - Freight Rail",[0,0.09],"Vehicle Fuel Economy Standards"),
(True,"Percentage Additional Improvement of Fuel Economy Std[passenger,ships]","Fuel Economy Standard - Passenger Recreational boats",[0,0.06],"Vehicle Fuel Economy Standards"),
(True,"Percentage Additional Improvement of Fuel Economy Std[freight,ships]","Fuel Economy Standard - Freight Cargo ships",[0,0.1],"Vehicle Fuel Economy Standards"),
(False,"Percentage Additional Improvement of Fuel Economy Std[passenger,motorbikes]","Fuel Economy Standard - Passenger Motorbikes",[0,1],"Vehicle Fuel Economy Standards"),
(False,"Additional LCFS Percentage","Low Carbon Fuel Standard",[0,1],"Low Carbon Fuel Standard"),
(True,"Percent of Travel Demand Shifted to Other Modes or Eliminated[passenger,LDVs]","Mode Shifting - Passenger Cars and SUVs",[0,0.1],"Mode Shifting"),
(True,"Percent of Travel Demand Shifted to Other Modes or Eliminated[passenger,aircraft]","Mode Shifting - Passenger Commercial flights",[0,0.2],"Mode Shifting"),
(False,"Percent of Travel Demand Shifted to Other Modes or Eliminated[freight,LDVs]","Mode Shifting - Freight Light and Medium Commercial Trucks",[0,0.26],"Mode Shifting"),
(True,"Percent of Travel Demand Shifted to Other Modes or Eliminated[freight,HDVs]","Mode Shifting - Freight Heavy Duty Trucks",[0,0.3],"Mode Shifting"),

# Buildings and Appliances Sector Policies
(True,"Fraction of New Bldg Components Shifted to Other Fuels[heating,urban residential]","Building Component Electrification - Heating Urban Residential",[0,0.99],"Building Component Electrification"),
(True,"Fraction of New Bldg Components Shifted to Other Fuels[appliances,urban residential]","Building Component Electrification - Appliances Urban Residential",[0,0.99],"Building Component Electrification"),
(False,"Fraction of New Bldg Components Shifted to Other Fuels[other component,urban residential]","Building Component Electrification - Other Components Urban Residential",[0,1],"Building Component Electrification"),
(True,"Fraction of New Bldg Components Shifted to Other Fuels[heating,rural residential]","Building Component Electrification - Heating Rural Residential",[0,0.99],"Building Component Electrification"),
(True,"Fraction of New Bldg Components Shifted to Other Fuels[appliances,rural residential]","Building Component Electrification - Appliances Rural Residential",[0,0.99],"Building Component Electrification"),
(False,"Fraction of New Bldg Components Shifted to Other Fuels[other component,rural residential]","Building Component Electrification - Other Components Rural Residential",[0,1],"Building Component Electrification"),
(True,"Fraction of New Bldg Components Shifted to Other Fuels[heating,commercial]","Building Component Electrification - Heating Commercial",[0,0.99],"Building Component Electrification"),
(True,"Fraction of New Bldg Components Shifted to Other Fuels[appliances,commercial]","Building Component Electrification - Appliances Commercial",[0,0.99],"Building Component Electrification"),
(False,"Fraction of New Bldg Components Shifted to Other Fuels[other component,commercial]","Building Component Electrification - Other Components Commercial",[0,1],"Building Component Electrification"),
(True,"Reduction in E Use Allowed by Component Eff Std[heating,urban residential]","Building Energy Efficiency Standards - Heating Urban Residential",[0,0.413],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,urban residential]","Building Energy Efficiency Standards - Cooling and Ventilation Urban Residential",[0,0.463],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[envelope,urban residential]","Building Energy Efficiency Standards - Envelope Urban Residential",[0,0.5],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[lighting,urban residential]","Building Energy Efficiency Standards - Lighting Urban Residential",[0,0.491],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[appliances,urban residential]","Building Energy Efficiency Standards - Appliances Urban Residential",[0,0.128],"Building Energy Efficiency Standards"),
(False,"Reduction in E Use Allowed by Component Eff Std[other component,urban residential]","Building Energy Efficiency Standards - Other Components Urban Residential",[0,0.75],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[heating,rural residential]","Building Energy Efficiency Standards - Heating Rural Residential",[0,0.413],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,rural residential]","Building Energy Efficiency Standards - Cooling and Ventilation Rural Residential",[0,0.463],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[envelope,rural residential]","Building Energy Efficiency Standards - Envelope Rural Residential",[0,0.5],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[lighting,rural residential]","Building Energy Efficiency Standards - Lighting Rural Residential",[0,0.491],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[appliances,rural residential]","Building Energy Efficiency Standards - Appliances Rural Residential",[0,0.128],"Building Energy Efficiency Standards"),
(False,"Reduction in E Use Allowed by Component Eff Std[other component,rural residential]","Building Energy Efficiency Standards - Other Components Rural Residential",[0,0.75],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[heating,commercial]","Building Energy Efficiency Standards - Heating Commercial",[0,0.413],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,commercial]","Building Energy Efficiency Standards - Cooling and Ventilation Commercial",[0,0.463],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[envelope,commercial]","Building Energy Efficiency Standards - Envelope Commercial",[0,0.563],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[lighting,commercial]","Building Energy Efficiency Standards - Lighting Commercial",[0,0.491],"Building Energy Efficiency Standards"),
(True,"Reduction in E Use Allowed by Component Eff Std[appliances,commercial]","Building Energy Efficiency Standards - Appliances Commercial",[0,0.128],"Building Energy Efficiency Standards"),
(False,"Reduction in E Use Allowed by Component Eff Std[other component,commercial]","Building Energy Efficiency Standards - Other Components Commercial",[0,0.75],"Building Energy Efficiency Standards"),
(False,"Boolean Improved Contractor Edu and Training","Contractor Training",[0,1],"Contractor Training"),
(False,"Min Fraction of Total Elec Demand to be Met by Distributed Solar PV","Distributed Solar Carve-Out",[0,0.1285],"Distributed Solar Promotion"),
(False,"Perc Subsidy for Distributed Solar PV Capacity","Distributed Solar Subsidy",[0,0.5],"Distributed Solar Promotion"),
(True,"Share of Preexisting Buildings Subject to Retrofitting[urban residential]","Retrofit Existing Buildings - Urban Residential",[0,0.4],"Increased Retrofitting"),
(True,"Share of Preexisting Buildings Subject to Retrofitting[rural residential]","Retrofit Existing Buildings - Rural Residential",[0,0.4],"Increased Retrofitting"),
(True,"Share of Preexisting Buildings Subject to Retrofitting[commercial]","Retrofit Existing Buildings - Commercial",[0,0.4],"Increased Retrofitting"),
(False,"Boolean Rebate Program for Efficient Components[heating]","Rebate for Efficient Products - Heating",[0,1],"Rebate for Efficient Products"),
(False,"Boolean Rebate Program for Efficient Components[cooling and ventilation]","Rebate for Efficient Products - Cooling and Ventilation",[0,1],"Rebate for Efficient Products"),
(False,"Boolean Rebate Program for Efficient Components[appliances]","Rebate for Efficient Products - Appliances",[0,1],"Rebate for Efficient Products"),

# Electricity Supply Sector Policies
(True,"Boolean Ban New Power Plants[hard coal es]","Ban New Power Plants - Hard Coal",[0,1],"Ban New Power Plants"),
(False,"Boolean Ban New Power Plants[natural gas nonpeaker es]","Ban New Power Plants - Natural Gas Nonpeaker",[0,1],"Ban New Power Plants"),
(False,"Boolean Ban New Power Plants[nuclear es]","Ban New Power Plants - Nuclear",[0,1],"Ban New Power Plants"),
(False,"Boolean Ban New Power Plants[hydro es]","Ban New Power Plants - Hydro",[0,1],"Ban New Power Plants"),
(True,"Boolean Ban New Power Plants[geothermal es]","Ban New Power Plants - Geothermal",[0,1],"Ban New Power Plants"),
(True,"Boolean Ban New Power Plants[petroleum es]","Ban New Power Plants - Petroleum",[0,1],"Ban New Power Plants"),
(True,"Boolean Ban New Power Plants[lignite es]","Ban New Power Plants - Gangue",[0,1],"Ban New Power Plants"),
(True,"Boolean Ban New Power Plants[crude oil es]","Ban New Power Plants - Crude Oil",[0,1],"Ban New Power Plants"),
(True,"Boolean Ban New Power Plants[heavy or residual fuel oil es]","Ban New Power Plants - Heavy or Residual Fuel Oil",[0,1],"Ban New Power Plants"),
(True,"Electricity Sector Fraction of Potential Additional CCS Achieved[hard coal es]","Carbon Capture and Sequestration - Hard Coal",[0,1],"Clean Electricity Standard"),
(False,"Electricity Sector Fraction of Potential Additional CCS Achieved[natural gas nonpeaker es]","Carbon Capture and Sequestration - Natural Gas Nonpeaker",[0,1],"Clean Electricity Standard"),
(False,"Electricity Sector Fraction of Potential Additional CCS Achieved[biomass es]","Carbon Capture and Sequestration - Biomass",[0,1],"Clean Electricity Standard"),
(False,"Electricity Sector Fraction of Potential Additional CCS Achieved[petroleum es]","Carbon Capture and Sequestration - Petroleum",[0,1],"Clean Electricity Standard"),
(False,"Electricity Sector Fraction of Potential Additional CCS Achieved[natural gas peaker es]","Carbon Capture and Sequestration - Natural Gas Peaker",[0,1],"Clean Electricity Standard"),
(True,"Electricity Sector Fraction of Potential Additional CCS Achieved[lignite es]","Carbon Capture and Sequestration - Gangue",[0,1],"Clean Electricity Standard"),
(False,"Electricity Sector Fraction of Potential Additional CCS Achieved[municipal solid waste es]","Carbon Capture and Sequestration - Municipal Solid Waste",[0,1],"Clean Electricity Standard"),
(True,"Renewable Portfolio Std Percentage","Clean Electricity Standard",[0,0.39],"Clean Electricity Standard"),
(False,"Percent Change in Electricity Exports","Change Electricity Exports",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[hard coal es]","Change Electricity Imports - Hard Coal",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[natural gas nonpeaker es]","Change Electricity Imports - Natural Gas Nonpeaker",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[nuclear es]","Change Electricity Imports - Nuclear",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[hydro es]","Change Electricity Imports - Hydro",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[onshore wind es]","Change Electricity Imports - Onshore Wind",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[solar PV es]","Change Electricity Imports - Solar PV",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[solar thermal es]","Change Electricity Imports - Solar Thermal",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[biomass es]","Change Electricity Imports - Biomass",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[geothermal es]","Change Electricity Imports - Geothermal",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[petroleum es]","Change Electricity Imports - Petroleum",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[natural gas peaker es]","Change Electricity Imports - Natural Gas Peaker",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[lignite es]","Change Electricity Imports - Gangue",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[offshore wind es]","Change Electricity Imports - Offshore Wind",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[crude oil es]","Change Electricity Imports - Crude Oil",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[heavy or residual fuel oil es]","Change Electricity Imports - Heavy or Residual Fuel Oil",[-0.5,1],"Electricity Imports and Exports"),
(False,"Percent Change in Electricity Imports[municipal solid waste es]","Change Electricity Imports - Municipal Solid Waste",[-0.5,1],"Electricity Imports and Exports"),
(False,"Fraction of Additional Demand Response Potential Achieved","Demand Response",[0,1],"Demand Response"),
(False,"Annual Additional Capacity Retired due to Early Retirement Policy[hard coal es]","Early Retirement of Power Plants - Hard Coal",[0,25000],"Early Retirement of Power Plants"),
(False,"Annual Additional Capacity Retired due to Early Retirement Policy[natural gas nonpeaker es]","Early Retirement of Power Plants - Natural Gas Nonpeaker",[0,25000],"Early Retirement of Power Plants"),
(False,"Annual Additional Capacity Retired due to Early Retirement Policy[nuclear es]","Early Retirement of Power Plants - Nuclear",[0,25000],"Early Retirement of Power Plants"),
(False,"Annual Additional Capacity Retired due to Early Retirement Policy[natural gas peaker es]","Early Retirement of Power Plants - Natural Gas Peaker",[0,25000],"Early Retirement of Power Plants"),
(False,"Annual Additional Capacity Retired due to Early Retirement Policy[lignite es]","Early Retirement of Power Plants - Gangue",[0,25000],"Early Retirement of Power Plants"),
(False,"Fraction of Additional Grid Battery Storage Potential Achieved","Grid-Scale Electricity Storage",[0,1],"Grid-Scale Electricity Storage"),
(False,"Percentage Increase in Transmission Capacity vs BAU","Increase Transmission",[0,1.13],"Increase Transmission"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[hard coal es]","Non BAU Capacity Retirement Schedule - Hard Coal",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[natural gas nonpeaker es]","Non BAU Capacity Retirement Schedule - Natural Gas Nonpeaker",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[nuclear es]","Non BAU Capacity Retirement Schedule - Nuclear",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[hydro es]","Non BAU Capacity Retirement Schedule - Hydro",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[onshore wind es]","Non BAU Capacity Retirement Schedule - Onshore Wind",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[solar PV es]","Non BAU Capacity Retirement Schedule - Solar PV",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[solar thermal es]","Non BAU Capacity Retirement Schedule - Solar Thermal",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[biomass es]","Non BAU Capacity Retirement Schedule - Biomass",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[geothermal es]","Non BAU Capacity Retirement Schedule - Geothermal",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[petroleum es]","Non BAU Capacity Retirement Schedule - Petroleum",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[natural gas peaker es]","Non BAU Capacity Retirement Schedule - Natural Gas Peaker",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[lignite es]","Non BAU Capacity Retirement Schedule - Gangue",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[offshore wind es]","Non BAU Capacity Retirement Schedule - Offshore Wind",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[crude oil es]","Non BAU Capacity Retirement Schedule - Crude Oil",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[heavy or residual fuel oil es]","Non BAU Capacity Retirement Schedule - Heavy or Residual Fuel Oil",[0,1],"Non BAU Capacity Retirement Schedule"),
(False,"Boolean Use Non BAU Capacity Retirement Schedule[municipal solid waste es]","Non BAU Capacity Retirement Schedule - Municipal Solid Waste",[0,1],"Non BAU Capacity Retirement Schedule"),
(True,"Boolean Use Non BAU Mandated Capacity Construction Schedule[hard coal es]","Non BAU Mandated Capacity Construction - Hard Coal",[0,1],"Non BAU Mandated Capacity Construction"),
(False,"Boolean Use Non BAU Mandated Capacity Construction Schedule[natural gas nonpeaker es]","Non BAU Mandated Capacity Construction - Natural Gas Nonpeaker",[0,1],"Non BAU Mandated Capacity Construction"),
(True,"Boolean Use Non BAU Mandated Capacity Construction Schedule[nuclear es]","Non BAU Mandated Capacity Construction - Nuclear",[0,1],"Non BAU Mandated Capacity Construction"),
(True,"Boolean Use Non BAU Mandated Capacity Construction Schedule[hydro es]","Non BAU Mandated Capacity Construction - Hydro",[0,1],"Non BAU Mandated Capacity Construction"),
(True,"Boolean Use Non BAU Mandated Capacity Construction Schedule[onshore wind es]","Non BAU Mandated Capacity Construction - Onshore Wind",[0,1],"Non BAU Mandated Capacity Construction"),
(True,"Boolean Use Non BAU Mandated Capacity Construction Schedule[solar PV es]","Non BAU Mandated Capacity Construction - Solar PV",[0,1],"Non BAU Mandated Capacity Construction"),
(False,"Boolean Use Non BAU Mandated Capacity Construction Schedule[solar thermal es]","Non BAU Mandated Capacity Construction - Solar Thermal",[0,1],"Non BAU Mandated Capacity Construction"),
(True,"Boolean Use Non BAU Mandated Capacity Construction Schedule[biomass es]","Non BAU Mandated Capacity Construction - Biomass",[0,1],"Non BAU Mandated Capacity Construction"),
(False,"Boolean Use Non BAU Mandated Capacity Construction Schedule[geothermal es]","Non BAU Mandated Capacity Construction - Geothermal",[0,1],"Non BAU Mandated Capacity Construction"),
(False,"Boolean Use Non BAU Mandated Capacity Construction Schedule[petroleum es]","Non BAU Mandated Capacity Construction - Petroleum",[0,1],"Non BAU Mandated Capacity Construction"),
(True,"Boolean Use Non BAU Mandated Capacity Construction Schedule[natural gas peaker es]","Non BAU Mandated Capacity Construction - Natural Gas Peaker",[0,1],"Non BAU Mandated Capacity Construction"),
(True,"Boolean Use Non BAU Mandated Capacity Construction Schedule[lignite es]","Non BAU Mandated Capacity Construction - Gangue",[0,1],"Non BAU Mandated Capacity Construction"),
(True,"Boolean Use Non BAU Mandated Capacity Construction Schedule[offshore wind es]","Non BAU Mandated Capacity Construction - Offshore Wind",[0,1],"Non BAU Mandated Capacity Construction"),
(False,"Boolean Use Non BAU Mandated Capacity Construction Schedule[crude oil es]","Non BAU Mandated Capacity Construction - Crude Oil",[0,1],"Non BAU Mandated Capacity Construction"),
(False,"Boolean Use Non BAU Mandated Capacity Construction Schedule[heavy or residual fuel oil es]","Non BAU Mandated Capacity Construction - Heavy or Residual Fuel Oil",[0,1],"Non BAU Mandated Capacity Construction"),
(True,"Boolean Use Non BAU Mandated Capacity Construction Schedule[municipal solid waste es]","Non BAU Mandated Capacity Construction - Municipal Solid Waste",[0,1],"Non BAU Mandated Capacity Construction"),
(False,"Boolean Use Non BAU RPS Qualifying Resource Definitions","Non BAU RPS Qualifying Resources",[0,1],"Non BAU RPS Qualifying Resources"),
(False,"Nuclear Capacity Lifetime Extension","Nuclear Plant Lifetime Extension",[0,20],"Nuclear Lifetime Extension"),
(False,"Percentage Reduction in Plant Downtime[natural gas nonpeaker es,preexisting retiring]","Reduce Plant Downtime - Natural Gas Nonpeaker Preexisting",[0,0.6],"Reduce Plant Downtime"),
(False,"Percentage Reduction in Plant Downtime[onshore wind es,newly built]","Reduce Plant Downtime - Onshore Wind New",[0,0.6],"Reduce Plant Downtime"),
(False,"Percentage Reduction in Plant Downtime[solar PV es,newly built]","Reduce Plant Downtime - Solar PV New",[0,0.6],"Reduce Plant Downtime"),
(False,"Percentage Reduction in Plant Downtime[offshore wind es,newly built]","Reduce Plant Downtime - Offshore Wind New",[0,0.6],"Reduce Plant Downtime"),
(False,"Percent Reduction in Soft Costs of Capacity Construction[onshore wind es]","Reduce Soft Costs - Onshore Wind",[0,0.9],"Reduce Soft Costs"),
(False,"Percent Reduction in Soft Costs of Capacity Construction[solar PV es]","Reduce Soft Costs - Solar PV",[0,0.9],"Reduce Soft Costs"),
(False,"Percent Reduction in Soft Costs of Capacity Construction[offshore wind es]","Reduce Soft Costs - Offshore Wind",[0,0.9],"Reduce Soft Costs"),
(False,"Percentage TnD Losses Avoided","Reduce Transmission n Distribution Losses",[0,0.4],"Reduce TnD Losses"),
(False,"Perc Subsidy for Elec Capacity Construction[nuclear es]","Subsidy for Capacity Construction - Nuclear",[0,0.95],"Subsidy for Capacity Construction"),
(False,"Perc Subsidy for Elec Capacity Construction[onshore wind es]","Subsidy for Capacity Construction - Onshore Wind",[0,0.95],"Subsidy for Capacity Construction"),
(False,"Perc Subsidy for Elec Capacity Construction[solar PV es]","Subsidy for Capacity Construction - Solar PV",[0,0.95],"Subsidy for Capacity Construction"),
(False,"Perc Subsidy for Elec Capacity Construction[solar thermal es]","Subsidy for Capacity Construction - Solar Thermal",[0,0.95],"Subsidy for Capacity Construction"),
(False,"Perc Subsidy for Elec Capacity Construction[biomass es]","Subsidy for Capacity Construction - Biomass",[0,0.95],"Subsidy for Capacity Construction"),
(False,"Perc Subsidy for Elec Capacity Construction[geothermal es]","Subsidy for Capacity Construction - Geothermal",[0,0.95],"Subsidy for Capacity Construction"),
(False,"Perc Subsidy for Elec Capacity Construction[offshore wind es]","Subsidy for Capacity Construction - Offshore Wind",[0,0.95],"Subsidy for Capacity Construction"),
(False,"Subsidy for Elec Production by Fuel[nuclear es,preexisting retiring]","Subsidy for Electricity Production - Nuclear Preexisting",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[nuclear es,newly built]","Subsidy for Electricity Production - Nuclear New",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[hydro es,preexisting retiring]","Subsidy for Electricity Production - Hydro Preexisting",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[hydro es,newly built]","Subsidy for Electricity Production - Hydro New",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[onshore wind es,preexisting retiring]","Subsidy for Electricity Production - Onshore Wind Preexisting",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[onshore wind es,newly built]","Subsidy for Electricity Production - Onshore Wind New",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[solar PV es,preexisting retiring]","Subsidy for Electricity Production - Solar PV Preexisting",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[solar PV es,newly built]","Subsidy for Electricity Production - Solar PV New",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[solar thermal es,preexisting retiring]","Subsidy for Electricity Production - Solar Thermal Preexisting",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[solar thermal es,newly built]","Subsidy for Electricity Production - Solar Thermal New",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[biomass es,preexisting retiring]","Subsidy for Electricity Production - Biomass Preexisting",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[biomass es,newly built]","Subsidy for Electricity Production - Biomass New",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[geothermal es,preexisting retiring]","Subsidy for Electricity Production - Geothermal Preexisting",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[geothermal es,newly built]","Subsidy for Electricity Production - Geothermal New",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[offshore wind es,preexisting retiring]","Subsidy for Electricity Production - Offshore Wind Preexisting",[0,60],"Subsidy for Electricity Production"),
(False,"Subsidy for Elec Production by Fuel[offshore wind es,newly built]","Subsidy for Electricity Production - Offshore Wind New",[0,60],"Subsidy for Electricity Production"),

# Industry Sector Policies
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[agriculture and forestry 01T03]","Buy In-Region Products - Agriculture and Forestry",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[coal mining 05]","Buy In-Region Products - Coal Mining",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[oil and gas extraction 06]","Buy In-Region Products - Oil and Gas Extraction",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[other mining and quarrying 07T08]","Buy In-Region Products - Other Mining and Quarrying",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[food beverage and tobacco 10T12]","Buy In-Region Products - Food Beverage and Tobacco",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[textiles apparel and leather 13T15]","Buy In-Region Products - Textiles Apparel and Leather",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[wood products 16]","Buy In-Region Products - Wood Products and Furniture",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[pulp paper and printing 17T18]","Buy In-Region Products - Pulp Paper and Printing",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[refined petroleum and coke 19]","Buy In-Region Products - Refined Petroleum and Coke",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[chemicals 20]","Buy In-Region Products - Chemicals",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[rubber and plastic products 22]","Buy In-Region Products - Rubber and Plastic Products",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[glass and glass products 231]","Buy In-Region Products - Specialized Equipment Manufacturing",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[cement and other nonmetallic minerals 239]","Buy In-Region Products - Cement Glass and Other Nonmetallic Minerals",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[iron and steel 241]","Buy In-Region Products - Iron and Steel",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[other metals 242]","Buy In-Region Products - Other Metals",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[metal products except machinery and vehicles 25]","Buy In-Region Products - Metal Products Except Machinery and Vehicles",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[computers and electronics 26]","Buy In-Region Products - Computers and Electronics",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[appliances and electrical equipment 27]","Buy In-Region Products - Appliances and Electrical Equipment",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[other machinery 28]","Buy In-Region Products - Other Machinery",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[road vehicles 29]","Buy In-Region Products - Road Vehicles",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[nonroad vehicles 30]","Buy In-Region Products - Nonroad Vehicles",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[other manufacturing 31T33]","Buy In-Region Products - Other Manufacturing",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[energy pipelines and gas processing 352T353]","Buy In-Region Products - Gas Production and Supply",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[water and waste 36T39]","Buy In-Region Products - Water and Waste",[0,0.5],"Buy In-Region Products"),
(False,"Fraction of Imported Industrial Outputs Shifted to In Region Suppliers[construction 41T43]","Buy In-Region Products - Construction",[0,0.5],"Buy In-Region Products"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[food beverage and tobacco 10T12,energy related emissions]","Carbon Capture and Sequestration - Food Beverage and Tobacco Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[textiles apparel and leather 13T15,energy related emissions]","Carbon Capture and Sequestration - Textiles Apparel and Leather Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[wood products 16,energy related emissions]","Carbon Capture and Sequestration - Wood Products and Furniture Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[pulp paper and printing 17T18,energy related emissions]","Carbon Capture and Sequestration - Pulp Paper and Printing Energy Related Emissions",[0,1],"Industry CCS"),
(True,"Industry Sector Fraction of Potential Additional CCS Achieved[refined petroleum and coke 19,energy related emissions]","Carbon Capture and Sequestration - Refined Petroleum and Coke Energy Related Emissions",[0,0.103371],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[refined petroleum and coke 19,process emissions]","Carbon Capture and Sequestration - Refined Petroleum and Coke Process Emissions",[0,1],"Industry CCS"),
(True,"Industry Sector Fraction of Potential Additional CCS Achieved[chemicals 20,energy related emissions]","Carbon Capture and Sequestration - Chemicals Energy Related Emissions",[0,0.103371],"Industry CCS"),
(True,"Industry Sector Fraction of Potential Additional CCS Achieved[chemicals 20,process emissions]","Carbon Capture and Sequestration - Chemicals Process Emissions",[0,0.452559],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[rubber and plastic products 22,energy related emissions]","Carbon Capture and Sequestration - Rubber and Plastic Products Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[glass and glass products 231,energy related emissions]","Carbon Capture and Sequestration - Specialized Equipment Manufacturing Energy Related Emissions",[0,1],"Industry CCS"),
(True,"Industry Sector Fraction of Potential Additional CCS Achieved[cement and other nonmetallic minerals 239,energy related emissions]","Carbon Capture and Sequestration - Cement Glass and Other Nonmetallic Minerals Energy Related Emissions",[0,0.175051],"Industry CCS"),
(True,"Industry Sector Fraction of Potential Additional CCS Achieved[cement and other nonmetallic minerals 239,process emissions]","Carbon Capture and Sequestration - Cement Glass and Other Nonmetallic Minerals Process Emissions",[0,0.552873],"Industry CCS"),
(True,"Industry Sector Fraction of Potential Additional CCS Achieved[iron and steel 241,energy related emissions]","Carbon Capture and Sequestration - Iron and Steel Energy Related Emissions",[0,0.652968],"Industry CCS"),
(True,"Industry Sector Fraction of Potential Additional CCS Achieved[iron and steel 241,process emissions]","Carbon Capture and Sequestration - Iron and Steel Process Emissions",[0,0.0431878],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[other metals 242,energy related emissions]","Carbon Capture and Sequestration - Other Metals Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[metal products except machinery and vehicles 25,energy related emissions]","Carbon Capture and Sequestration - Metal Products Except Machinery and Vehicles Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[computers and electronics 26,energy related emissions]","Carbon Capture and Sequestration - Computers and Electronics Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[appliances and electrical equipment 27,energy related emissions]","Carbon Capture and Sequestration - Appliances and Electrical Equipment Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[other machinery 28,energy related emissions]","Carbon Capture and Sequestration - Other Machinery Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[road vehicles 29,energy related emissions]","Carbon Capture and Sequestration - Road Vehicles Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[nonroad vehicles 30,energy related emissions]","Carbon Capture and Sequestration - Nonroad Vehicles Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[other manufacturing 31T33,energy related emissions]","Carbon Capture and Sequestration - Other Manufacturing Energy Related Emissions",[0,1],"Industry CCS"),
(False,"Industry Sector Fraction of Potential Additional CCS Achieved[energy pipelines and gas processing 352T353,energy related emissions]","Carbon Capture and Sequestration - Gas Production and Supply Energy Related Emissions",[0,1],"Industry CCS"),
(True,"Industry Sector Fraction of Potential Additional CCS Achieved[energy pipelines and gas processing 352T353,process emissions]","Carbon Capture and Sequestration - Gas Production and Supply Process Emissions",[0,0.191474],"Industry CCS"),
(False,"Fraction of Cement Measures Achieved","Cement Clinker Substitution",[0,1],"Cement Clinker Substitution"),
(True,"Fraction of Potential Cogeneration and Waste Heat Recovery Adopted","Cogeneration and Waste Heat Recovery",[0,1],"Cogeneration and Waste Heat Recovery"),
(False,"Fraction of Energy Savings from Early Facility Retirement Achieved","Early Retirement of Industrial Facilities",[0,1],"Early Retirement of Industrial Facilities"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[agriculture and forestry 01T03,electricity if]","Electrification + Hydrogen (Med n High Temp) - Agriculture and Forestry Shift to Electricity",[0,0.6],"Electrification + Hydrogen"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[agriculture and forestry 01T03,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Agriculture and Forestry Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[coal mining 05,electricity if]","Electrification + Hydrogen (Med n High Temp) - Coal Mining Shift to Electricity",[0,0.6],"Electrification + Hydrogen"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[coal mining 05,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Coal Mining Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[oil and gas extraction 06,electricity if]","Electrification + Hydrogen (Med n High Temp) - Oil and Gas Extraction Shift to Electricity",[0,0.6],"Electrification + Hydrogen"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[oil and gas extraction 06,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Oil and Gas Extraction Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[other mining and quarrying 07T08,electricity if]","Electrification + Hydrogen (Med n High Temp) - Other Mining and Quarrying Shift to Electricity",[0,0.6],"Electrification + Hydrogen"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[other mining and quarrying 07T08,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Other Mining and Quarrying Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen1"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[food beverage and tobacco 10T12,electricity if]","Electrification + Hydrogen (Med n High Temp) - Food Beverage and Tobacco Shift to Electricity",[0,0.6],"Electrification + Hydrogen1"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[food beverage and tobacco 10T12,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Food Beverage and Tobacco Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen1"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[textiles apparel and leather 13T15,electricity if]","Electrification + Hydrogen (Med n High Temp) - Textiles Apparel and Leather Shift to Electricity",[0,0.6],"Electrification + Hydrogen1"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[textiles apparel and leather 13T15,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Textiles Apparel and Leather Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen1"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[wood products 16,electricity if]","Electrification + Hydrogen (Med n High Temp) - Wood Products and Furniture Shift to Electricity",[0,0.6],"Electrification + Hydrogen1"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[wood products 16,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Wood Products and Furniture Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen1"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[pulp paper and printing 17T18,electricity if]","Electrification + Hydrogen (Med n High Temp) - Pulp Paper and Printing Shift to Electricity",[0,0.6],"Electrification + Hydrogen2"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[pulp paper and printing 17T18,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Pulp Paper and Printing Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen2"),
(False,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[refined petroleum and coke 19,electricity if]","Electrification + Hydrogen (Med n High Temp) - Refined Petroleum and Coke Shift to Electricity",[0,0.3],"Electrification + Hydrogen2"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[refined petroleum and coke 19,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Refined Petroleum and Coke Shift to Hydrogen",[0,0.28],"Electrification + Hydrogen2"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[chemicals 20,electricity if]","Electrification + Hydrogen (Med n High Temp) - Chemicals Shift to Electricity",[0,0.6],"Electrification + Hydrogen2"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[chemicals 20,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Chemicals Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen2"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[rubber and plastic products 22,electricity if]","Electrification + Hydrogen (Med n High Temp) - Rubber and Plastic Products Shift to Electricity",[0,0.6],"Electrification + Hydrogen2"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[rubber and plastic products 22,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Rubber and Plastic Products Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen3"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[glass and glass products 231,electricity if]","Electrification + Hydrogen (Med n High Temp) - Specialized Equipment Manufacturing Shift to Electricity",[0,0.6],"Electrification + Hydrogen3"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[glass and glass products 231,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Specialized Equipment Manufacturing Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen3"),
(False,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[cement and other nonmetallic minerals 239,electricity if]","Electrification + Hydrogen (Med n High Temp) - Cement Glass and Other Nonmetallic Minerals Shift to Electricity",[0,0.3],"Electrification + Hydrogen3"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[cement and other nonmetallic minerals 239,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Cement Glass and Other Nonmetallic Minerals Shift to Hydrogen",[0,0.35],"Electrification + Hydrogen3"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[iron and steel 241,electricity if]","Electrification + Hydrogen (Med n High Temp) - Iron and Steel Shift to Electricity",[0,0.1],"Electrification + Hydrogen3"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[iron and steel 241,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Iron and Steel Shift to Hydrogen",[0,0.13],"Electrification + Hydrogen3"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[other metals 242,electricity if]","Electrification + Hydrogen (Med n High Temp) - Other Metals Shift to Electricity",[0,0.6],"Electrification + Hydrogen4"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[other metals 242,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Other Metals Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen4"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[metal products except machinery and vehicles 25,electricity if]","Electrification + Hydrogen (Med n High Temp) - Metal Products Except Machinery and Vehicles Shift to Electricity",[0,0.6],"Electrification + Hydrogen4"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[metal products except machinery and vehicles 25,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Metal Products Except Machinery and Vehicles Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen4"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[computers and electronics 26,electricity if]","Electrification + Hydrogen (Med n High Temp) - Computers and Electronics Shift to Electricity",[0,0.6],"Electrification + Hydrogen4"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[computers and electronics 26,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Computers and Electronics Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen4"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[appliances and electrical equipment 27,electricity if]","Electrification + Hydrogen (Med n High Temp) - Appliances and Electrical Equipment Shift to Electricity",[0,0.6],"Electrification + Hydrogen4"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[appliances and electrical equipment 27,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Appliances and Electrical Equipment Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen5"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[other machinery 28,electricity if]","Electrification + Hydrogen (Med n High Temp) - Other Machinery Shift to Electricity",[0,0.6],"Electrification + Hydrogen5"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[other machinery 28,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Other Machinery Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen5"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[road vehicles 29,electricity if]","Electrification + Hydrogen (Med n High Temp) - Road Vehicles Shift to Electricity",[0,0.6],"Electrification + Hydrogen5"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[road vehicles 29,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Road Vehicles Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen5"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[nonroad vehicles 30,electricity if]","Electrification + Hydrogen (Med n High Temp) - Nonroad Vehicles Shift to Electricity",[0,0.6],"Electrification + Hydrogen5"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[nonroad vehicles 30,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Nonroad Vehicles Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen5"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[other manufacturing 31T33,electricity if]","Electrification + Hydrogen (Med n High Temp) - Other Manufacturing Shift to Electricity",[0,0.6],"Electrification + Hydrogen6"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[other manufacturing 31T33,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Other Manufacturing Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen6"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[energy pipelines and gas processing 352T353,electricity if]","Electrification + Hydrogen (Med n High Temp) - Gas Production and Supply Shift to Electricity",[0,0.6],"Electrification + Hydrogen6"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[energy pipelines and gas processing 352T353,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Gas Production and Supply Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen6"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[water and waste 36T39,electricity if]","Electrification + Hydrogen (Med n High Temp) - Water and Waste Shift to Electricity",[0,0.6],"Electrification + Hydrogen6"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[water and waste 36T39,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Water and Waste Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen6"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[construction 41T43,electricity if]","Electrification + Hydrogen (Med n High Temp) - Construction Shift to Electricity",[0,0.6],"Electrification + Hydrogen6"),
(True,"Fraction of Med and High Temp Industrial Heat Shifted to Other Fuels[construction 41T43,hydrogen if]","Electrification + Hydrogen (Med n High Temp) - Construction Shift to Hydrogen",[0,0.4],"Electrification + Hydrogen6"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[agriculture and forestry 01T03]","Electrification (Low Temp) - Agriculture and Forestry",[0,1],"Electrification + Hydrogen - Low"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[coal mining 05]","Electrification (Low Temp) - Coal Mining",[0,1],"Electrification + Hydrogen - Low"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[oil and gas extraction 06]","Electrification (Low Temp) - Oil and Gas Extraction",[0,1],"Electrification + Hydrogen - Low"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[other mining and quarrying 07T08]","Electrification (Low Temp) - Other Mining and Quarrying",[0,1],"Electrification + Hydrogen - Low"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[food beverage and tobacco 10T12]","Electrification (Low Temp) - Food Beverage and Tobacco",[0,1],"Electrification + Hydrogen - Low"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[textiles apparel and leather 13T15]","Electrification (Low Temp) - Textiles Apparel and Leather",[0,1],"Electrification + Hydrogen - Low"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[wood products 16]","Electrification (Low Temp) - Wood Products and Furniture",[0,1],"Electrification + Hydrogen - Low"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[pulp paper and printing 17T18]","Electrification (Low Temp) - Pulp Paper and Printing",[0,1],"Electrification + Hydrogen - Low1"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[refined petroleum and coke 19]","Electrification (Low Temp) - Refined Petroleum and Coke",[0,1],"Electrification + Hydrogen - Low1"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[chemicals 20]","Electrification (Low Temp) - Chemicals",[0,1],"Electrification + Hydrogen - Low"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[rubber and plastic products 22]","Electrification (Low Temp) - Rubber and Plastic Products",[0,1],"Electrification + Hydrogen - Low1"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[glass and glass products 231]","Electrification (Low Temp) - Specialized Equipment Manufacturing",[0,1],"Electrification + Hydrogen - Low1"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[cement and other nonmetallic minerals 239]","Electrification (Low Temp) - Cement Glass and Other Nonmetallic Minerals",[0,1],"Electrification + Hydrogen - Low1"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[iron and steel 241]","Electrification (Low Temp) - Iron and Steel",[0,1],"Electrification + Hydrogen - Low1"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[other metals 242]","Electrification (Low Temp) - Other Metals",[0,1],"Electrification + Hydrogen - Low1"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[metal products except machinery and vehicles 25]","Electrification (Low Temp) - Metal Products Except Machinery and Vehicles",[0,1],"Electrification + Hydrogen - Low2"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[computers and electronics 26]","Electrification (Low Temp) - Computers and Electronics",[0,1],"Electrification + Hydrogen - Low2"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[appliances and electrical equipment 27]","Electrification (Low Temp) - Appliances and Electrical Equipment",[0,1],"Electrification + Hydrogen - Low2"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[other machinery 28]","Electrification (Low Temp) - Other Machinery",[0,1],"Electrification + Hydrogen - Low2"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[road vehicles 29]","Electrification (Low Temp) - Road Vehicles",[0,1],"Electrification + Hydrogen - Low2"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[nonroad vehicles 30]","Electrification (Low Temp) - Nonroad Vehicles",[0,1],"Electrification + Hydrogen - Low2"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[other manufacturing 31T33]","Electrification (Low Temp) - Other Manufacturing",[0,1],"Electrification + Hydrogen - Low2"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[energy pipelines and gas processing 352T353]","Electrification (Low Temp) - Gas Production and Supply",[0,1],"Electrification + Hydrogen - Low3"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[water and waste 36T39]","Electrification (Low Temp) - Water and Waste",[0,1],"Electrification + Hydrogen - Low3"),
(True,"Fraction of Low Temp Industrial Heat Shifted to Other Fuels[construction 41T43]","Electrification (Low Temp) - Construction",[0,1],"Electrification + Hydrogen - Low3"),
(False,"Fraction of F Gas Substitution Achieved","F-Gas Substitution",[0,1],"F-gas Measures"),
(False,"Fraction of F Gas Destruction Achieved","F-Gas Destruction",[0,1],"F-gas Measures"),
(False,"Fraction of F Gas Recovery Achieved","F-Gas Recovery",[0,1],"F-gas Measures"),
(False,"Fraction of F Gas Inspct Maint Retrofit Achieved[chemicals 20]","F-Gas Eqpt. Maintenance n Retrofits - Chemicals",[0,1],"F-gas Measures"),
(False,"Fraction of F Gas Inspct Maint Retrofit Achieved[other metals 242]","F-Gas Eqpt. Maintenance n Retrofits - Other Metals",[0,1],"F-gas Measures"),
(False,"Fraction of Installation and System Integration Issues Remedied","Improved System Design",[0,1],"Improved System Design"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture and forestry 01T03,electricity if]","Industry Energy Efficiency Standards - Agriculture and Forestry Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture and forestry 01T03,hard coal if]","Industry Energy Efficiency Standards - Agriculture and Forestry Coal Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture and forestry 01T03,natural gas if]","Industry Energy Efficiency Standards - Agriculture and Forestry Natural Gas Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture and forestry 01T03,biomass if]","Industry Energy Efficiency Standards - Agriculture and Forestry Biomass Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture and forestry 01T03,petroleum diesel if]","Industry Energy Efficiency Standards - Agriculture and Forestry Petroleum Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture and forestry 01T03,heat if]","Industry Energy Efficiency Standards - Agriculture and Forestry Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture and forestry 01T03,crude oil if]","Industry Energy Efficiency Standards - Agriculture and Forestry Crude Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture and forestry 01T03,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Agriculture and Forestry Heavy or Residual Fuel Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture and forestry 01T03,LPG propane or butane if]","Industry Energy Efficiency Standards - Agriculture and Forestry LPG Propane or Butane Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture and forestry 01T03,hydrogen if]","Industry Energy Efficiency Standards - Agriculture and Forestry Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[coal mining 05,electricity if]","Industry Energy Efficiency Standards - Coal Mining Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[coal mining 05,hard coal if]","Industry Energy Efficiency Standards - Coal Mining Coal Use",[0,0.0374],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[coal mining 05,natural gas if]","Industry Energy Efficiency Standards - Coal Mining Natural Gas Use",[0,0.0374],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[coal mining 05,biomass if]","Industry Energy Efficiency Standards - Coal Mining Biomass Use",[0,0.0374],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[coal mining 05,petroleum diesel if]","Industry Energy Efficiency Standards - Coal Mining Petroleum Use",[0,0.0374],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[coal mining 05,heat if]","Industry Energy Efficiency Standards - Coal Mining Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[coal mining 05,crude oil if]","Industry Energy Efficiency Standards - Coal Mining Crude Oil Use",[0,0.0374],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[coal mining 05,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Coal Mining Heavy or Residual Fuel Oil Use",[0,0.0374],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[coal mining 05,LPG propane or butane if]","Industry Energy Efficiency Standards - Coal Mining LPG Propane or Butane Use",[0,0.0374],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[coal mining 05,hydrogen if]","Industry Energy Efficiency Standards - Coal Mining Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[oil and gas extraction 06,electricity if]","Industry Energy Efficiency Standards - Oil and Gas Extraction Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[oil and gas extraction 06,hard coal if]","Industry Energy Efficiency Standards - Oil and Gas Extraction Coal Use",[0,0.1487],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[oil and gas extraction 06,natural gas if]","Industry Energy Efficiency Standards - Oil and Gas Extraction Natural Gas Use",[0,0.1487],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[oil and gas extraction 06,biomass if]","Industry Energy Efficiency Standards - Oil and Gas Extraction Biomass Use",[0,0.1487],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[oil and gas extraction 06,petroleum diesel if]","Industry Energy Efficiency Standards - Oil and Gas Extraction Petroleum Use",[0,0.1487],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[oil and gas extraction 06,heat if]","Industry Energy Efficiency Standards - Oil and Gas Extraction Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[oil and gas extraction 06,crude oil if]","Industry Energy Efficiency Standards - Oil and Gas Extraction Crude Oil Use",[0,0.1487],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[oil and gas extraction 06,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Oil and Gas Extraction Heavy or Residual Fuel Oil Use",[0,0.1487],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[oil and gas extraction 06,LPG propane or butane if]","Industry Energy Efficiency Standards - Oil and Gas Extraction LPG Propane or Butane Use",[0,0.1487],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[oil and gas extraction 06,hydrogen if]","Industry Energy Efficiency Standards - Oil and Gas Extraction Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other mining and quarrying 07T08,electricity if]","Industry Energy Efficiency Standards - Other Mining and Quarrying Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other mining and quarrying 07T08,hard coal if]","Industry Energy Efficiency Standards - Other Mining and Quarrying Coal Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other mining and quarrying 07T08,natural gas if]","Industry Energy Efficiency Standards - Other Mining and Quarrying Natural Gas Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other mining and quarrying 07T08,biomass if]","Industry Energy Efficiency Standards - Other Mining and Quarrying Biomass Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other mining and quarrying 07T08,petroleum diesel if]","Industry Energy Efficiency Standards - Other Mining and Quarrying Petroleum Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other mining and quarrying 07T08,heat if]","Industry Energy Efficiency Standards - Other Mining and Quarrying Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other mining and quarrying 07T08,crude oil if]","Industry Energy Efficiency Standards - Other Mining and Quarrying Crude Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other mining and quarrying 07T08,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Other Mining and Quarrying Heavy or Residual Fuel Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other mining and quarrying 07T08,LPG propane or butane if]","Industry Energy Efficiency Standards - Other Mining and Quarrying LPG Propane or Butane Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other mining and quarrying 07T08,hydrogen if]","Industry Energy Efficiency Standards - Other Mining and Quarrying Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[food beverage and tobacco 10T12,electricity if]","Industry Energy Efficiency Standards - Food Beverage and Tobacco Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[food beverage and tobacco 10T12,hard coal if]","Industry Energy Efficiency Standards - Food Beverage and Tobacco Coal Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[food beverage and tobacco 10T12,natural gas if]","Industry Energy Efficiency Standards - Food Beverage and Tobacco Natural Gas Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[food beverage and tobacco 10T12,biomass if]","Industry Energy Efficiency Standards - Food Beverage and Tobacco Biomass Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[food beverage and tobacco 10T12,petroleum diesel if]","Industry Energy Efficiency Standards - Food Beverage and Tobacco Petroleum Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[food beverage and tobacco 10T12,heat if]","Industry Energy Efficiency Standards - Food Beverage and Tobacco Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[food beverage and tobacco 10T12,crude oil if]","Industry Energy Efficiency Standards - Food Beverage and Tobacco Crude Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[food beverage and tobacco 10T12,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Food Beverage and Tobacco Heavy or Residual Fuel Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[food beverage and tobacco 10T12,LPG propane or butane if]","Industry Energy Efficiency Standards - Food Beverage and Tobacco LPG Propane or Butane Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[food beverage and tobacco 10T12,hydrogen if]","Industry Energy Efficiency Standards - Food Beverage and Tobacco Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[textiles apparel and leather 13T15,electricity if]","Industry Energy Efficiency Standards - Textiles Apparel and Leather Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[textiles apparel and leather 13T15,hard coal if]","Industry Energy Efficiency Standards - Textiles Apparel and Leather Coal Use",[0,0.1247],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[textiles apparel and leather 13T15,natural gas if]","Industry Energy Efficiency Standards - Textiles Apparel and Leather Natural Gas Use",[0,0.1247],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[textiles apparel and leather 13T15,biomass if]","Industry Energy Efficiency Standards - Textiles Apparel and Leather Biomass Use",[0,0.1247],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[textiles apparel and leather 13T15,petroleum diesel if]","Industry Energy Efficiency Standards - Textiles Apparel and Leather Petroleum Use",[0,0.1247],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[textiles apparel and leather 13T15,heat if]","Industry Energy Efficiency Standards - Textiles Apparel and Leather Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[textiles apparel and leather 13T15,crude oil if]","Industry Energy Efficiency Standards - Textiles Apparel and Leather Crude Oil Use",[0,0.1247],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[textiles apparel and leather 13T15,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Textiles Apparel and Leather Heavy or Residual Fuel Oil Use",[0,0.1247],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[textiles apparel and leather 13T15,LPG propane or butane if]","Industry Energy Efficiency Standards - Textiles Apparel and Leather LPG Propane or Butane Use",[0,0.1247],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[textiles apparel and leather 13T15,hydrogen if]","Industry Energy Efficiency Standards - Textiles Apparel and Leather Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[wood products 16,electricity if]","Industry Energy Efficiency Standards - Wood Products and Furniture Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[wood products 16,hard coal if]","Industry Energy Efficiency Standards - Wood Products and Furniture Coal Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[wood products 16,natural gas if]","Industry Energy Efficiency Standards - Wood Products and Furniture Natural Gas Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[wood products 16,biomass if]","Industry Energy Efficiency Standards - Wood Products and Furniture Biomass Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[wood products 16,petroleum diesel if]","Industry Energy Efficiency Standards - Wood Products and Furniture Petroleum Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[wood products 16,heat if]","Industry Energy Efficiency Standards - Wood Products and Furniture Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[wood products 16,crude oil if]","Industry Energy Efficiency Standards - Wood Products and Furniture Crude Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[wood products 16,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Wood Products and Furniture Heavy or Residual Fuel Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[wood products 16,LPG propane or butane if]","Industry Energy Efficiency Standards - Wood Products and Furniture LPG Propane or Butane Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[wood products 16,hydrogen if]","Industry Energy Efficiency Standards - Wood Products and Furniture Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[pulp paper and printing 17T18,electricity if]","Industry Energy Efficiency Standards - Pulp Paper and Printing Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[pulp paper and printing 17T18,hard coal if]","Industry Energy Efficiency Standards - Pulp Paper and Printing Coal Use",[0,0.1266],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[pulp paper and printing 17T18,natural gas if]","Industry Energy Efficiency Standards - Pulp Paper and Printing Natural Gas Use",[0,0.1266],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[pulp paper and printing 17T18,biomass if]","Industry Energy Efficiency Standards - Pulp Paper and Printing Biomass Use",[0,0.1266],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[pulp paper and printing 17T18,petroleum diesel if]","Industry Energy Efficiency Standards - Pulp Paper and Printing Petroleum Use",[0,0.1266],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[pulp paper and printing 17T18,heat if]","Industry Energy Efficiency Standards - Pulp Paper and Printing Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[pulp paper and printing 17T18,crude oil if]","Industry Energy Efficiency Standards - Pulp Paper and Printing Crude Oil Use",[0,0.1266],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[pulp paper and printing 17T18,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Pulp Paper and Printing Heavy or Residual Fuel Oil Use",[0,0.1266],"Industry Energy Efficiency Standards"),
(True"Percentage Improvement in Eqpt Efficiency Standards above BAU[pulp paper and printing 17T18,LPG propane or butane if]","Industry Energy Efficiency Standards - Pulp Paper and Printing LPG Propane or Butane Use",[0,0.1266],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[pulp paper and printing 17T18,hydrogen if]","Industry Energy Efficiency Standards - Pulp Paper and Printing Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[refined petroleum and coke 19,electricity if]","Industry Energy Efficiency Standards - Refined Petroleum and Coke Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[refined petroleum and coke 19,hard coal if]","Industry Energy Efficiency Standards - Refined Petroleum and Coke Coal Use",[0,0.1549],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[refined petroleum and coke 19,natural gas if]","Industry Energy Efficiency Standards - Refined Petroleum and Coke Natural Gas Use",[0,0.1549],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[refined petroleum and coke 19,biomass if]","Industry Energy Efficiency Standards - Refined Petroleum and Coke Biomass Use",[0,0.1549],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[refined petroleum and coke 19,petroleum diesel if]","Industry Energy Efficiency Standards - Refined Petroleum and Coke Petroleum Use",[0,0.1549],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[refined petroleum and coke 19,heat if]","Industry Energy Efficiency Standards - Refined Petroleum and Coke Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[refined petroleum and coke 19,crude oil if]","Industry Energy Efficiency Standards - Refined Petroleum and Coke Crude Oil Use",[0,0.1549],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[refined petroleum and coke 19,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Refined Petroleum and Coke Heavy or Residual Fuel Oil Use",[0,0.1549],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[refined petroleum and coke 19,LPG propane or butane if]","Industry Energy Efficiency Standards - Refined Petroleum and Coke LPG Propane or Butane Use",[0,0.1549],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[refined petroleum and coke 19,hydrogen if]","Industry Energy Efficiency Standards - Refined Petroleum and Coke Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals 20,electricity if]","Industry Energy Efficiency Standards - Chemicals Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals 20,hard coal if]","Industry Energy Efficiency Standards - Chemicals Coal Use",[0,0.0838],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals 20,natural gas if]","Industry Energy Efficiency Standards - Chemicals Natural Gas Use",[0,0.0838],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals 20,biomass if]","Industry Energy Efficiency Standards - Chemicals Biomass Use",[0,0.0838],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals 20,petroleum diesel if]","Industry Energy Efficiency Standards - Chemicals Petroleum Use",[0,0.0838],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals 20,heat if]","Industry Energy Efficiency Standards - Chemicals Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals 20,crude oil if]","Industry Energy Efficiency Standards - Chemicals Crude Oil Use",[0,0.0838],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals 20,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Chemicals Heavy or Residual Fuel Oil Use",[0,0.838],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals 20,LPG propane or butane if]","Industry Energy Efficiency Standards - Chemicals LPG Propane or Butane Use",[0,0.0838],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals 20,hydrogen if]","Industry Energy Efficiency Standards - Chemicals Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[rubber and plastic products 22,electricity if]","Industry Energy Efficiency Standards - Rubber and Plastic Products Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[rubber and plastic products 22,hard coal if]","Industry Energy Efficiency Standards - Rubber and Plastic Products Coal Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[rubber and plastic products 22,natural gas if]","Industry Energy Efficiency Standards - Rubber and Plastic Products Natural Gas Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[rubber and plastic products 22,biomass if]","Industry Energy Efficiency Standards - Rubber and Plastic Products Biomass Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[rubber and plastic products 22,petroleum diesel if]","Industry Energy Efficiency Standards - Rubber and Plastic Products Petroleum Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[rubber and plastic products 22,heat if]","Industry Energy Efficiency Standards - Rubber and Plastic Products Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[rubber and plastic products 22,crude oil if]","Industry Energy Efficiency Standards - Rubber and Plastic Products Crude Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[rubber and plastic products 22,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Rubber and Plastic Products Heavy or Residual Fuel Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[rubber and plastic products 22,LPG propane or butane if]","Industry Energy Efficiency Standards - Rubber and Plastic Products LPG Propane or Butane Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[rubber and plastic products 22,hydrogen if]","Industry Energy Efficiency Standards - Rubber and Plastic Products Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[glass and glass products 231,electricity if]","Industry Energy Efficiency Standards - Specialized Equipment Manufacturing Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[glass and glass products 231,hard coal if]","Industry Energy Efficiency Standards - Specialized Equipment Manufacturing Coal Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[glass and glass products 231,natural gas if]","Industry Energy Efficiency Standards - Specialized Equipment Manufacturing Natural Gas Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[glass and glass products 231,biomass if]","Industry Energy Efficiency Standards - Specialized Equipment Manufacturing Biomass Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[glass and glass products 231,petroleum diesel if]","Industry Energy Efficiency Standards - Specialized Equipment Manufacturing Petroleum Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[glass and glass products 231,heat if]","Industry Energy Efficiency Standards - Specialized Equipment Manufacturing Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[glass and glass products 231,crude oil if]","Industry Energy Efficiency Standards - Specialized Equipment Manufacturing Crude Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[glass and glass products 231,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Specialized Equipment Manufacturing Heavy or Residual Fuel Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[glass and glass products 231,LPG propane or butane if]","Industry Energy Efficiency Standards - Specialized Equipment Manufacturing LPG Propane or Butane Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[glass and glass products 231,hydrogen if]","Industry Energy Efficiency Standards - Specialized Equipment Manufacturing Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other nonmetallic minerals 239,electricity if]","Industry Energy Efficiency Standards - Cement Glass and Other Nonmetallic Minerals Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other nonmetallic minerals 239,hard coal if]","Industry Energy Efficiency Standards - Cement Glass and Other Nonmetallic Minerals Coal Use",[0,0.4328],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other nonmetallic minerals 239,natural gas if]","Industry Energy Efficiency Standards - Cement Glass and Other Nonmetallic Minerals Natural Gas Use",[0,0.4328],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other nonmetallic minerals 239,biomass if]","Industry Energy Efficiency Standards - Cement Glass and Other Nonmetallic Minerals Biomass Use",[0,0.4328],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other nonmetallic minerals 239,petroleum diesel if]","Industry Energy Efficiency Standards - Cement Glass and Other Nonmetallic Minerals Petroleum Use",[0,0.4328],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other nonmetallic minerals 239,heat if]","Industry Energy Efficiency Standards - Cement Glass and Other Nonmetallic Minerals Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other nonmetallic minerals 239,crude oil if]","Industry Energy Efficiency Standards - Cement Glass and Other Nonmetallic Minerals Crude Oil Use",[0,0.4328],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other nonmetallic minerals 239,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Cement Glass and Other Nonmetallic Minerals Heavy or Residual Fuel Oil Use",[0,0.4328],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other nonmetallic minerals 239,LPG propane or butane if]","Industry Energy Efficiency Standards - Cement Glass and Other Nonmetallic Minerals LPG Propane or Butane Use",[0,0.4328],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other nonmetallic minerals 239,hydrogen if]","Industry Energy Efficiency Standards - Cement Glass and Other Nonmetallic Minerals Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel 241,electricity if]","Industry Energy Efficiency Standards - Iron and Steel Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel 241,hard coal if]","Industry Energy Efficiency Standards - Iron and Steel Coal Use",[0,0.4057],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel 241,natural gas if]","Industry Energy Efficiency Standards - Iron and Steel Natural Gas Use",[0,0.4057],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel 241,biomass if]","Industry Energy Efficiency Standards - Iron and Steel Biomass Use",[0,0.4057],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel 241,petroleum diesel if]","Industry Energy Efficiency Standards - Iron and Steel Petroleum Use",[0,0.4057],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel 241,heat if]","Industry Energy Efficiency Standards - Iron and Steel Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel 241,crude oil if]","Industry Energy Efficiency Standards - Iron and Steel Crude Oil Use",[0,0.4057],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel 241,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Iron and Steel Heavy or Residual Fuel Oil Use",[0,0.4057],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel 241,LPG propane or butane if]","Industry Energy Efficiency Standards - Iron and Steel LPG Propane or Butane Use",[0,0.4057],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel 241,hydrogen if]","Industry Energy Efficiency Standards - Iron and Steel Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other metals 242,electricity if]","Industry Energy Efficiency Standards - Other Metals Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other metals 242,hard coal if]","Industry Energy Efficiency Standards - Other Metals Coal Use",[0,0.0637],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other metals 242,natural gas if]","Industry Energy Efficiency Standards - Other Metals Natural Gas Use",[0,0.0637],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other metals 242,biomass if]","Industry Energy Efficiency Standards - Other Metals Biomass Use",[0,0.0637],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other metals 242,petroleum diesel if]","Industry Energy Efficiency Standards - Other Metals Petroleum Use",[0,0.0637],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other metals 242,heat if]","Industry Energy Efficiency Standards - Other Metals Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other metals 242,crude oil if]","Industry Energy Efficiency Standards - Other Metals Crude Oil Use",[0,0.0637],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other metals 242,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Other Metals Heavy or Residual Fuel Oil Use",[0,0.0637],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other metals 242,LPG propane or butane if]","Industry Energy Efficiency Standards - Other Metals LPG Propane or Butane Use",[0,0.0637],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other metals 242,hydrogen if]","Industry Energy Efficiency Standards - Other Metals Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[metal products except machinery and vehicles 25,electricity if]","Industry Energy Efficiency Standards - Metal Products Except Machinery and Vehicles Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[metal products except machinery and vehicles 25,hard coal if]","Industry Energy Efficiency Standards - Metal Products Except Machinery and Vehicles Coal Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[metal products except machinery and vehicles 25,natural gas if]","Industry Energy Efficiency Standards - Metal Products Except Machinery and Vehicles Natural Gas Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[metal products except machinery and vehicles 25,biomass if]","Industry Energy Efficiency Standards - Metal Products Except Machinery and Vehicles Biomass Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[metal products except machinery and vehicles 25,petroleum diesel if]","Industry Energy Efficiency Standards - Metal Products Except Machinery and Vehicles Petroleum Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[metal products except machinery and vehicles 25,heat if]","Industry Energy Efficiency Standards - Metal Products Except Machinery and Vehicles Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[metal products except machinery and vehicles 25,crude oil if]","Industry Energy Efficiency Standards - Metal Products Except Machinery and Vehicles Crude Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[metal products except machinery and vehicles 25,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Metal Products Except Machinery and Vehicles Heavy or Residual Fuel Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[metal products except machinery and vehicles 25,LPG propane or butane if]","Industry Energy Efficiency Standards - Metal Products Except Machinery and Vehicles LPG Propane or Butane Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[metal products except machinery and vehicles 25,hydrogen if]","Industry Energy Efficiency Standards - Metal Products Except Machinery and Vehicles Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[computers and electronics 26,electricity if]","Industry Energy Efficiency Standards - Computers and Electronics Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[computers and electronics 26,hard coal if]","Industry Energy Efficiency Standards - Computers and Electronics Coal Use",[0,0.0185],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[computers and electronics 26,natural gas if]","Industry Energy Efficiency Standards - Computers and Electronics Natural Gas Use",[0,0.0185],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[computers and electronics 26,biomass if]","Industry Energy Efficiency Standards - Computers and Electronics Biomass Use",[0,0.0185],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[computers and electronics 26,petroleum diesel if]","Industry Energy Efficiency Standards - Computers and Electronics Petroleum Use",[0,0.0185],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[computers and electronics 26,heat if]","Industry Energy Efficiency Standards - Computers and Electronics Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[computers and electronics 26,crude oil if]","Industry Energy Efficiency Standards - Computers and Electronics Crude Oil Use",[0,0.0185],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[computers and electronics 26,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Computers and Electronics Heavy or Residual Fuel Oil Use",[0,0.0185],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[computers and electronics 26,LPG propane or butane if]","Industry Energy Efficiency Standards - Computers and Electronics LPG Propane or Butane Use",[0,0.0185],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[computers and electronics 26,hydrogen if]","Industry Energy Efficiency Standards - Computers and Electronics Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[appliances and electrical equipment 27,electricity if]","Industry Energy Efficiency Standards - Appliances and Electrical Equipment Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[appliances and electrical equipment 27,hard coal if]","Industry Energy Efficiency Standards - Appliances and Electrical Equipment Coal Use",[0,0.844],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[appliances and electrical equipment 27,natural gas if]","Industry Energy Efficiency Standards - Appliances and Electrical Equipment Natural Gas Use",[0,0.0844],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[appliances and electrical equipment 27,biomass if]","Industry Energy Efficiency Standards - Appliances and Electrical Equipment Biomass Use",[0,0.0844],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[appliances and electrical equipment 27,petroleum diesel if]","Industry Energy Efficiency Standards - Appliances and Electrical Equipment Petroleum Use",[0,0.0844],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[appliances and electrical equipment 27,heat if]","Industry Energy Efficiency Standards - Appliances and Electrical Equipment Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[appliances and electrical equipment 27,crude oil if]","Industry Energy Efficiency Standards - Appliances and Electrical Equipment Crude Oil Use",[0,0.0844],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[appliances and electrical equipment 27,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Appliances and Electrical Equipment Heavy or Residual Fuel Oil Use",[0,0.0844],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[appliances and electrical equipment 27,LPG propane or butane if]","Industry Energy Efficiency Standards - Appliances and Electrical Equipment LPG Propane or Butane Use",[0,0.0844],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[appliances and electrical equipment 27,hydrogen if]","Industry Energy Efficiency Standards - Appliances and Electrical Equipment Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other machinery 28,electricity if]","Industry Energy Efficiency Standards - Other Machinery Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other machinery 28,hard coal if]","Industry Energy Efficiency Standards - Other Machinery Coal Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other machinery 28,natural gas if]","Industry Energy Efficiency Standards - Other Machinery Natural Gas Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other machinery 28,biomass if]","Industry Energy Efficiency Standards - Other Machinery Biomass Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other machinery 28,petroleum diesel if]","Industry Energy Efficiency Standards - Other Machinery Petroleum Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other machinery 28,heat if]","Industry Energy Efficiency Standards - Other Machinery Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other machinery 28,crude oil if]","Industry Energy Efficiency Standards - Other Machinery Crude Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other machinery 28,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Other Machinery Heavy or Residual Fuel Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other machinery 28,LPG propane or butane if]","Industry Energy Efficiency Standards - Other Machinery LPG Propane or Butane Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other machinery 28,hydrogen if]","Industry Energy Efficiency Standards - Other Machinery Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[road vehicles 29,electricity if]","Industry Energy Efficiency Standards - Road Vehicles Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[road vehicles 29,hard coal if]","Industry Energy Efficiency Standards - Road Vehicles Coal Use",[0,0.1294],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[road vehicles 29,natural gas if]","Industry Energy Efficiency Standards - Road Vehicles Natural Gas Use",[0,0.1294],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[road vehicles 29,biomass if]","Industry Energy Efficiency Standards - Road Vehicles Biomass Use",[0,0.1294],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[road vehicles 29,petroleum diesel if]","Industry Energy Efficiency Standards - Road Vehicles Petroleum Use",[0,0.1294],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[road vehicles 29,heat if]","Industry Energy Efficiency Standards - Road Vehicles Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[road vehicles 29,crude oil if]","Industry Energy Efficiency Standards - Road Vehicles Crude Oil Use",[0,0.1294],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[road vehicles 29,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Road Vehicles Heavy or Residual Fuel Oil Use",[0,0.1294],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[road vehicles 29,LPG propane or butane if]","Industry Energy Efficiency Standards - Road Vehicles LPG Propane or Butane Use",[0,0.1294],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[road vehicles 29,hydrogen if]","Industry Energy Efficiency Standards - Road Vehicles Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[nonroad vehicles 30,electricity if]","Industry Energy Efficiency Standards - Nonroad Vehicles Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[nonroad vehicles 30,hard coal if]","Industry Energy Efficiency Standards - Nonroad Vehicles Coal Use",[0,0.2114],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[nonroad vehicles 30,natural gas if]","Industry Energy Efficiency Standards - Nonroad Vehicles Natural Gas Use",[0,0.2114],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[nonroad vehicles 30,biomass if]","Industry Energy Efficiency Standards - Nonroad Vehicles Biomass Use",[0,0.2114],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[nonroad vehicles 30,petroleum diesel if]","Industry Energy Efficiency Standards - Nonroad Vehicles Petroleum Use",[0,0.2114],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[nonroad vehicles 30,heat if]","Industry Energy Efficiency Standards - Nonroad Vehicles Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[nonroad vehicles 30,crude oil if]","Industry Energy Efficiency Standards - Nonroad Vehicles Crude Oil Use",[0,0.2114],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[nonroad vehicles 30,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Nonroad Vehicles Heavy or Residual Fuel Oil Use",[0,0.2114],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[nonroad vehicles 30,LPG propane or butane if]","Industry Energy Efficiency Standards - Nonroad Vehicles LPG Propane or Butane Use",[0,0.2114],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[nonroad vehicles 30,hydrogen if]","Industry Energy Efficiency Standards - Nonroad Vehicles Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other manufacturing 31T33,electricity if]","Industry Energy Efficiency Standards - Other Manufacturing Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other manufacturing 31T33,hard coal if]","Industry Energy Efficiency Standards - Other Manufacturing Coal Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other manufacturing 31T33,natural gas if]","Industry Energy Efficiency Standards - Other Manufacturing Natural Gas Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other manufacturing 31T33,biomass if]","Industry Energy Efficiency Standards - Other Manufacturing Biomass Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other manufacturing 31T33,petroleum diesel if]","Industry Energy Efficiency Standards - Other Manufacturing Petroleum Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other manufacturing 31T33,heat if]","Industry Energy Efficiency Standards - Other Manufacturing Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other manufacturing 31T33,crude oil if]","Industry Energy Efficiency Standards - Other Manufacturing Crude Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other manufacturing 31T33,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Other Manufacturing Heavy or Residual Fuel Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other manufacturing 31T33,LPG propane or butane if]","Industry Energy Efficiency Standards - Other Manufacturing LPG Propane or Butane Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other manufacturing 31T33,hydrogen if]","Industry Energy Efficiency Standards - Other Manufacturing Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[energy pipelines and gas processing 352T353,electricity if]","Industry Energy Efficiency Standards - Gas Production and Supply Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[energy pipelines and gas processing 352T353,hard coal if]","Industry Energy Efficiency Standards - Gas Production and Supply Coal Use",[0,0.0052],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[energy pipelines and gas processing 352T353,natural gas if]","Industry Energy Efficiency Standards - Gas Production and Supply Natural Gas Use",[0,0.0052],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[energy pipelines and gas processing 352T353,biomass if]","Industry Energy Efficiency Standards - Gas Production and Supply Biomass Use",[0,0.0052],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[energy pipelines and gas processing 352T353,petroleum diesel if]","Industry Energy Efficiency Standards - Gas Production and Supply Petroleum Use",[0,0.0052],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[energy pipelines and gas processing 352T353,heat if]","Industry Energy Efficiency Standards - Gas Production and Supply Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[energy pipelines and gas processing 352T353,crude oil if]","Industry Energy Efficiency Standards - Gas Production and Supply Crude Oil Use",[0,0.0052],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[energy pipelines and gas processing 352T353,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Gas Production and Supply Heavy or Residual Fuel Oil Use",[0,0.0052],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[energy pipelines and gas processing 352T353,LPG propane or butane if]","Industry Energy Efficiency Standards - Gas Production and Supply LPG Propane or Butane Use",[0,0.0052],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[energy pipelines and gas processing 352T353,hydrogen if]","Industry Energy Efficiency Standards - Gas Production and Supply Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[water and waste 36T39,electricity if]","Industry Energy Efficiency Standards - Water and Waste Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[water and waste 36T39,hard coal if]","Industry Energy Efficiency Standards - Water and Waste Coal Use",[0,0.0034],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[water and waste 36T39,natural gas if]","Industry Energy Efficiency Standards - Water and Waste Natural Gas Use",[0,0.0034],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[water and waste 36T39,biomass if]","Industry Energy Efficiency Standards - Water and Waste Biomass Use",[0,0.0034],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[water and waste 36T39,petroleum diesel if]","Industry Energy Efficiency Standards - Water and Waste Petroleum Use",[0,0.0034],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[water and waste 36T39,heat if]","Industry Energy Efficiency Standards - Water and Waste Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[water and waste 36T39,crude oil if]","Industry Energy Efficiency Standards - Water and Waste Crude Oil Use",[0,0.0034],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[water and waste 36T39,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Water and Waste Heavy or Residual Fuel Oil Use",[0,0.0034],"Industry Energy Efficiency Standards"),
(True,"Percentage Improvement in Eqpt Efficiency Standards above BAU[water and waste 36T39,LPG propane or butane if]","Industry Energy Efficiency Standards - Water and Waste LPG Propane or Butane Use",[0,0.0034],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[water and waste 36T39,hydrogen if]","Industry Energy Efficiency Standards - Water and Waste Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[construction 41T43,electricity if]","Industry Energy Efficiency Standards - Construction Electricity Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[construction 41T43,hard coal if]","Industry Energy Efficiency Standards - Construction Coal Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[construction 41T43,natural gas if]","Industry Energy Efficiency Standards - Construction Natural Gas Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[construction 41T43,biomass if]","Industry Energy Efficiency Standards - Construction Biomass Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[construction 41T43,petroleum diesel if]","Industry Energy Efficiency Standards - Construction Petroleum Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[construction 41T43,heat if]","Industry Energy Efficiency Standards - Construction Purchased Heat Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[construction 41T43,crude oil if]","Industry Energy Efficiency Standards - Construction Crude Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[construction 41T43,heavy or residual fuel oil if]","Industry Energy Efficiency Standards - Construction Heavy or Residual Fuel Oil Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[construction 41T43,LPG propane or butane if]","Industry Energy Efficiency Standards - Construction LPG Propane or Butane Use",[0,0.25],"Industry Energy Efficiency Standards"),
(False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[construction 41T43,hydrogen if]","Industry Energy Efficiency Standards - Construction Hydrogen Use",[0,0.25],"Industry Energy Efficiency Standards"),
(True,"Percent Reduction in Nonenergy Nonagriculture Industry Product Demand[refined petroleum and coke 19]","Material Efficiency, Longevity, n Re-Use - Refined Petroleum and Coke",[0,0.039],"Material Efficiency, Longevity, n Re-Use"),
(True,"Percent Reduction in Nonenergy Nonagriculture Industry Product Demand[cement and other nonmetallic minerals 239]","Material Efficiency, Longevity, n Re-Use - Cement and Other Nonmetallic Minerals",[0,0.217],"Material Efficiency, Longevity, n Re-Use"),
(True,"Percent Reduction in Nonenergy Nonagriculture Industry Product Demand[iron and steel 241]","Material Efficiency, Longevity, n Re-Use - Iron and Steel",[0,0.219],"Material Efficiency, Longevity, n Re-Use"),
(True,"Percent Reduction in Nonenergy Nonagriculture Industry Product Demand[other metals 242]","Material Efficiency, Longevity, n Re-Use - Other Metals",[0,0.081],"Material Efficiency, Longevity, n Re-Use"),
(False,"Percent Reduction in Nonenergy Nonagriculture Industry Product Demand[water and waste 36T39]","Material Efficiency, Longevity, n Re-Use - Water and Waste",[0,1],"Material Efficiency, Longevity, n Re-Use"),
(False,"Fraction of Methane Capture Opportunities Achieved[oil and gas extraction 06]","Methane Capture - Oil and Gas Extraction",[0,1],"Methane Capture and Destruction"),
(False,"Fraction of Methane Capture Opportunities Achieved[energy pipelines and gas processing 352T353]","Methane Capture - Gas Production and Supply",[0,1],"Methane Capture and Destruction"),
(False,"Fraction of Methane Capture Opportunities Achieved[coal mining 05]","Methane Capture - Coal Mining",[0,1],"Methane Capture and Destruction"),
(False,"Fraction of Methane Capture Opportunities Achieved[water and waste 36T39]","Methane Capture - Water and Waste",[0,1],"Methane Capture and Destruction"),
(False,"Fraction of Methane Destruction Opportunities Achieved[oil and gas extraction 06]","Methane Destruction - Oil and Gas Extraction",[0,1],"Methane Capture and Destruction"),
(False,"Fraction of Methane Destruction Opportunities Achieved[energy pipelines and gas processing 352T353]","Methane Destruction - Gas Production and Supply",[0,1],"Methane Capture and Destruction"),
(False,"Fraction of Methane Destruction Opportunities Achieved[coal mining 05]","Methane Destruction - Coal Mining",[0,1],"Methane Capture and Destruction"),
(False,"Fraction of Methane Destruction Opportunities Achieved[water and waste 36T39]","Methane Destruction - Water and Waste",[0,1],"Methane Capture and Destruction"),
(False,"Fraction of N2O Abatement Achieved","N2O Abatement",[0,1],"N2O Abatement"),
(False,"Percent Reduction in Fossil Fuel Exports[hard coal]","Reduce Fossil Fuel Exports - Hard Coal",[0,1],"Percent Reduction in Fossil Fuel Exports"),
(False,"Percent Reduction in Fossil Fuel Exports[natural gas]","Reduce Fossil Fuel Exports - Natural Gas",[0,1],"Percent Reduction in Fossil Fuel Exports"),
(False,"Percent Reduction in Fossil Fuel Exports[petroleum gasoline]","Reduce Fossil Fuel Exports - Petroleum Gasoline",[0,1],"Percent Reduction in Fossil Fuel Exports"),
(False,"Percent Reduction in Fossil Fuel Exports[petroleum diesel]","Reduce Fossil Fuel Exports - Petroleum Diesel",[0,1],"Percent Reduction in Fossil Fuel Exports"),
(False,"Percent Reduction in Fossil Fuel Exports[jet fuel or kerosene]","Reduce Fossil Fuel Exports - Jet Fuel/Kerosene",[0,1],"Percent Reduction in Fossil Fuel Exports"),
(False,"Percent Reduction in Fossil Fuel Exports[crude oil]","Reduce Fossil Fuel Exports - Crude Oil",[0,1],"Percent Reduction in Fossil Fuel Exports"),
(False,"Percent Reduction in Fossil Fuel Exports[heavy or residual fuel oil]","Reduce Fossil Fuel Exports - Heavy/Residual Fuel Oil",[0,1],"Percent Reduction in Fossil Fuel Exports"),
(False,"Percent Reduction in Fossil Fuel Exports[LPG propane or butane]","Reduce Fossil Fuel Exports - LPG/Propane/Butane",[0,1],"Percent Reduction in Fossil Fuel Exports"),

# Agriculture, Land Use, and Forestry Sector Policies
(True,"Fraction of Afforestation and Reforestation Achieved","Afforestation and Reforestation",[0,0.739],"Afforestation and Reforestation"),
(False,"Fraction of Avoided Deforestation Achieved","Avoid Deforestation",[0,1],"Avoid Deforestation"),
(True,"Fraction of Forest Restoration Achieved","Forest Restoration",[0,0.8],"Forest Restoration"),
(False,"Fraction of Forest Set Asides Achieved","Forest Set-Asides",[0,1],"Forest Set-Asides"),
(False,"Fraction of Cropland and Rice Measures Achieved","Cropland and Rice Measures",[0,1],"Cropland and Rice Measures"),
(False,"Fraction of CO2 Storage Through Tillage Practices","Improved Soil Measures",[0,1],"Improved Soil Measures"),
(True,"Fraction of Improved Forest Management Achieved","Improved Forest Management",[0,1],"Improved Forest Management"),
(False,"Fraction of Livestock Measures Achieved","Livestock Measures",[0,1],"Livestock Measures"),
(False,"Fraction of Peatland Restoration Achieved","Wetland Restoration",[0,1],"Wetland Restoration"),
(False,"Percent Animal Products Shifted to Nonanimal Products","Shift to Non-Animal Products",[0,1],"Shift to Non-Animal Products"),

# District Heat and Hydrogen Sector Policies
(False,"Fraction of Non CHP Heat Production Converted to CHP","Use CHP for District Heat",[0,1],"District Heat CHP"),
(True,"Fraction of District Heat Fuel Use Shifted to Other Fuels","Produce District Heat with Hydrogen",[0,1],"District Heat Fuel Switching"),
(True,"Fraction of Hydrogen Production Pathways Shifted","Shift Hydrogen Production to Electrolysis",[0,1],"Hydrogen Electrolysis"),

# Cross-Sector Sector Policies
(False,"Additional Carbon Tax Rate[transportation sector]","Carbon Price - Transportation Sector",[0,300],"Carbon Price"),
(False,"Additional Carbon Tax Rate[electricity sector]","Carbon Price - Electricity Sector",[0,300],"Carbon Price"),
(False,"Additional Carbon Tax Rate[residential buildings sector]","Carbon Price - Residential Bldg Sector",[0,300],"Carbon Price"),
(False,"Additional Carbon Tax Rate[commercial buildings sector]","Carbon Price - Commercial Bldg Sector",[0,300],"Carbon Price"),
(False,"Additional Carbon Tax Rate[industry sector]","Carbon Price - Industry Sector",[0,300],"Carbon Price"),
(False,"Additional Carbon Tax Rate[district heat and hydrogen sector]","Carbon Price - District Heat n Hydrogen Sector",[0,300],"Carbon Price"),
(False,"Percent Reduction in BAU Subsidies[hard coal]","End Existing Subsidies - Hard Coal",[0,1],"End Existing Subsidies"),
(False,"Percent Reduction in BAU Subsidies[natural gas]","End Existing Subsidies - Natural Gas",[0,1],"End Existing Subsidies"),
(False,"Percent Reduction in BAU Subsidies[nuclear]","End Existing Subsidies - Nuclear",[0,1],"End Existing Subsidies"),
(False,"Percent Reduction in BAU Subsidies[solar]","End Existing Subsidies - Solar",[0,1],"End Existing Subsidies"),
(False,"Percent Reduction in BAU Subsidies[petroleum gasoline]","End Existing Subsidies - Petroleum Gasoline",[0,1],"End Existing Subsidies"),
(False,"Percent Reduction in BAU Subsidies[petroleum diesel]","End Existing Subsidies - Petroleum Diesel",[0,1],"End Existing Subsidies"),
(False,"BEPEfCT Boolean Exempt Process Emissions from Carbon Tax[agriculture and forestry 01T03]","Exempt Process Emissions from C Tax - Agriculture and Forestry",[0,1],""),
(False,"BEPEfCT Boolean Exempt Process Emissions from Carbon Tax[coal mining 05]","Exempt Process Emissions from C Tax - Coal Mining",[0,1],""),
(False,"BEPEfCT Boolean Exempt Process Emissions from Carbon Tax[oil and gas extraction 06]","Exempt Process Emissions from C Tax - Oil and Gas Extraction",[0,1],""),
(False,"BEPEfCT Boolean Exempt Process Emissions from Carbon Tax[chemicals 20]","Exempt Process Emissions from C Tax - Chemicals",[0,1],""),
(False,"BEPEfCT Boolean Exempt Process Emissions from Carbon Tax[energy pipelines and gas processing 352T353]","Exempt Process Emissions from C Tax - Gas Production and Supply",[0,1],""),
(False,"BEPEfCT Boolean Exempt Process Emissions from Carbon Tax[water and waste 36T39]","Exempt Process Emissions from C Tax - Water and Waste",[0,1],""),
(False,"BDCTBA Boolean Disable Carbon Tax Border Adjustment","Toggle Carbon Tax Border Adjustment",[0,1],""),
(False,"Additional Fuel Tax or Subsidy Rate by Fuel[electricity]","Fuel Taxes or Subsidies - Electricity",[-0.5,0.5],"Fuel Taxes or Subsidies"),
(False,"Additional Fuel Tax or Subsidy Rate by Fuel[hard coal]","Fuel Taxes or Subsidies - Hard Coal",[-0.5,0.5],"Fuel Taxes or Subsidies"),
(False,"Additional Fuel Tax or Subsidy Rate by Fuel[natural gas]","Fuel Taxes or Subsidies - Natural Gas",[-0.5,0.5],"Fuel Taxes or Subsidies"),
(False,"Additional Fuel Tax or Subsidy Rate by Fuel[petroleum gasoline]","Fuel Taxes or Subsidies - Petroleum Gasoline",[-0.5,0.5],"Fuel Taxes or Subsidies"),
(False,"Additional Fuel Tax or Subsidy Rate by Fuel[petroleum diesel]","Fuel Taxes or Subsidies - Petroleum Diesel",[-0.5,0.5],"Fuel Taxes or Subsidies"),

# Research and Development Sector Policies
(False,"RnD Building Capital Cost Perc Reduction[heating]","Capital Cost Reduction - Buildings: Heating",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Building Capital Cost Perc Reduction[cooling and ventilation]","Capital Cost Reduction - Buildings: Cooling and Ventilation",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Building Capital Cost Perc Reduction[envelope]","Capital Cost Reduction - Buildings: Envelope",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Building Capital Cost Perc Reduction[lighting]","Capital Cost Reduction - Buildings: Lighting",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Building Capital Cost Perc Reduction[appliances]","Capital Cost Reduction - Buildings: Appliances",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Building Capital Cost Perc Reduction[other component]","Capital Cost Reduction - Buildings: Other Components",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD CCS Capital Cost Perc Reduction","Capital Cost Reduction - Carbon Capture and Sequestration",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[hard coal es]","Capital Cost Reduction - Electricity: Hard Coal",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[natural gas nonpeaker es]","Capital Cost Reduction - Electricity: Natural Gas Nonpeaker",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[nuclear es]","Capital Cost Reduction - Electricity: Nuclear",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[hydro es]","Capital Cost Reduction - Electricity: Hydro",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[onshore wind es]","Capital Cost Reduction - Electricity: Onshore Wind",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[solar PV es]","Capital Cost Reduction - Electricity: Solar PV",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[solar thermal es]","Capital Cost Reduction - Electricity: Solar Thermal",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[biomass es]","Capital Cost Reduction - Electricity: Biomass",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[natural gas peaker es]","Capital Cost Reduction - Electricity: Natural Gas Peaker",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[lignite es]","Capital Cost Reduction - Electricity: Gangue",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Electricity Capital Cost Perc Reduction[offshore wind es]","Capital Cost Reduction - Electricity: Offshore Wind",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[agriculture and forestry 01T03]","Capital Cost Reduction - Industry: Agriculture and Forestry",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[coal mining 05]","Capital Cost Reduction - Industry: Coal Mining",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[oil and gas extraction 06]","Capital Cost Reduction - Industry: Oil and Gas Extraction",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[other mining and quarrying 07T08]","Capital Cost Reduction - Industry: Other Mining and Quarrying",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[food beverage and tobacco 10T12]","Capital Cost Reduction - Industry: Food Beverage and Tobacco",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[textiles apparel and leather 13T15]","Capital Cost Reduction - Industry: Textiles Apparel and Leather",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[wood products 16]","Capital Cost Reduction - Industry: Wood Products and Furniture",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[pulp paper and printing 17T18]","Capital Cost Reduction - Industry: Pulp Paper and Printing",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[refined petroleum and coke 19]","Capital Cost Reduction - Industry: Refined Petroleum and Coke",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[chemicals 20]","Capital Cost Reduction - Industry: Chemicals",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[rubber and plastic products 22]","Capital Cost Reduction - Industry: Rubber and Plastic Products",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[glass and glass products 231]","Capital Cost Reduction - Industry: Specialized Eqiupment Manufacturing",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[cement and other nonmetallic minerals 239]","Capital Cost Reduction - Industry: Cement Glassand Other Nonmetallic Minerals",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[iron and steel 241]","Capital Cost Reduction - Industry: Iron and Steel",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[other metals 242]","Capital Cost Reduction - Industry: Other Metals",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[metal products except machinery and vehicles 25]","Capital Cost Reduction - Industry: Metal Products Except Machinery and Vehicles",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[computers and electronics 26]","Capital Cost Reduction - Industry: Computers and Electronics",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[appliances and electrical equipment 27]","Capital Cost Reduction - Industry: Appliances and Electrical Equipment",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[other machinery 28]","Capital Cost Reduction - Industry: Other Machinery",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[road vehicles 29]","Capital Cost Reduction - Industry: Road Vehicles",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[nonroad vehicles 30]","Capital Cost Reduction - Industry: Nonroad Vehicles",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[other manufacturing 31T33]","Capital Cost Reduction - Industry: Other Manufacturing",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[energy pipelines and gas processing 352T353]","Capital Cost Reduction - Industry: Gas Production and Supply",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[water and waste 36T39]","Capital Cost Reduction - Industry: Water and Waste",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Industry Capital Cost Perc Reduction[construction 41T43]","Capital Cost Reduction - Industry: Construction",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Transportation Capital Cost Perc Reduction[battery electric vehicle]","Capital Cost Reduction - Vehicles: Battery Electric",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Transportation Capital Cost Perc Reduction[natural gas vehicle]","Capital Cost Reduction - Vehicles: Natural Gas",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Transportation Capital Cost Perc Reduction[gasoline vehicle]","Capital Cost Reduction - Vehicles: Gasoline Engine",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Transportation Capital Cost Perc Reduction[diesel vehicle]","Capital Cost Reduction - Vehicles: Diesel Engine",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Transportation Capital Cost Perc Reduction[plugin hybrid vehicle]","Capital Cost Reduction - Vehicles: Plug-in Hybrid",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Transportation Capital Cost Perc Reduction[LPG vehicle]","Capital Cost Reduction - Vehicles: LPG",[0,0.4],"RnD Capital Cost Reductions"),
(False,"RnD Transportation Capital Cost Perc Reduction[hydrogen vehicle]","Capital Cost Reduction - Vehicles: Hydrogen",[0,0.4],"RnD Capital Cost Reductions"),
(False,"Fraction of Direct Air Capture Potential Achieved","Direct Air Capture",[0,1],"Direct Air Capture"),
(False,"RnD Building Fuel Use Perc Reduction[heating]","Fuel Use Reduction - Buildings: Heating",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Building Fuel Use Perc Reduction[cooling and ventilation]","Fuel Use Reduction - Buildings: Cooling and Ventilation",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Building Fuel Use Perc Reduction[lighting]","Fuel Use Reduction - Buildings: Lighting",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Building Fuel Use Perc Reduction[appliances]","Fuel Use Reduction - Buildings: Appliances",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Building Fuel Use Perc Reduction[other component]","Fuel Use Reduction - Buildings: Other Components",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD CCS Fuel Use Perc Reduction","Fuel Use Reduction - Carbon Capture and Sequestration",[0,0.4],"RnD Fuel Use Reductions"),
(True,"RnD Electricity Fuel Use Perc Reduction[hard coal es]","Fuel Use Reduction - Electricity: Hard Coal",[0,0.018],"RnD Fuel Use Reductions"),
(False,"RnD Electricity Fuel Use Perc Reduction[natural gas nonpeaker es]","Fuel Use Reduction - Electricity: Natural Gas Nonpeaker",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Electricity Fuel Use Perc Reduction[nuclear es]","Fuel Use Reduction - Electricity: Nuclear",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Electricity Fuel Use Perc Reduction[biomass es]","Fuel Use Reduction - Electricity: Biomass",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Electricity Fuel Use Perc Reduction[natural gas peaker es]","Fuel Use Reduction - Electricity: Natural Gas Peaker",[0,0.4],"RnD Fuel Use Reductions"),
(True,"RnD Electricity Fuel Use Perc Reduction[lignite es]","Fuel Use Reduction - Electricity: Gangue",[0,0.018],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[agriculture and forestry 01T03]","Fuel Use Reduction - Industry: Agriculture and Forestry",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[coal mining 05]","Fuel Use Reduction - Industry: Coal Mining",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[oil and gas extraction 06]","Fuel Use Reduction - Industry: Oil and Gas Extraction",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[other mining and quarrying 07T08]","Fuel Use Reduction - Industry: Other Mining and Quarrying",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[food beverage and tobacco 10T12]","Fuel Use Reduction - Industry: Food Beverage and Tobacco",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[textiles apparel and leather 13T15]","Fuel Use Reduction - Industry: Textiles Apparel and Leather",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[wood products 16]","Fuel Use Reduction - Industry: Wood Products and Furniture",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[pulp paper and printing 17T18]","Fuel Use Reduction - Industry: Pulp Paper and Printing",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[refined petroleum and coke 19]","Fuel Use Reduction - Industry: Refined Petroleum and Coke",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[chemicals 20]","Fuel Use Reduction - Industry: Chemicals",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[rubber and plastic products 22]","Fuel Use Reduction - Industry: Rubber and Plastic Products",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[glass and glass products 231]","Fuel Use Reduction - Industry: Specialized Equipment Manufacturing",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[cement and other nonmetallic minerals 239]","Fuel Use Reduction - Industry: Cement Glass and Other Nonmetallic Minerals",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[iron and steel 241]","Fuel Use Reduction - Industry: Iron and Steel",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[other metals 242]","Fuel Use Reduction - Industry: Other Metals",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[metal products except machinery and vehicles 25]","Fuel Use Reduction - Industry: Metal Products Except Machinery and Vehicles",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[computers and electronics 26]","Fuel Use Reduction - Industry: Computers and Electronics",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[appliances and electrical equipment 27]","Fuel Use Reduction - Industry: Appliances and Electrical Equipment",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[other machinery 28]","Fuel Use Reduction - Industry: Other Machinery",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[road vehicles 29]","Fuel Use Reduction - Industry: Road Vehicles",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[nonroad vehicles 30]","Fuel Use Reduction - Industry: Nonroad Vehicles",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[other manufacturing 31T33]","Fuel Use Reduction - Industry: Other Manufacturing",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[energy pipelines and gas processing 352T353]","Fuel Use Reduction - Industry: Gas Production and Supply",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[water and waste 36T39]","Fuel Use Reduction - Industry: Water and Waste",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Industry Fuel Use Perc Reduction[construction 41T43]","Fuel Use Reduction - Industry: Construction",[0,0.4],"RnD Fuel Use Reductions"),
(True,"RnD Transportation Fuel Use Perc Reduction[battery electric vehicle]","Fuel Use Reduction - Vehicles: Battery Electric",[0,0.1],"RnD Fuel Use Reductions"),
(False,"RnD Transportation Fuel Use Perc Reduction[natural gas vehicle]","Fuel Use Reduction - Vehicles: Natural Gas",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Transportation Fuel Use Perc Reduction[gasoline vehicle]","Fuel Use Reduction - Vehicles: Gasoline Engine",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Transportation Fuel Use Perc Reduction[diesel vehicle]","Fuel Use Reduction - Vehicles: Diesel Engine",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Transportation Fuel Use Perc Reduction[plugin hybrid vehicle]","Fuel Use Reduction - Vehicles: Plug-in Hybrid",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Transportation Fuel Use Perc Reduction[LPG vehicle]","Fuel Use Reduction - Vehicles: LPG",[0,0.4],"RnD Fuel Use Reductions"),
(False,"RnD Transportation Fuel Use Perc Reduction[hydrogen vehicle]","Fuel Use Reduction - Vehicles: Hydrogen",[0,0.4],"RnD Fuel Use Reductions"),

# Government Revenue Accounting Sector Policies
(False,"GRA for Carbon Tax Revenue[regular spending]","Carbon Tax Revenue - Regular Spending",[0,10],""),
(False,"GRA for Carbon Tax Revenue[deficit spending]","Carbon Tax Revenue - Budget Deficit",[0,10],""),
(False,"GRA for Carbon Tax Revenue[household taxes]","Carbon Tax Revenue - Household Taxes",[0,10],""),
(False,"GRA for Carbon Tax Revenue[payroll taxes]","Carbon Tax Revenue - Payroll Taxes",[0,10],""),
(False,"GRA for Carbon Tax Revenue[corporate taxes]","Carbon Tax Revenue - Corporate Income Taxes",[0,10],""),
(False,"GRA for Fuel Tax Revenue[regular spending]","Fuel Tax Revenue - Regular Spending",[0,10],""),
(False,"GRA for Fuel Tax Revenue[deficit spending]","Fuel Tax Revenue - Budget Deficit",[0,10],""),
(False,"GRA for Fuel Tax Revenue[household taxes]","Fuel Tax Revenue - Household Taxes",[0,10],""),
(False,"GRA for Fuel Tax Revenue[payroll taxes]","Fuel Tax Revenue - Payroll Taxes",[0,10],""),
(False,"GRA for Fuel Tax Revenue[corporate taxes]","Fuel Tax Revenue - Corporate Income Taxes",[0,10],""),
(False,"GRA for EV Subsidy[regular spending]","EV Subsidy - Regular Spending",[0,10],""),
(False,"GRA for EV Subsidy[deficit spending]","EV Subsidy - Budget Deficit",[0,10],""),
(False,"GRA for EV Subsidy[household taxes]","EV Subsidy - Household Taxes",[0,10],""),
(False,"GRA for EV Subsidy[payroll taxes]","EV Subsidy - Payroll Taxes",[0,10],""),
(False,"GRA for EV Subsidy[corporate taxes]","EV Subsidy - Corporate Income Taxes",[0,10],""),
(False,"GRA for Electricity Generation Subsidies[regular spending]","Electricity Generation Subsidy - Regular Spending",[0,10],""),
(False,"GRA for Electricity Generation Subsidies[deficit spending]","Electricity Generation Subsidy - Budget Deficit",[0,10],""),
(False,"GRA for Electricity Generation Subsidies[household taxes]","Electricity Generation Subsidy - Household Taxes",[0,10],""),
(False,"GRA for Electricity Generation Subsidies[payroll taxes]","Electricity Generation Subsidy - Payroll Taxes",[0,10],""),
(False,"GRA for Electricity Generation Subsidies[corporate taxes]","Electricity Generation Subsidy - Corporate Income Taxes",[0,10],""),
(False,"GRA for Electricity Capacity Construction Subsidies[regular spending]","Electricity Capacity Construction Subsidy - Regular Spending",[0,10],""),
(False,"GRA for Electricity Capacity Construction Subsidies[deficit spending]","Electricity Capacity Construction Subsidy - Budget Deficit",[0,10],""),
(False,"GRA for Electricity Capacity Construction Subsidies[household taxes]","Electricity Capacity Construction Subsidy - Household Taxes",[0,10],""),
(False,"GRA for Electricity Capacity Construction Subsidies[payroll taxes]","Electricity Capacity Construction Subsidy - Payroll Taxes",[0,10],""),
(False,"GRA for Electricity Capacity Construction Subsidies[corporate taxes]","Electricity Capacity Construction Subsidy - Corporate Income Taxes",[0,10],""),
(False,"GRA for Distributed Solar Subsidy[regular spending]","Distributed Solar Subsidy - Regular Spending",[0,10],""),
(False,"GRA for Distributed Solar Subsidy[deficit spending]","Distributed Solar Subsidy - Budget Deficit",[0,10],""),
(False,"GRA for Distributed Solar Subsidy[household taxes]","Distributed Solar Subsidy - Household Taxes",[0,10],""),
(False,"GRA for Distributed Solar Subsidy[payroll taxes]","Distributed Solar Subsidy - Payroll Taxes",[0,10],""),
(False,"GRA for Distributed Solar Subsidy[corporate taxes]","Distributed Solar Subsidy - Corporate Income Taxes",[0,10],""),
(False,"GRA for Fuel Subsidies[regular spending]","Fuel Subsidy - Regular Spending",[0,10],""),
(False,"GRA for Fuel Subsidies[deficit spending]","Fuel Subsidy - Budget Deficit",[0,10],""),
(False,"GRA for Fuel Subsidies[household taxes]","Fuel Subsidy - Household Taxes",[0,10],""),
(False,"GRA for Fuel Subsidies[payroll taxes]","Fuel Subsidy - Payroll Taxes",[0,10],""),
(False,"GRA for Fuel Subsidies[corporate taxes]","Fuel Subsidy - Corporate Income Taxes",[0,10],""),
(False,"GRA for National Debt Interest[regular spending]","National Debt Interest - Regular Spending",[0,10],""),
(False,"GRA for National Debt Interest[deficit spending]","National Debt Interest - Budget Deficit",[0,10],""),
(False,"GRA for National Debt Interest[household taxes]","National Debt Interest - Household Taxes",[0,10],""),
(False,"GRA for National Debt Interest[payroll taxes]","National Debt Interest - Payroll Taxes",[0,10],""),
(False,"GRA for National Debt Interest[corporate taxes]","National Debt Interest - Corporate Income Taxes",[0,10],""),
(False,"GRA for Remaining Government Cash Flow Changes[regular spending]","Remaining Government Cash Flows - Regular Spending",[0,10],""),
(False,"GRA for Remaining Government Cash Flow Changes[deficit spending]","Remaining Government Cash Flows - Budget Deficit",[0,10],""),
(False,"GRA for Remaining Government Cash Flow Changes[household taxes]","Remaining Government Cash Flows - Household Taxes",[0,10],""),
(False,"GRA for Remaining Government Cash Flow Changes[payroll taxes]","Remaining Government Cash Flows - Payroll Taxes",[0,10],""),
(False,"GRA for Remaining Government Cash Flow Changes[corporate taxes]","Remaining Government Cash Flows - Corporate Income Taxes",[0,10],"")

# Control Settings Sector Policies

)

# Building the Policy List
# ------------------------
# Every policy, whether enabled or not, appears in a tuple called "PotentialPolicies" that was constructed above.
# Now we construct the actual list of policies to be included (named "Policies") by
# checking which of the policies have been enabled.

Policies = []
for PotentialPolicy in PotentialPolicies:
	if PotentialPolicy[Enabled]:
		Policies.append(PotentialPolicy)


# Exit with an error if no policies were enabled in the script.  We write the error to the output
# file because it's likely a user will run this without a console and won't be able to see the
# message produced by sys.exit()
if len(Policies) < 1:
	f = open(OutputScript, 'w')
	ErrorMessage = "Error: No policies were enabled in the Python script.  Before running the script, you must enable at least one policy."
	f.write(ErrorMessage)
	f.close()
	import sys
	sys.exit(ErrorMessage)


# Building the Groups List
# ------------------------
# We create a list of all the unique groups that are used by enabled policies.
Groups = []
for Policy in Policies:
	if Policy[Group] not in Groups:
		Groups.append(Policy[Group])


# Generate Vensim Command Script
# ------------------------------
# We begin by creating a new file to serve as the Vensim command script (overwriting
# any older version at that filename).  We then tell Vensim to load
# the model file, and we give it a RUNNAME that will be used for all runs.  (It is
# overwritten each run.)
f = open(OutputScript, 'w')
f.write('SPECIAL>LOADMODEL|"' + ModelFile + '"\n')
f.write("SIMULATE>RUNNAME|" + RunName + "\n")

# The following options may be useful in certain cases, but they may slow Vensim down
# or increase the odds that Vensim crashes during execution of a batch of runs (though
# it is hard to tell for sure).  These lines are usually best left commented out.
# f.write("SPECIAL>NOINTERACTION\n")
# f.write("SIMULATE>SAVELIST|" + OutputVarsFile + "\n")
f.write("\n")

def PerformRunsWithEnabledGroups():

	# First, we do a run with all of the groups disabled
	f.write("MENU>RUN|O\n")
	f.write("MENU>VDF2TAB|" + RunName + ".vdfx|" + RunResultsFile + "|" + OutputVarsFile + "|||" + FirstYear + "|" + FinalYear + "|:")
	f.write("\tEnabledPolicyGroup=None")
	f.write("\tEnabledPolicies=None\n\n")

	# Next, we do a run with each group enabled in turn
	for EnabledGroup in Groups:

		# We create an empty string that we'll use to track the policies enabled in each group
		EnabledPolicies=""

		# We activate policies if their group name matches the currently enabled group
		for Policy in Policies:
			if Policy[Group] == EnabledGroup:
				f.write("SIMULATE>SETVAL|" + Policy[LongName] + "=" + str(Policy[Settings][1]) + "\n")
				# We add the policy to the EnabledPolicies string
				if len(EnabledPolicies) > 0:
					EnabledPolicies += ", "
				EnabledPolicies += Policy[ShortName]

		# We include a SETVAL instruction to select the correct policy implementation schedule file
		f.write("SIMULATE>SETVAL|Policy Implementation Schedule Selector=" + str(PolicySchedule) + "\n")
		
		# We perform our run and log the output
		f.write("MENU>RUN|O\n")
		f.write("MENU>VDF2TAB|" + RunName + ".vdfx|" + RunResultsFile + "|" + OutputVarsFile + "|+!||" + FirstYear + "|" + FinalYear + "|:")
		f.write("\tEnabledPolicyGroup=" + str(EnabledGroup))
		f.write("\tEnabledPolicies=" + EnabledPolicies + "\n\n")
	
	# Finally, we do a run with all of the policy groups enabled (a full policy case run)
	for Policy in Policies:
		f.write("SIMULATE>SETVAL|" + Policy[LongName] + "=" + str(Policy[Settings][1]) + "\n")
	
	# We include a SETVAL instruction to select the correct policy implementation schedule file
	f.write("SIMULATE>SETVAL|Policy Implementation Schedule Selector=" + str(PolicySchedule) + "\n")
	
	f.write("MENU>RUN|O\n")
	f.write("MENU>VDF2TAB|" + RunName + ".vdfx|" + RunResultsFile + "|" + OutputVarsFile + "|+!||" + FirstYear + "|" + FinalYear + "|:")
	f.write("\tEnabledPolicyGroup=All")
	f.write("\tEnabledPolicies=All")
	f.write("\n")

	# We instruct Vensim to delete the .vdfx file, to prevent it from getting picked up by
	# sync software, such as DropBox or Google Drive.  If sync software locks the file,
	# Vensim won't be able to overwrite it on the next model run, ruining the batch.
	f.write("FILE>DELETE|" + RunName + ".vdfx")
	f.write("\n\n")
	
def PerformRunsWithDisabledGroups():

	# First, we do a run with all of the groups enabled
	for Policy in Policies:
		f.write("SIMULATE>SETVAL|" + Policy[LongName] + "=" + str(Policy[Settings][1]) + "\n")
	
	# We include a SETVAL instruction to select the correct policy implementation schedule file
	f.write("SIMULATE>SETVAL|Policy Implementation Schedule Selector=" + str(PolicySchedule) + "\n")
	
	f.write("MENU>RUN|O\n")
	f.write("MENU>VDF2TAB|" + RunName + ".vdfx|" + RunResultsFile + "|" + OutputVarsFile + "|||" + FirstYear + "|" + FinalYear + "|:")
	f.write("\tDisabledPolicyGroup=None")
	f.write("\tDisabledPolicies=None\n\n")

	# Next, we do a run with each group disabled in turn
	for DisabledGroup in Groups:

		# We create an empty string that we'll use to track the policies disabled in each group
		DisabledPolicies=""

		# We activate policies if their group name does not match the currently disabled group
		for Policy in Policies:
			if Policy[Group] != DisabledGroup:
				f.write("SIMULATE>SETVAL|" + Policy[LongName] + "=" + str(Policy[Settings][1]) + "\n")
			# Otherwise, we add the policy to the DisabledPolicies string
			else:
				if len(DisabledPolicies) > 0:
					DisabledPolicies += ", "
				DisabledPolicies += Policy[ShortName]
		
		# We include a SETVAL instruction to select the correct policy implementation schedule file
		f.write("SIMULATE>SETVAL|Policy Implementation Schedule Selector=" + str(PolicySchedule) + "\n")
		
		# We perform our run and log the output
		f.write("MENU>RUN|O\n")
		f.write("MENU>VDF2TAB|" + RunName + ".vdfx|" + RunResultsFile + "|" + OutputVarsFile + "|+!||" + FirstYear + "|" + FinalYear + "|:")
		f.write("\tDisabledPolicyGroup=" + str(DisabledGroup))
		f.write("\tDisabledPolicies=" + DisabledPolicies + "\n\n")
	
	# Finally, we do a run with all of the groups disabled (a BAU case run)
	f.write("MENU>RUN|O\n")
	f.write("MENU>VDF2TAB|" + RunName + ".vdfx|" + RunResultsFile + "|" + OutputVarsFile + "|+!||" + FirstYear + "|" + FinalYear + "|:")
	f.write("\tDisabledPolicyGroup=All")
	f.write("\tDisabledPolicies=All")
	f.write("\n")

	# We instruct Vensim to delete the .vdfx file, to prevent it from getting picked up by
	# sync software, such as DropBox or Google Drive.  If sync software locks the file,
	# Vensim won't be able to overwrite it on the next model run, ruining the batch.
	f.write("FILE>DELETE|" + RunName + ".vdfx")
	f.write("\n\n")
	
if EnableOrDisableGroups == "Enable":
	PerformRunsWithEnabledGroups()
else:
	PerformRunsWithDisabledGroups()

# We are done writing the Vensim command script and therefore close the file.
f.close()
