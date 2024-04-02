from eppy import modeleditor
from eppy.modeleditor import IDF

def before_energy_simulation():
        IDF.setiddname(api_environment.EnergyPlusInputIddPath)
        idf_file = IDF(api_environment.EnergyPlusInputIdfPath)
        idf_file.newidfobject("MATERIAL")
        idf_file.idfobjects["MATERIAL"][-1].Name = "Polyurethane Foam"

        new_material = idf_file.idfobjects["MATERIAL"][-1]

        new_material.Roughness = 'MediumSmooth'
        new_material.Thickness = 0.03
        new_material.Conductivity = 0.16
        new_material.Density = 600
        new_material.Specific_Heat = 1500

        construction_objects = idf_file.idfobjects['CONSTRUCTION']
        for construction_object in construction_objects:
            if 'wall' in construction_object.Name:
                construction_object.Layer_3 = 'Polyurethane Foam'       

        idf_file.save()