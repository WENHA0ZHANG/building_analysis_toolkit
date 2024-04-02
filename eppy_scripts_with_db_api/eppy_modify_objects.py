from eppy import modeleditor
from eppy.modeleditor import IDF

def before_energy_simulation():
        IDF.setiddname(api_environment.EnergyPlusInputIddPath)
        idf_file = IDF(api_environment.EnergyPlusInputIdfPath)
        zone_objects = idf_file.idfobjects["zone"][0]
        idf_file.idfobjects["Zone"][0].Direction_of_Relative_North = 45
       

        idf_file.save()
